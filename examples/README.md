# ReviewBot LLM Extension - 使用例

このフォルダには、ReviewBot LLM拡張機能の設定例とサンプルファイルが含まれています。

## 📁 ファイル構成

### Docker Compose設定例
- `docker-compose.basic.yml` - 基本的な設定例（環境変数を直接指定）
- `docker-compose.env-file.yml` - .envファイルを使用した設定例（推奨）
- `docker-compose.multi-instance.yml` - 複数インスタンス設定例（異なるモデル・設定）
- `docker-compose.scalable.yml` - スケーラブルな複数インスタンス設定例
- `custom_rules.env` - カスタムルール用の.envファイル例

### 複数インスタンス設定ファイル
- `multi-instance.env` - 複数インスタンス用環境変数例
- `python-config.env` - Python専用インスタンス設定
- `cpp-config.env` - C++専用インスタンス設定
- `ros2-config.env` - ROS2専用インスタンス設定

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

### 3. 複数インスタンスの起動（異なるモデル・設定）
```bash
# 複数のレビューボットを同時起動
docker-compose -f examples/docker-compose.multi-instance.yml up -d

# 特定のインスタンスのみ起動
docker-compose -f examples/docker-compose.multi-instance.yml up -d reviewbot-llm-python
docker-compose -f examples/docker-compose.multi-instance.yml up -d reviewbot-llm-cpp
```

### 4. スケーラブルな複数インスタンス設定
```bash
# 設定ファイルをコピーして編集
cp examples/python-config.env .
cp examples/cpp-config.env .
cp examples/ros2-config.env .

# 各設定ファイルを編集してカスタマイズ
# サービスを起動
docker-compose -f examples/docker-compose.scalable.yml up -d
```

### 5. カスタムルールファイルからの読み込み
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

## 🔧 複数インスタンス設定のポイント

### インスタンス設計例
- **Python専用**: GPT-4 + PEP 8重視 + セキュリティチェック
- **C++専用**: Code Llama + RAII + Modern C++標準
- **ROS2専用**: Llama2 + ノード設計 + QoS設定
- **汎用**: Mixtral + 総合的なコード品質チェック

### Review Board設定
各インスタンスは異なるユーザー名でReview Boardに接続：
- `reviewbot-python`
- `reviewbot-cpp` 
- `reviewbot-ros2`
- `reviewbot-general`

### リソース管理
```bash
# 特定のインスタンスのみ停止
docker-compose -f examples/docker-compose.multi-instance.yml stop reviewbot-llm-python

# 全インスタンスの状態確認
docker-compose -f examples/docker-compose.multi-instance.yml ps

# リソース使用量確認
docker stats
```

## 🔧 トラブルシューティング

### よくある問題
- **接続エラー**: `host.docker.internal`がLinuxで動作しない場合は、ホストのIPアドレスを直接指定
- **文字化け**: カスタムルールに日本語を含む場合は、ファイルのエンコーディングをUTF-8に設定
- **環境変数が読み込まれない**: .envファイルのパスと権限を確認
- **ポート競合**: 複数のllamacppサーバーを使用する場合は、異なるポートを指定

### ログの確認
```bash
# 特定のサービスのログを確認
docker-compose logs reviewbot-llm-python
docker-compose logs reviewbot-llm-cpp

# 全サービスのログを確認
docker-compose logs

# リアルタイムでログを監視
docker-compose logs -f reviewbot-llm-python
```
