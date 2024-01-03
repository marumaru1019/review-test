import openai
from github import Github
import os

def get_pr():
    # GitHub Actionsが提供するトークンを使用
    g = Github(os.getenv('GITHUB_TOKEN'))

    # リポジトリの取得
    repo = g.get_repo(f"{os.getenv('GITHUB_REPOSITORY')}")

    # プルリクエストの取得
    pr_number = int(os.getenv('PULL_REQUEST_NUMBER'))
    pr = repo.get_pull(pr_number)
    return pr

def get_openai_review(deployment_name: str, 
                      pr, 
                      system_prompt: str
                      ) -> str:

    # プルリクエストの差分を取得
    diffs = pr.get_files()

    review_messages = []

    for diff in diffs:

        try:
            response = openai.ChatCompletion.create(
                engine=deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": diff.patch}
                ],
                max_tokens=1000
            )
            message = response["choices"][0]["message"]["content"]
            # return message.strip()
            review_messages.append(f"{diff.filename}:\n{message.strip()}")
        except openai.OpenAIError as e:
            print(f"An error occurred: {e}")
            # return "No feedback."
            review_messages.append(f"{diff.filename}:\nNo feedback.")

    return review_messages