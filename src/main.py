import openai
import json
import sys
from review import get_openai_review
# from pr import add_comment_to_pr

# Load config values
with open(r'config.json') as config_file:
    config_details = json.load(config_file)
    
# Setting up the deployment name
deployment_name = config_details['DEPLOYMENT_NAME']
print(deployment_name)

# This is set to `azure`
openai.api_type = "azure"

# The API key for your Azure OpenAI resource.
openai.api_key = config_details["OPENAI_API_KEY"]

# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"
openai.api_base = config_details['OPENAI_API_BASE']

# Currently Chat Completion API have the following versions available: 2023-07-01-preview
openai.api_version = config_details['OPENAI_API_VERSION']

# MEMO: 日本語でプロンプトを作成することで、レビューの言語が自動的に日本語に設定される。
INSTRUCTIONS_JP = ("プルリクエストのコードレビュアーとして振る舞い、可能性のあるバグやクリーンなコードの問題についてフィードバックを提供してください。\n"
                   "あなたにはパッチ形式でプルリクエストの変更が提供されます。\n"
                   "各パッチエントリには、コミットメッセージがサブジェクト行に続いてコードの変更点（diff）がunidiff形式で記載されています。\n\n"
                   "コードレビュアーとしてのあなたのタスクは以下の通りです：\n"
                   "- 追加された行、編集された行、削除された行のみをレビューしてください。\n"
                   "- バグがなく、変更が正しい場合は「フィードバックなし」とのみ記述してください。\n"
                   "- バグがある場合やコードの変更が不正確である場合は、「フィードバックなし」と記述しないでください。")


def main():
    # Call the review function from review.py
    # review_message = get_openai_review("GPTPullRequestReview/src/git.ts")
    review_messages = get_openai_review(INSTRUCTIONS_JP)
    for review_message in review_messages:

        # Print out the review message
        print(f"レビューメッセージ: {review_message}")

if __name__ == "__main__":
    main()