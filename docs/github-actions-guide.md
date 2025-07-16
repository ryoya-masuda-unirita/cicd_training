# GitHub Actions ガイド

## 目次
1. [概要](#概要)
2. [ワークフローの基本](#ワークフローの基本)
3. [アクションの使用（uses）](#アクションの使用)
4. [ジョブとステップの詳細](#ジョブとステップの詳細)
5. [CI/CDパイプライン](#cicdパイプライン)
6. [シークレット管理](#シークレット管理)
7. [環境変数と文脈](#環境変数と文脈)
8. [トラブルシューティング](#トラブルシューティング)

## 概要

GitHub Actionsは、GitHubに統合された自動化ツールです。以下のような作業を自動化できます：
- コードのテスト
- アプリケーションのビルド
- コンテナイメージの作成
- クラウドへのデプロイ

## ワークフローの基本

### ワークフローファイルの場所
```
.github/
└── workflows/
    ├── main.yml     # テスト用ワークフロー
    └── deploy.yml   # デプロイ用ワークフロー
```

### 基本的な構文
```yaml
name: ワークフロー名

on:  # トリガーの定義
  push:
    branches: [ main ]
    paths-ignore:    # 特定のパスを除外
      - 'docs/**'
      - '**.md'
  pull_request:
    branches: [ main ]
    types: [opened, synchronize, reopened]

jobs:  # ジョブの定義
  job-name:
    runs-on: ubuntu-latest
    steps:
      - name: ステップ名
        run: コマンド
```

### 主要なトリガー
- `push`: コードがプッシュされた時
- `pull_request`: PRが作成/更新された時
- `workflow_dispatch`: 手動実行
- `schedule`: 定期実行（cron形式）
  ```yaml
  on:
    schedule:
      - cron: '0 0 * * *'  # 毎日午前0時
  ```
- `workflow_call`: 他のワークフローから呼び出し可能

## アクションの使用

### usesとは
`uses`キーワードは、既存のアクションを再利用するための指示です。以下の形式があります：

1. **公開アクション**
```yaml
steps:
  - uses: actions/checkout@v4   # GitHubが提供する公式アクション
```
- `actions`: 組織名
- `checkout`: アクション名
- `@v4`: バージョン指定

2. **Dockerコンテナ**
```yaml
steps:
  - uses: docker://alpine:3.8
    with:
      entrypoint: /bin/echo
      args: Hello, World!
```

3. **ローカルアクション**
```yaml
steps:
  - uses: ./.github/actions/my-action
```

### 主要なアクションの解説

1. **actions/checkout**
```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0  # 全履歴を取得
    submodules: true  # サブモジュールも取得
```
- リポジトリのコードをチェックアウト
- ほとんどのワークフローで最初に使用

2. **actions/setup-python**
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.10'
    architecture: 'x64'  # アーキテクチャ指定
    cache: 'pip'  # 依存関係のキャッシュ
```
- Python環境のセットアップ
- バージョン管理とキャッシュ機能

3. **docker/build-push-action**
```yaml
- uses: docker/build-push-action@v5
  with:
    context: .
    file: ./Dockerfile
    push: true
    tags: |
      myorg/myimage:latest
      myorg/myimage:${{ github.sha }}
    cache-from: type=registry,ref=myorg/myimage:buildcache
    cache-to: type=registry,ref=myorg/myimage:buildcache,mode=max
```
- Dockerイメージのビルドとプッシュ
- キャッシュ機能でビルド時間を短縮

4. **azure/login**
```yaml
- uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```
- Azureへの認証
- サービスプリンシパルを使用

## ジョブとステップの詳細

### ジョブの依存関係
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps: [...]

  build:
    needs: test    # testジョブの完了を待つ
    runs-on: ubuntu-latest
    steps: [...]

  deploy:
    needs: [test, build]    # 複数の依存関係
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'    # 条件付き実行
    steps: [...]
```

### ジョブのマトリックス実行
```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ['3.8', '3.9', '3.10']
        exclude:    # 特定の組み合わせを除外
          - os: windows-latest
            python-version: '3.8'
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

### ステップの条件付き実行
```yaml
steps:
  - name: 条件付きステップ
    if: ${{ success() && github.event_name == 'push' }}
    run: echo "プッシュイベントで前のステップが成功"

  - name: 失敗時のステップ
    if: ${{ failure() }}
    run: echo "何かが失敗した"

  - name: 常に実行
    if: ${{ always() }}
    run: echo "結果に関わらず実行"
```

## 環境変数と文脈

### 組み込み変数
```yaml
steps:
  - name: 組み込み変数の使用
    run: |
      echo "リポジトリ: ${{ github.repository }}"
      echo "ブランチ: ${{ github.ref }}"
      echo "コミット: ${{ github.sha }}"
      echo "ワークフロー: ${{ github.workflow }}"
      echo "イベント: ${{ github.event_name }}"
```

### 環境変数の定義
```yaml
env:
  GLOBAL_VAR: "グローバル変数"    # ワークフロー全体

jobs:
  build:
    env:
      JOB_VAR: "ジョブ変数"      # ジョブ内
    steps:
      - name: ステップ変数
        env:
          STEP_VAR: "ステップ変数"  # ステップ内
        run: |
          echo $GLOBAL_VAR
          echo $JOB_VAR
          echo $STEP_VAR
```

### 文脈（Context）の使用
```yaml
steps:
  - name: 文脈の使用
    run: |
      # github文脈
      echo ${{ github.actor }}      # アクションを実行したユーザー
      echo ${{ github.event.pull_request.title }}  # PRのタイトル

      # env文脈
      echo ${{ env.MY_VARIABLE }}   # 環境変数

      # secrets文脈
      echo ${{ secrets.SECRET_KEY }}  # シークレット

      # runner文脈
      echo ${{ runner.os }}         # ランナーのOS
```

## CI/CDパイプライン

### テストワークフロー（main.yml）
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: pytest
```

### デプロイワークフロー（deploy.yml）
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Build and push
      run: |
        docker build -t myapp .
        docker push myapp
```

## シークレット管理

### シークレットの設定方法
1. GitHubリポジトリの「Settings」タブを開く
2. 左メニューから「Secrets and variables」→「Actions」を選択
3. 「New repository secret」ボタンをクリック
4. 名前と値を入力して保存

### シークレットの使用方法
```yaml
steps:
  - name: シークレットを使用
    env:
      API_KEY: ${{ secrets.API_KEY }}
    run: echo "APIキーを使用"
```

### 主なシークレット
- `AZURE_CLIENT_ID`: Azureクライアントid
- `AZURE_TENANT_ID`: AzureテナントID
- `AZURE_SUBSCRIPTION_ID`: Azureサブスクリプション

## トラブルシューティング

### よくあるエラー

1. **Permission denied**
   ```yaml
   # 解決策：権限を追加
   permissions:
     contents: read
     packages: write
   ```

2. **Secrets not available**
   - シークレットが正しく設定されているか確認
   - シークレット名が正しいか確認
   - 環境変数の参照方法が正しいか確認

3. **Runner error**
   - ランナーのOSが正しいか確認
   - 必要なツールがインストールされているか確認

### デバッグ方法

1. **デバッグログの有効化**
   ```yaml
   env:
     ACTIONS_RUNNER_DEBUG: true
   ```

2. **ステップの出力確認**
   ```yaml
   steps:
     - name: デバッグ情報
       run: |
         pwd
         ls -la
         env
   ```

### ワークフローの実行確認
1. GitHubリポジトリの「Actions」タブを開く
2. 実行中または完了したワークフローを選択
3. ログを確認
4. 失敗したステップを特定

### アクションのデバッグ
```yaml
steps:
  - name: アクションのデバッグ
    uses: actions/checkout@v4
    with:
      debug: true    # デバッグモード有効化
```

### ステップのタイムアウト
```yaml
jobs:
  build:
    timeout-minutes: 30    # ジョブ全体のタイムアウト
    steps:
      - name: 長時間の処理
        timeout-minutes: 10    # 個別ステップのタイムアウト
        run: |
          echo "長時間の処理"
```

## ベストプラクティス

1. **バージョン管理**
   - アクションのバージョンは具体的に指定
   - `@main`や`@master`は非推奨
   ```yaml
   # 良い例
   - uses: actions/checkout@v4
   
   # 悪い例
   - uses: actions/checkout@master
   ```

2. **キャッシュの活用**
   ```yaml
   - uses: actions/cache@v3
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
   ```

3. **アーティファクトの管理**
   ```yaml
   - uses: actions/upload-artifact@v3
     with:
       name: my-artifact
       path: dist/
       retention-days: 5    # 保持期間の設定
   ```

4. **セキュリティ考慮事項**
   - シークレットは必ず`secrets`として管理
   - 最小権限の原則に従う
   - サードパーティアクションは慎重に選択

## 参考リンク
- [GitHub Actions 公式ドキュメント](https://docs.github.com/ja/actions)
- [GitHub Actions マーケットプレイス](https://github.com/marketplace?type=actions)
- [GitHub Actions サンプル集](https://github.com/actions/starter-workflows)
- [GitHub Actions 組み込み変数](https://docs.github.com/ja/actions/reference/environment-variables#default-environment-variables) 