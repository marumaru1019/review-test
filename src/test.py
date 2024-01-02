from github import Github
import os

def main():
    # GitHub Actionsが提供するトークンを使用
    g = Github(os.getenv('GITHUB_TOKEN'))

    # リポジトリの取得
    repo = g.get_repo(f"{os.getenv('GITHUB_REPOSITORY')}")

    # プルリクエストの取得
    pr = repo.get_pull(os.getenv('PULL_REQUEST_NUMBER'))

    # プルリクエストの差分を取得
    diff = pr.get_files()

    diff_text = ''


    # 出力
    for file in diff:
        diff_text += f'File: {file.filename}\n{file.patch}\n\n'
        print(f"File: {file.filename}, Status: {file.status}")

    print("Diff retrieved")
    print(diff_text)
    
if __name__ == "__main__":
    main()