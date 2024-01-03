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
INSTRUCTIONS_JP = """
プルリクエストのコードレビュアーとして振る舞い、可能性のあるバグやクリーンなコードの問題についてフィードバックを提供してください。
あなたにはパッチ形式でプルリクエストの変更が提供されます。
各パッチエントリには、コミットメッセージがサブジェクト行に続いてコードの変更点（diff）がunidiff形式で記載されています。

コードレビュアーとしてのあなたのタスクは以下の通りです：
- 追加された行、編集された行、削除された行のみをレビューしてください。
- バグがなく、変更が正しい場合は「フィードバックなし」とのみ記述してください。
- バグがある場合やコードの変更が不正確である場合は、どのように不正確であるか詳細に記載してください。
"""

system_prompt = os.environ.get('SYSTEM_PROMPT', INSTRUCTIONS_JP)

def main():
    pr = get_pr()
    review_messages = get_openai_review(deployment_name=deployment_name, pr=pr, system_prompt=system_prompt)
    for review_message in review_messages:
        # コメントの追加
        pr.create_issue_comment(review_message)

    # コメントを改行を入れてまとめて追加
    # pr.create_issue_comment("\n\n".join(review_messages))
        
if __name__ == "__main__":
    main()