import openai
from github import Github
import os

# MEMO: 日本語でプロンプトを作成することで、レビューの言語が自動的に日本語に設定される。
INSTRUCTIONS_JP = ("プルリクエストのコードレビュアーとして振る舞い、可能性のあるバグやクリーンなコードの問題についてフィードバックを提供してください。\n"
                   "あなたにはパッチ形式でプルリクエストの変更が提供されます。\n"
                   "各パッチエントリには、コミットメッセージがサブジェクト行に続いてコードの変更点（diff）がunidiff形式で記載されています。\n\n"
                   "コードレビュアーとしてのあなたのタスクは以下の通りです：\n"
                   "- 追加された行、編集された行、削除された行のみをレビューしてください。\n"
                   "- バグがなく、変更が正しい場合は「フィードバックなし」とのみ記述してください。\n"
                   "- バグがある場合やコードの変更が不正確である場合は、「フィードバックなし」と記述しないでください。")


def get_pr():
    # GitHub Actionsが提供するトークンを使用
    g = Github(os.getenv('GITHUB_TOKEN'))

    # リポジトリの取得
    repo = g.get_repo(f"{os.getenv('GITHUB_REPOSITORY')}")

    # プルリクエストの取得
    pr_number = int(os.getenv('PULL_REQUEST_NUMBER'))
    pr = repo.get_pull(pr_number)
    return pr

def get_openai_review(deployment_name ,pr, system_propmpt: str = INSTRUCTIONS_JP) -> str:

    # プルリクエストの差分を取得
    diffs = pr.get_files()

    review_messages = []

    for diff in diffs:

        try:
            response = openai.ChatCompletion.create(
                engine=deployment_name,
                messages=[
                    {"role": "system", "content": system_propmpt},
                    {"role": "user", "content": diff.patch}
                ],
                max_tokens=1000
            )
            message = response["choices"][0]["message"]["content"]
            # return message.strip()
            review_messages.append(f"{diff.filename}: {message.strip()}")
        except openai.OpenAIError as e:
            print(f"An error occurred: {e}")
            # return "No feedback."
            review_messages.append(f"{diff.filename}: No feedback.")

    return review_messages