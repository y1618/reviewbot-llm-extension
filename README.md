# ReviewBot LLM拡張機能

OpenWebUIやllamacppを通じてローカル大規模言語モデル（LLM）を使用して自動コードレビューを実行するReviewBot拡張機能です。

## 機能

- OpenWebUI HTTP APIとllamacppローカル実行の両方をサポート
- 設定可能なバックエンド選択
- 包括的なコードレビュープロンプト
- JSON構造化されたレビュー応答
- 複数のプログラミング言語をサポート（Python、JavaScript、TypeScript、Java、C/C++、Go、Rust、Ruby、PHP）
- 設定可能な温度とトークン制限
- ネットワーク問題とモデル読み込み失敗のエラーハンドリング

## インストール

### Dockerインストール（推奨）

ReviewBot LLM拡張機能を使用する最も簡単な方法は、公式の`beanbag/reviewbot-base`イメージを拡張したDockerを使用することです：

```bash
# リポジトリをクローン
git clone https://github.com/y1618/reviewbot-llm-extension.git
cd reviewbot-llm-extension

# Dockerイメージをビルド
docker build -t reviewbot-llm .

# docker-composeで実行
docker-compose up -d
```

### 手動インストール

1. このリポジトリをクローン：
```bash
git clone https://github.com/y1618/reviewbot-llm-extension.git
cd reviewbot-llm-extension
```

2. 拡張機能をインストール：
```bash
pip install -e .
```

## 設定

Review Boardで以下のオプションを使用してツールを設定します：

### バックエンド選択
- **Backend**: 'openwebui'または'llamacpp'を選択

### OpenWebUI設定
- **OpenWebUI URL**: サーバーURL（デフォルト: http://localhost:3000）
- **OpenWebUI API Key**: 認証用のオプションAPIキー
- **Model Name**: OpenWebUIインスタンスで利用可能なモデル名

### llamacpp設定
- **Model Name**: GGUFモデルファイルへのフルパス（例：`/path/to/model.gguf`）

### 一般設定
- **Max Tokens**: LLM応答の最大トークン数（デフォルト: 1000）
- **Temperature**: LLM応答の温度（0.0-1.0、低いほど集中的、デフォルト: 0.1）
- **Custom Instructions**: LLMが従うプロジェクト固有のコーディングルールとガイドライン（オプション）

## Docker設定

### 基本セットアップ（外部OpenWebUI/Ollama）

デフォルトのDocker設定には以下のみが含まれます：

- **reviewbot-llm**: LLM拡張機能を含むメインReviewBotコンテナ
- **redis**: ReviewBot用メッセージブローカー

この設定では、OpenWebUIとOllamaをホストシステムで別途実行していることを前提としています。

### 環境変数

環境変数を使用してLLM拡張機能を設定します：

```bash
# バックエンド選択
REVIEWBOT_LLM_BACKEND=openwebui  # または 'llamacpp'

# OpenWebUI設定（外部）
REVIEWBOT_LLM_OPENWEBUI_URL=http://host.docker.internal:3000
REVIEWBOT_LLM_OPENWEBUI_API_KEY=your_api_key_here  # オプション
REVIEWBOT_LLM_MODEL_NAME=llama2
REVIEWBOT_LLM_MAX_TOKENS=1000
REVIEWBOT_LLM_TEMPERATURE=0.1
REVIEWBOT_LLM_CUSTOM_INSTRUCTIONS="PythonコードはPEP 8に従う。意味のある変数名を使用する。"  # オプション
```

### デプロイメントオプション

#### オプション1: 外部OpenWebUI/Ollama（推奨）
```bash
# OpenWebUIとOllamaを別途起動
# その後ReviewBot LLM拡張機能を実行
docker-compose up -d
```

#### オプション2: フルスタック（オールインワン）
docker-compose.ymlのOpenWebUIとOllamaサービスのコメントを外す：
```bash
# docker-compose.ymlを編集してOpenWebUI/Ollamaサービスのコメントを外す
docker-compose up -d
```

### サービスアクセス

- **Redis**: localhost:6379のメッセージブローカー
- **OpenWebUI**: 外部インスタンス（通常 http://localhost:3000）
- **Ollama**: 外部インスタンス（通常 http://localhost:11434）

## サポート環境

- **SCM**: Git、Subversion、Mercurial（SCM非依存設計）
- **言語**: Python、JavaScript、TypeScript、Java、C/C++、Go、Rust、Ruby、PHP
- **フレームワーク**: ROS2、標準Pythonプロジェクト
- **デプロイメント**: Docker、ベアメタル、クラウド環境

## 要件

- ReviewBot
- requests（OpenWebUI統合用）
- llama-cpp-python（ローカルllamacpp実行用）
- DockerとDocker Compose（コンテナ化デプロイメント用）

## 使用方法

1. Review Boardで拡張機能をインストールして設定
2. レビューリクエストにLLM Code Reviewツールを追加
3. ツールが自動的にコードファイルを分析してレビューコメントを提供
4. コメントはReview Boardの通常のレビューコメントとして表示

## サポートファイルタイプ

- Python (*.py)
- JavaScript (*.js)
- TypeScript (*.ts)
- Java (*.java)
- C/C++ (*.c, *.cpp, *.h)
- Go (*.go)
- Rust (*.rs)
- Ruby (*.rb)
- PHP (*.php)

## バックエンド詳細

### OpenWebUI
- OpenWebUIインスタンスへのHTTP API呼び出しを使用
- OpenAI互換（`/v1/chat/completions`）とネイティブ（`/api/chat`）エンドポイントの両方をサポート
- エンドポイント間の自動フォールバック
- オプションAPIキー認証

### llamacpp
- llama-cpp-pythonを使用した直接ローカル実行
- パフォーマンス向上のためのモデルキャッシュ
- 設定可能なコンテキストサイズとスレッド
- GGUFモデル形式をサポート

## エラーハンドリング

拡張機能には以下の包括的なエラーハンドリングが含まれています：
- ネットワーク接続問題（OpenWebUI）
- モデル読み込み失敗（llamacpp）
- 無効なJSON応答
- ファイルエンコーディング問題
- API認証エラー

## 開発

このプロジェクトに貢献するには：

1. リポジトリをフォーク
2. フィーチャーブランチを作成
3. 変更を加える
4. 該当する場合はテストを追加
5. プルリクエストを送信

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細はLICENSEファイルを参照してください。

## サポート

問題や質問については：
- GitHubでissueを開く
- ReviewBotドキュメントを確認
- OpenWebUIまたはllamacppの設定を確認
