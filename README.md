# GPT を活用したプルリクエストの自動レビュー
このリポジトリでは、Github のプルリクエストに対して、GPT を活用して自動でレビューコメントを追加するためのパイプラインを提供します。

## 構築手順

以下の手順を実施します。

### Github リポジトリの準備

**レビュー対象と同じリポジトリに配置する場合**

1. Github に任意のリポジトリを作成します。
1. 作成したリポジトリに、コードレビューの対象にしたいファイルを配置し、リモートリポジトリにプッシュします。
1. 作成したリポジトリに `src` と `requirements.txt` と `.github\workflows\gpt-pr-review.yml` を追加し、リモートリポジトリにプッシュします。

### Azure OpenAI の準備

1. [手順ページ](https://learn.microsoft.com/ja-JP/azure/ai-services/openai/how-to/create-resource) を参考に、Azure OpenAI のリソースを作成します。デプロイするモデルは `gpt-35-turbo` など GPT 系統のものを選択します。
1. 作成した AOAI の API キー、エンドポイント、デプロイ名を控えておきます。

### パイプラインの作成

1. Github から対象のリポジトリを選択して、Settings > Secrets and variables > Actions を選択します。
2. [手順ページ](https://docs.github.com/ja/actions/learn-github-actions/variables#creating-configuration-variables-for-a-repository) を参考に、スクリプトで利用する環境変数に対応した変数を追加します。

    | 環境変数  | 値 | 補足 |
    | ------------- | ------------- | ------------- |
    | OPENAI_API_KEY | Azure OpenAI の API キー | Azure Portal から AOAI のキーを確認します |
    | OPENAI_API_BASE  | Azure OpenAI のエンドポイント | Azure Portal から AOAI のエンドポイントを確認します |
    | DEPLOYMENT_NAME  | Azure OpenAI のデプロイ名 | Azure OpenAI Studio からデプロイ名を確認します |


## 動作確認

1. 構築手順で指定したブランチをマージ先に指定したプルリクエストを作成します。
1. 自動でパイプラインがスタートしたことを確認します。
1. パイプラインの完了後、プルリクエストのコメントが追加されていることを確認します。

## 動作例

以下のような内容の Python ファイルを対象にしたプルリクエストを作成した場合、以下のようなコメントが追加されます。
この例では、関数内にいくつかのバグが含まれています。

```python
def monitor_battery_status(battery_voltage, battery_capacity, current_draw, total_distance_covered):
    # 電力消費を計算 (typo: correct variable name is 'battery_capacity')
    power_used = battery_voltge * current_draw  # typo: 'battery_voltage'
    
    # 現在のバッテリー充電レベルを計算
    current_charge_level = (battery_capacity - power_used) / battery_capacity * 100
    
    # 1km走行あたりの平均消費電力を計算
    avg_power_per_km = power_used / total_distance_covered  # potential bug: division by zero
    
    # 推定残り走行距離を計算
    estimated_range = (battery_capacity - power_used) / avg_power_per_km # potential bug: division by zero
    
    # 充電警告をチェック
    charge_warning = current_charge_level < 20  # battery needs charging if less than 20%
    
    return current_charge_level, estimated_range, charge_warning

if __name__ == "__main__":
    monitor_battery_status(12, 100, 10, 30)
```

これに対して、以下のようなコメントが追加されます。
Python ファイルの内容に対して、バグがある場合やコードの変更が不正確である場合は、どのように不正確であるか詳細に記載されます。

![image](https://github.com/marumaru1019/github-image/assets/70362624/0e4a1c77-66c9-4f1c-b94e-29ff26f99843)

## システムプロンプト

```
プルリクエストのコードレビュアーとして振る舞い、可能性のあるバグやクリーンなコードの問題についてフィードバックを提供してください。
あなたにはパッチ形式でプルリクエストの変更が提供されます。
各パッチエントリには、コミットメッセージがサブジェクト行に続いてコードの変更点（diff）がunidiff形式で記載されています。

コードレビュアーとしてのあなたのタスクは以下の通りです：
- 追加された行、編集された行、削除された行のみをレビューしてください。
- バグがなく、変更が正しい場合は「フィードバックなし」とのみ記述してください。
- バグがある場合やコードの変更が不正確である場合は、どのように不正確であるか詳細に記載してください。
```

## パイプラインサンプル

```yaml
name: GPT PR

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  run-script:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'  # Pythonバージョンを指定

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run GPT PR
      run: python src/main.py
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        GITHUB_REPOSITORY: ${{ github.repository }}
        PULL_REQUEST_NUMBER: ${{ github.event.pull_request.number }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        OPENAI_API_BASE: ${{ secrets.OPENAI_API_BASE }}
        DEPLOYMENT_NAME: ${{ secrets.DEPLOYMENT_NAME }}

```