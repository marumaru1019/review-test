import openai
import os
from review import *

# This is deployment name for your Azure OpenAI resource.
deployment_name = os.environ.get('DEPLOYMENT_NAME')

# This is set to `azure`
openai.api_type = "azure"

# The API key for your Azure OpenAI resource.
openai.api_key = os.environ.get('OPENAI_API_KEY')

# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"
openai.api_base = os.environ.get('OPENAI_API_BASE')

# Currently Chat Completion API have the following versions available: 2023-07-01-preview
# OPENAI_API_VERSION があれば使いなければデフォルト値を使用する
openai.api_version = os.environ.get('OPENAI_API_VERSION', '2023-07-01-preview')

# MEMO: 日本語でプロンプトを作成することで、レビューの言語が自動的に日本語に設定される。
INSTRUCTIONS_JP = ("プルリクエストのコードレビュアーとして振る舞い、可能性のあるバグやクリーンなコードの問題についてフィードバックを提供してください。\n"
                   "あなたにはパッチ形式でプルリクエストの変更が提供されます。\n"
                   "各パッチエントリには、コミットメッセージがサブジェクト行に続いてコードの変更点（diff）がunidiff形式で記載されています。\n\n"
                   "コードレビュアーとしてのあなたのタスクは以下の通りです：\n"
                   "- 追加された行、編集された行、削除された行のみをレビューしてください。\n"
                   "- バグがなく、変更が正しい場合は「フィードバックなし」とのみ記述してください。\n"
                   "- バグがある場合やコードの変更が不正確である場合は、「フィードバックなし」と記述しないでください。")


def main():
    pr = get_pr()
    review_messages = get_openai_review(deployment_name=deployment_name, pr=pr)
    for review_message in review_messages:

        # Print out the review message
        # コメントの追加
        pr.create_issue_comment(review_message)

if __name__ == "__main__":
    main()