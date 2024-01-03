from github import Github
import os

def main():
    # GitHub Actionsが提供するトークンを使用
    g = Github(os.getenv('GITHUB_TOKEN'))

    # リポジトリの取得
    repo = g.get_repo(f"{os.getenv('GITHUB_REPOSITORY')}")

    # プルリクエストの取得
    pr_number = int(os.getenv('PULL_REQUEST_NUMBER'))
    pr = repo.get_pull(pr_number)

    # プルリクエストの差分を取得
    diff = pr.get_files()

    diff_text = ''

    last_commit = pr.get_commits()[pr.commits - 1]

    # 出力
    for file in diff:
        diff_text += f'File: {file.filename}\n{file.patch}\n\n'
        print(f"File: {file.filename}, Status: {file.status}")

    # コメントを追加
    pr.create_issue_comment("This is a comment.")


    

if __name__ == "__main__":
    main()