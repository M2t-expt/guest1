# Python import
import os
import re
import threading

from github import Github
from flask import Flask, request, render_template

import scenario1

# Flask
app = Flask(__name__)
app.debug = False

# GitHub API
g = Github(os.environ.get('GITHUB_BOT_TOKEN'))

# Scenario
sce1 = scenario1.sce1
send_msg = scenario1.send_msg

# Test
def run_test(files):
  # 実行可能であればTrue、実行不可能であればFalseを返す
  # ダミーコード
  result = "OK"  # テスト結果
  executable = True  # 実行可能かどうか
  # send_msg("Test Result: Success")
  return result, executable

# Merge
def merge_pr(pr,pr_title):
  pr.merge()
  send_msg("bot:Pull Request「" + pr_title + "」をMergeしました")
  send_msg("bot:mainブランチに移動してリモートリポジトリの内容をPullしてください")

# Pull Request File Check
def test_pr(repo,pr,pr_title):
  print("Start Test...")
  files = pr.get_files()
  for file in files:
    if file.filename.endswith('.java'):
      if not run_test(file):
        send_msg("bot:テストがうまくいきませんでした\n変更内容を確認してしてください")
        return
  if pr_title == "User_1":
    merge_pr(pr,pr_title)
    sce1(repo,pr_title)
  elif pr_title == "User_2":
    sce1(repo,pr_title)
    merge_pr(pr,pr_title)

# Check Pull Request
def check_pr(repo_name, pr_number):
  # Pull Requestデータの取得
  send_msg("GCBot:Pull Requestの情報を取得中")
  repo = g.get_repo(repo_name)
  pr = repo.get_pull(pr_number)
  pr_creater = pr.user.login
  pr_title = pr.title
  if pr.state != 'open':
    send_msg("GCBot:Pull RequestがClosed")
    return
  elif re.match(r'^User_.*$', pr_title) and pr.state == 'open':
    send_msg("bot:ユーザーからのPull Requestを検知しました")
    # Pull Requestデータの送信
    pr_data = "リポジトリ名:" + repo_name + "\nPull Request番号:" + str(pr_number) + "\nPull Request名:" + pr_title + "\n作成者:" + pr_creater
    send_msg("bot:Pull Requestデータ\n" + pr_data)
  elif re.match(r'^Bot_.*$', pr_title):
    send_msg("GCBot:Botの作成したPull Requestです")
    return
  else:
    send_msg("bot:シナリオ外のPull Requestの作成を検知しました")
    return
  test_pr(repo,pr,pr_title)

# GitHub Event Detection
@app.route('/', methods=['POST'])
def handle_webhook():
  global status_text
  event_type = request.headers.get('X-GitHub-Event')

  # Pull Request検知
  if event_type == 'pull_request':
    send_msg("GCBot:Pull Requestを検知")
    data = request.get_json()
    repo_name = data['repository']['full_name']
    pr_number = data['number'] 
    t = threading.Thread(target=check_pr, args=(repo_name, pr_number))
    t.start()
  return 'PyGitHub'

# Flask Main
if __name__ == '__main__':
  app.run(debug=True)