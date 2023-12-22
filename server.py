import os
import asyncio
import websockets
import subprocess
import csv
import re

# すべてのメッセージを保存するリスト
logs = []
cmds = []

# コマンドプロンプトの実行結果
async def cmd_exe(cmd):
  try:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr
  except subprocess.CalledProcessError as e:
    return f"Error: {e.returncode}, {e.output}"
  
async def cmd_msg(msg):
  cmd = msg[4:]
  cmds.append(cmd)
  # cdのみ別処理
  if cmd.startswith("cd "):  # ユーザーが "cd ディレクトリ名" と指定した場合
    dir = cmd[3:]  # "cd "を除いたディレクトリ名を取得
    cmd = cmd[:3]
    os.chdir(dir)
  # 実行結果を送信
  stdout, stderr = await cmd_exe(cmd)
  return stdout, stderr

# CSVのロード
def load_sheet(file_name):
  commands = {}
  file_path = os.path.join('csv', file_name)
  with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      if len(row) == 2:
        commands[row[0]] = row[1]
  return commands

# メッセージ送信
async def msg_send(websocket, msg):  
  logs.append(msg)
  print(msg)
  if msg != "Log out":
    await websocket.send(msg)

class MessagePattern:
  def __init__(self):
    self.pattern = None

  async def handle_msg(self, msg):
    res = None
    if msg == "Help1":
      help1 = load_sheet('help1.csv')
      last_cmd = cmds[-1] if len(cmds) >= 1 else None
      for key, value in help1.items():
        if re.match(key, last_cmd):
          res = value
          break
      if res == None:
        res = "対応するコマンドが見つかりません"
    else:
      if msg in ["Pattern0", "Pattern1", "Pattern2"]:
        cmds.append(msg)
        self.pattern = msg
      if self.pattern != None:
        csv_f = f"{self.pattern}.csv"
        pattern_csv = load_sheet(csv_f)
        last_cmd = cmds[-1] if len(cmds) >= 1 else None
        for key, value in pattern_csv.items():
          if re.match(key, last_cmd):
            res = value
            break
      # res = pattern_csv.get(last_cmd, None)
    return res 

# メッセージ受信時
async def echo(websocket, path):
  msg_pattern = MessagePattern()

  async for msg in websocket:
    # 受信したメッセージをすべてのクライアントに送信
    await msg_send(websocket, msg)

    # コマンド入力の場合
    if msg.startswith("uni:") and msg != "uni:":
      stdout, stderr = await cmd_msg(msg)
      if stdout != None:
        await msg_send(websocket, "cmd:" + stdout)
      if stderr != None:
        await msg_send(websocket, "cmd:" + stderr)
    
    # コマンドもしくはシナリオ設定の場合
    if (msg.startswith("uni:") and msg != "uni:") or msg in ["Pattern0", "Pattern1", "Pattern2", "Help1"]:
      res = await msg_pattern.handle_msg(msg)
      if res != None:
        await msg_send(websocket, "bot:" + res)
    
    # タイトルへ戻る場合
    if msg == "Log out":
      with open("log/msg.txt", "w") as file:
        file.write("\n".join(logs))

async def main():
  server = await websockets.serve(echo, "localhost", 8765)
  await server.wait_closed()

if __name__ == "__main__":
  asyncio.run(main())
