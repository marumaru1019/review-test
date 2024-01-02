from github import Github
import os

def main():
    # GitHub Actionsが提供するトークンを使用
    g = Github(os.getenv('GITHUB_TOKEN'))

    # リポジトリの取得
    repo = g.get_repo(f"{os.getenv('GITHUB_REPOSITORY')}")

    # プルリクエストの取得
    pr = repo.get_pull(pull_request_number)

    # コメントの追加
    pr.create_issue_comment("Your automated review comment here")

    print("Comment added")

if __name__ == "__main__":
    main()