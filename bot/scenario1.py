# Python import
import asyncio
import websockets

# Unity WebSockets
uri = "ws://localhost:8765"  # UnityのWebSocketサーバーのアドレスを指定
loop = asyncio.get_event_loop()

async def send_to_unity(msg):
  async with websockets.connect(uri) as websocket:
    await websocket.send(msg)

# メッセージ送信
def send_msg(msg):
  print(msg)
  loop.run_until_complete(send_to_unity(msg))

# 新規ブランチの作成
def create_branch(repo,new_branch,base_branch):
  cnt = 1
  while new_branch in [b.name for b in repo.get_branches()]:
    cnt += 1
    new_branch = f"{new_branch}_{cnt}"
  repo.create_git_ref(ref=f'refs/heads/{new_branch}', sha=repo.get_branch(base_branch).commit.sha)
  msg = "GCBot:" + new_branch + "ブランチを作成"
  send_msg(msg)

# ファイルの編集とコミット
def edit_file_commit(repo,branch_name,file_name,edit_file):
  file = repo.get_contents(file_name)
  with open(edit_file, 'rb') as new_file:
    modified_content = new_file.read().decode('utf-8')
  msg = "GCBot:" + file_name + "を編集"
  repo.update_file(file_name, msg, modified_content, file.sha, branch_name)
  send_msg(msg)

# ブランチのプッシュ
def push_branch(repo,branch_name):
  repo.get_git_ref(f'heads/{branch_name}').edit(repo.get_branch(branch_name).commit.sha)
  msg = "GCBot:Push"
  send_msg(msg)

# プルリクエストの作成
def create_pull_request(repo,pr_title,branch_name,base_branch):
  repo.create_pull(title=pr_title, head=branch_name, base=base_branch)
  msg = "GCBot:Pull Request作成"
  send_msg(msg)


# 新規ファイル追加のプルリクエスト作成
def sce1(repo,pr_title):
  new_branch = "Bot"
  # シナリオ1-1
  if pr_title == 'User_1':
    # 新規ブランチの作成(Bot_1)
    create_branch(repo,new_branch,'master')

    # ファイルの編集とコミット
    file_name = 'GameMain.java'
    edit_file = '../bot_file/GameMain_Bot2.txt'
    edit_file_commit(repo,new_branch,file_name,edit_file)

    file_name = 'Hand.java'
    edit_file = '../bot_file/Hand_Bot2.txt'
    edit_file_commit(repo,new_branch,file_name,edit_file)

    # ブランチのプッシュ
    push_branch(repo,new_branch)

    # プルリクエストの作成
    pr_title = 'Bot_GameMain.javaで文章の表示'
    create_pull_request(repo,pr_title,new_branch,'main')
  # シナリオ1-2
  elif pr_title == 'User_2':
    # 新規ブランチの作成(Bot_2)
    create_branch(repo,new_branch,'master')

    # ファイルの編集とコミット
    file_name = 'GameMain.java'
    edit_file = '../bot_file/GameMain_Bot4.txt'
    edit_file_commit(repo,new_branch,file_name,edit_file)
    file_name = 'VictoryOrDefeat.java'
    edit_file = '../bot_file/VictoryOrDefeat_Bot4.txt'
    edit_file_commit(repo,new_branch,file_name,edit_file)

    # ブランチのプッシュ
    push_branch(repo,new_branch)

    # プルリクエストの作成
    pr_title = 'Bot_Computerの手の決定とその表示'
    create_pull_request(repo,pr_title,new_branch,'main')
