# GitHub Actions ガイド

## 目次
1. [概要](#概要)
2. [ワークフローの基本](#ワークフローの基本)
3. [CI/CDパイプライン](#cicdパイプライン)
4. [シークレット管理](#シークレット管理)
5. [トラブルシューティング](#トラブルシューティング)

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
  pull_request:
    branches: [ main ]

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
- `schedule`: 定期実行

### 環境変数の使用
```yaml
env:
  GLOBAL_VAR: "グローバル変数"

jobs:
  example:
    env:
      JOB_VAR: "ジョブ変数"
    steps:
      - env:
          STEP_VAR: "ステップ変数"
        run: echo $STEP_VAR
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

### ベストプラクティス
1. 小さなステップに分割
2. 明確な名前付け
3. タイムアウトの設定
4. 依存関係のキャッシュ
5. 必要最小限の権限使用

## 参考リンク
- [GitHub Actions 公式ドキュメント](https://docs.github.com/ja/actions)
- [GitHub Actions マーケットプレイス](https://github.com/marketplace?type=actions)
- [GitHub Actions サンプル集](https://github.com/actions/starter-workflows) 