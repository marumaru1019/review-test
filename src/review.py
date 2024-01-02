# from openai import ChatCompletion, OpenAIError
import openai
from git import Repo

# Constants
INSTRUCTIONS = ("Act as a code reviewer of a Pull Request, providing feedback on possible bugs and clean code issues.\n"
                "You are provided with the Pull Request changes in a patch format.\n"
                "Each patch entry has the commit message in the Subject line followed by the code changes (diffs) in a unidiff format.\n\n"
                "As a code reviewer, your task is:\n"
                "- Review only added, edited or deleted lines.\n"
                "- If there's no bugs and the changes are correct, write only 'No feedback.'\n"
                "- If there's bug or incorrect code changes, don't write 'No feedback.'")

def get_git_diff_files(repo_path) -> list:
    repo = Repo(repo_path)
    diffs = repo.git.diff(name_only=True).splitlines()
    return diffs


def get_git_diff(repo_path, target_branch, file_name) -> str:
    repo = Repo(repo_path)
    # Ensure the repo is not in a dirty state
    # if repo.is_dirty():
    #     raise Exception("The repository is dirty. Please commit or stash changes first.")
    # Get the git object for the file
    # git_file = repo.git.path(file_name)
    # # Fetch the latest changes for the target :
    # repo.git.fetch()
    # # Generate the diff for the file against the target branch
    print(repo.git.diff(name_only=True).splitlines())
    print("-----------------------")
    diff = repo.git.diff(file_name)
    return diff


def get_openai_review(system_propmpt: str = INSTRUCTIONS) -> str:
    # Example usage
    repo_path = '../../'  # Replace with the path to your local git repository
    target_branch = 'feature/add-review-sample'  # Replace with the target branch name
    diffs = get_git_diff_files(repo_path)

    review_messages = []

    for diff in diffs:

        patch = get_git_diff(repo_path, target_branch, diff)
        # print(patch)

        try:
            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",
                messages=[
                    {"role": "system", "content": system_propmpt},
                    {"role": "user", "content": patch}
                ],
                max_tokens=1000
            )
            message = response["choices"][0]["message"]["content"]
            # return message.strip()
            review_messages.append(f"{diff}: {message.strip()}")
        except openai.OpenAIError as e:
            print(f"An error occurred: {e}")
            # return "No feedback."
            review_messages.append(f"{diff}: No feedback.")

    return review_messages
