# GitHub Actions 入門ガイド

## はじめに

### GitHub Actionsとは？
GitHub Actionsは、ソフトウェア開発の作業を自動化するためのツールです。
例えば、以下のような作業を自動的に行うことができます：

- プログラムが正しく動くかテストする
- アプリケーションを本番環境にアップロードする
- コードの品質をチェックする

これは、次のような状況で特に役立ちます：
```
例：チームでアプリ開発をしている場合
1. Aさんがコードを書いて GitHub に保存（プッシュ）
2. GitHub Actions が自動的にテストを実行
3. テストが成功したら、自動的にアプリを本番環境にアップロード
4. もしテストが失敗したら、チームに通知
```

### 基本的な用語説明

1. **ワークフロー（Workflow）**
   - 自動化したい一連の作業を書いたレシピのようなもの
   - `.github/workflows` フォルダの中に置く
   - `yml`（ヤムル）という形式のファイルで書く

2. **ジョブ（Job）**
   - ワークフローの中の大きな作業単位
   - 例：「テストする」「デプロイする」など
   ```yaml
   jobs:
     test:       # テストのジョブ
       steps:    # 具体的な手順
         - ...
     
     deploy:     # デプロイのジョブ
       steps:    # 具体的な手順
         - ...
   ```

3. **ステップ（Step）**
   - ジョブの中の細かい作業手順
   - 例：「Pythonをインストール」「テストを実行」など

4. **uses**
   - 他の人が作った便利な機能（アクション）を使うためのキーワード
   - 例：`uses: actions/checkout@v4`は、GitHubのコードを取得するアクション
   - `@v4`のような部分は、アクションのバージョンを指定
   ```yaml
   steps:
     - name: コードを取得
       uses: actions/checkout@v4    # GitHubのコードを取得
     
     - name: Nodeをセットアップ
       uses: actions/setup-node@v4  # Node.jsを準備
   ```

5. **with**
   - usesで指定したアクションに設定を渡すためのキーワード
   - アクションごとに設定できる項目が決まっている
   ```yaml
   steps:
     - name: Pythonをセットアップ
       uses: actions/setup-python@v5
       with:
         python-version: '3.10'    # Pythonのバージョンを指定
         architecture: 'x64'       # システムのアーキテクチャを指定
   ```

## 具体例で学ぶ

### 例1：簡単なテストの自動化

以下は、Pythonのプログラムをテストする最も基本的な例です：

```yaml
name: はじめてのワークフロー    # わかりやすい名前をつける

# いつ実行するか
on:
  push:                # コードをプッシュしたとき
    branches:
      - main          # mainブランチの場合

# 何をするか
jobs:
  # テストという作業
  test:
    runs-on: ubuntu-latest    # Ubuntu（Linux）で実行
    
    steps:
      # 1. コードを取ってくる
      - name: コードを取得
        uses: actions/checkout@v4
      
      # 2. Pythonを準備
      - name: Pythonをセットアップ
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'    # Pythonのバージョン
      
      # 3. 必要なものをインストール
      - name: 必要なパッケージをインストール
        run: |
          pip install pytest
          pip install -r requirements.txt
      
      # 4. テストを実行
      - name: テストを実行
        run: pytest
```

### 変数について学ぶ

変数は、何度も使う値や、後で変更するかもしれない値を保存するために使います。
GitHub Actionsには3つの種類の変数があります：

1. **グローバル変数**（全体で使える変数）
   ```yaml
   name: 変数の例
   
   # これが グローバル変数 の定義方法
   env:
     APP_NAME: "私のアプリ"      # どこでも使える
     API_URL: "https://api.example.com"
   
   jobs:
     test:
       steps:
         - name: アプリ名を表示
           run: echo $APP_NAME    # "私のアプリ" と表示される
   ```

2. **ジョブ変数**（特定のジョブの中だけで使える変数）
   ```yaml
   jobs:
     test:
       # これが ジョブ変数 の定義方法
       env:
         DEBUG_MODE: "ON"    # このジョブの中だけで使える
       
       steps:
         - name: デバッグモードを確認
           run: echo $DEBUG_MODE    # "ON" と表示される
   ```

3. **ステップ変数**（そのステップだけで使える変数）
   ```yaml
   steps:
     - name: 一時的な設定
       # これが ステップ変数 の定義方法
       env:
         TEMP_FILE: "data.txt"    # このステップだけで使える
       run: echo $TEMP_FILE       # "data.txt" と表示される
   ```

### 秘密の情報（シークレット）の扱い方

パスワードなどの秘密の情報は、特別な方法で管理します：

1. GitHubのリポジトリの設定画面で登録
   - Settings → Secrets and variables → Actions → New repository secret

2. 使い方
   ```yaml
   steps:
     - name: データベースに接続
       env:
         # シークレットはこのように使う
         PASSWORD: ${{ secrets.DATABASE_PASSWORD }}
       run: |
         echo "データベースに接続します..."
   ```

### よくある使い方

1. **テストの自動化**
   - コードが正しく動くかチェック
   - バグを早く見つけられる

2. **コードの品質チェック**
   - コードの書き方が正しいかチェック
   - チーム全員で同じルールを守れる

3. **自動デプロイ**
   - テストが成功したら自動的にアプリを更新
   - 手作業による間違いを防げる

## トラブルシューティング

### よくあるエラーと解決方法

1. **テストが失敗する**
   - エラーメッセージをよく読む
   - テストコードが正しいか確認
   - 必要なパッケージがインストールされているか確認

2. **シークレットが見つからない**
   - シークレットの名前が正しいか確認
   - リポジトリの設定で正しく登録されているか確認

3. **コマンドが見つからない**
   - 必要なツールがインストールされているか確認
   - パスが正しく設定されているか確認

### 困ったときは

1. **Actions タブを確認**
   - GitHubのリポジトリの「Actions」タブで実行結果を確認
   - エラーの詳細な情報が見られる

2. **ログを確認**
   - 失敗したジョブの詳細を開く
   - エラーメッセージを確認

## 参考リンク
- [GitHub Actions 公式ドキュメント（日本語）](https://docs.github.com/ja/actions)
- [GitHub Actions 入門ガイド（日本語）](https://docs.github.com/ja/actions/quickstart) 