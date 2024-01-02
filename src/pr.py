from azure.devops.connection import Connection
from azure.devops.v7_1.git.git_client import GitClient
from azure.devops.v7_1.git.models import GitPullRequestCommentThread, Comment
from msrest.authentication import BasicAuthentication
import os

def add_comment_to_pr(comment):

    # Azure DevOpsのサービスURLとパーソナルアクセストークンを環境変数から取得
    organization_url = os.environ.get('SYSTEM_TEAMFOUNDATIONCOLLECTIONURI')
    personal_access_token = os.environ.get('SYSTEM_ACCESSTOKEN')

    # リポジトリIDとプルリクエストIDを環境変数から取得
    repository_id = os.environ.get('BUILD_REPOSITORY_ID')
    pull_request_id = int(os.environ.get('SYSTEM_PULLREQUEST_PULLREQUESTID'))

    # 認証情報と接続の設定
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)

    # Gitクライアントの取得
    git_client = connection.clients.get_git_client()

    # コメントスレッドを作成
    comment_thread = GitPullRequestCommentThread(
        comments=[Comment(content='ここにPRに追加するコメントを記入')],
        status='active'
    )

    # PRにコメントスレッドを追加
    added_thread = git_client.create_thread(comment_thread, repository_id, pull_request_id)

    print(f'Comment thread added with ID: {added_thread.id}')
