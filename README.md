# CI/CD学習プロジェクト

このプロジェクトは、CI/CD（継続的インテグレーション/継続的デリバリー）の基本を学ぶためのハンズオン学習用リポジトリです。
ローカル環境での基礎学習から始めて、最終的にはAzure環境での本格的なCI/CD構築まで行います。

# Phase 1: ローカル環境での基礎学習

## 1. 基本環境のセットアップ
### 1.1 必要な環境
- Git/GitHubアカウント
- Python 3.10以上
- Docker（ローカルコンテナ実行用）

### 1.2 初期セットアップ
```bash
# 仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate

# 必要なパッケージのインストール
pip install fastapi uvicorn pytest python-dotenv requests
```

## 2. サンプルアプリケーションの作成
### 2.1 プロジェクト構成
```
cicd_training/
├── .gitignore
├── README.md
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── models.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt
└── Dockerfile
```

### 2.2 実装内容
シンプルなREST APIを作成します：
- GET /health - ヘルスチェックエンドポイント
- GET /items - アイテム一覧取得
- POST /items - アイテム追加
- GET /items/{item_id} - 個別アイテム取得

## 3. ローカルでのテスト環境構築
### 3.1 テスト実装
- pytestを使用したユニットテスト
- テストカバレッジの計測
- テスト自動化の設定

### 3.2 テスト実行
```bash
# テストの実行
pytest

# カバレッジレポート付きでテスト実行
pytest --cov=app tests/
```

## 4. ローカルCI/CD環境（GitHub Actions）
### 4.1 基本ワークフロー
```yaml
# .github/workflows/main.yml の基本構成
- リポジトリのチェックアウト
- Pythonセットアップ
- 依存関係のインストール
- リンター実行（flake8）
- ユニットテスト実行
- テストカバレッジレポート生成
```

### 4.2 自動化項目
- プルリクエスト時の自動テスト
- コードの品質チェック
- セキュリティスキャン（dependabot等）

## 5. ローカルでのコンテナ化
### 5.1 Dockerfile
```dockerfile
# 基本的なDockerfile構成
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5.2 ローカル開発環境
```bash
# コンテナのビルドと実行
docker build -t cicd-training .
docker run -p 8000:8000 cicd-training
```

# Phase 2: Azure環境での本格的なCI/CD構築

## 6. Azure環境セットアップ
### 6.1 必要なツール
- Azure CLI
- Azure アカウントとサブスクリプション

### 6.2 Azure基本設定
- リソースグループの作成
- サービスプリンシパルの設定
- 必要な権限の付与

## 7. Azureリソースの構築
### 7.1 コンテナ関連
- Azure Container Registryの作成と設定
- Azure Container Appsの設定

### 7.2 モニタリング関連
- Application Insightsの設定
- Azure Logsの設定
- アラートの設定

## 8. Azure CI/CDパイプライン
### 8.1 GitHub Actions設定
- Azure認証情報の設定
- コンテナビルドとプッシュの自動化
- 自動デプロイの設定

### 8.2 本番環境デプロイ
- ステージング環境の構築
- Blue-Greenデプロイメントの設定
- ロールバック手順の確認

## 学習の進め方
1. Phase 1 をステップバイステップで完了
2. ローカル環境で十分な理解を得る
3. Phase 2 でAzure環境に移行
4. 本番環境を想定した運用手順の確認

## 注意点
- 各ステップでのベストプラクティスを意識する
- セキュリティ面での考慮（環境変数、シークレット管理）
- エラーハンドリングの実装
- ドキュメント作成の習慣化
- Azure利用時のコスト管理

## ライセンス
MIT

## 貢献について
プルリクエストや課題の報告は歓迎します。大きな変更を加える場合は、まずissueを作成して変更内容を議論してください。 