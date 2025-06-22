# ReviewBot LLM Extension - 使用例

このフォルダには、ReviewBot LLM拡張機能の設定例とサンプルファイルが含まれています。

## 📁 ファイル構成

### Docker Compose設定例
- `docker-compose.basic.yml` - 基本的な設定例（環境変数を直接指定）
- `docker-compose.env-file.yml` - .envファイルを使用した設定例（推奨）
- `custom_rules.env` - カスタムルール用の.envファイル例

### カスタムルールサンプル
- `example_custom_instructions.txt` - 基本的なコーディングルール例（1.3KB）
- `custom_instructions_large.txt` - 包括的なコーディングルール例（3.8KB）

## 🚀 使用方法

### 1. 基本的な使用方法
```bash
# 基本設定でサービスを起動
docker-compose -f examples/docker-compose.basic.yml up -d
```

### 2. .envファイルを使用した設定（推奨）
```bash
# .envファイルをコピーして編集
cp examples/custom_rules.env .
# custom_rules.envを編集してプロジェクト固有のルールを設定

# サービスを起動
docker-compose -f examples/docker-compose.env-file.yml up -d
```

### 3. カスタムルールファイルからの読み込み
```bash
# ファイル内容を環境変数に読み込み
export REVIEWBOT_LLM_CUSTOM_INSTRUCTIONS="$(cat examples/example_custom_instructions.txt)"

# または大容量ルールを使用
export REVIEWBOT_LLM_CUSTOM_INSTRUCTIONS="$(cat examples/custom_instructions_large.txt)"

# サービスを起動
docker-compose up -d
```

## ⚙️ 設定のカスタマイズ

### バックエンドの選択
```bash
# OpenWebUIを使用
REVIEWBOT_LLM_BACKEND=openwebui

# llamacppを使用
REVIEWBOT_LLM_BACKEND=llamacpp
```

### サーバーURL設定
```bash
# OpenWebUI
REVIEWBOT_LLM_OPENWEBUI_URL=http://host.docker.internal:3000

# llamacpp
REVIEWBOT_LLM_LLAMACPP_URL=http://host.docker.internal:8080
```

### APIキー設定（オプション）
```bash
REVIEWBOT_LLM_OPENWEBUI_API_KEY=your_api_key_here
REVIEWBOT_LLM_LLAMACPP_API_KEY=your_api_key_here
```

## 📝 カスタムルールの作成

1. `example_custom_instructions.txt`をテンプレートとして使用
2. プロジェクト固有の要件に合わせてルールを追加・修正
3. 箇条書き形式で整理された構造を維持
4. 必要に応じて複数のセクションに分割

## 🔧 トラブルシューティング

### よくある問題
- **接続エラー**: `host.docker.internal`がLinuxで動作しない場合は、ホストのIPアドレスを直接指定
- **文字化け**: カスタムルールに日本語を含む場合は、ファイルのエンコーディングをUTF-8に設定
- **環境変数が読み込まれない**: .envファイルのパスと権限を確認

### ログの確認
```bash
# サービスのログを確認
docker-compose logs reviewbot-llm

# リアルタイムでログを監視
docker-compose logs -f reviewbot-llm
```
