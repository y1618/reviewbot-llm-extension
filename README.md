# ReviewBot LLM Extension

A ReviewBot extension that performs automated code reviews using local Large Language Models (LLMs) through OpenWebUI or llamacpp.

## Features

- Support for both OpenWebUI HTTP API and llamacpp local execution
- Configurable backend selection
- Comprehensive code review prompts
- JSON-structured review responses
- Support for multiple programming languages (Python, JavaScript, TypeScript, Java, C/C++, Go, Rust, Ruby, PHP)
- Configurable temperature and token limits
- Error handling for network issues and model loading failures

## Installation

### Docker Installation (Recommended)

The easiest way to use the ReviewBot LLM extension is with Docker, extending the official `beanbag/reviewbot-base` image:

```bash
# Clone the repository
git clone https://github.com/y1618/reviewbot-llm-extension.git
cd reviewbot-llm-extension

# Build the Docker image
docker build -t reviewbot-llm .

# Run with docker-compose (includes OpenWebUI and Ollama)
docker-compose up -d
```

### Manual Installation

1. Clone this repository:
```bash
git clone https://github.com/y1618/reviewbot-llm-extension.git
cd reviewbot-llm-extension
```

2. Install the extension:
```bash
pip install -e .
```

## Configuration

Configure the tool in Review Board with the following options:

### Backend Selection
- **Backend**: Choose between 'openwebui' or 'llamacpp'

### OpenWebUI Configuration
- **OpenWebUI URL**: Server URL (default: http://localhost:3000)
- **OpenWebUI API Key**: Optional API key for authentication
- **Model Name**: Model name available in your OpenWebUI instance

### llamacpp Configuration
- **Model Name**: Full path to your GGUF model file (e.g., `/path/to/model.gguf`)

### General Settings
- **Max Tokens**: Maximum tokens for LLM response (default: 1000)
- **Temperature**: Temperature for LLM response (0.0-1.0, lower = more focused, default: 0.1)

## Docker Configuration

### Basic Setup (External OpenWebUI/Ollama)

The default Docker setup includes only:

- **reviewbot-llm**: Main ReviewBot container with LLM extension
- **redis**: Message broker for ReviewBot

This setup assumes you're running OpenWebUI and Ollama separately on your host system.

### Environment Variables

Configure the LLM extension using environment variables:

```bash
# Backend selection
REVIEWBOT_LLM_BACKEND=openwebui  # or 'llamacpp'

# OpenWebUI configuration (external)
REVIEWBOT_LLM_OPENWEBUI_URL=http://host.docker.internal:3000
REVIEWBOT_LLM_MODEL_NAME=llama2
REVIEWBOT_LLM_MAX_TOKENS=1000
REVIEWBOT_LLM_TEMPERATURE=0.1
```

### Deployment Options

#### Option 1: External OpenWebUI/Ollama (Recommended)
```bash
# Start your OpenWebUI and Ollama separately
# Then run ReviewBot LLM extension
docker-compose up -d
```

#### Option 2: Full Stack (All-in-One)
Uncomment the OpenWebUI and Ollama services in docker-compose.yml:
```bash
# Edit docker-compose.yml to uncomment OpenWebUI/Ollama services
docker-compose up -d
```

### Service Access

- **Redis**: Message broker at localhost:6379
- **OpenWebUI**: Your external instance (typically http://localhost:3000)
- **Ollama**: Your external instance (typically http://localhost:11434)

## Supported Environments

- **SCM**: Git, Subversion, Mercurial (SCM-independent design)
- **Languages**: Python, JavaScript, TypeScript, Java, C/C++, Go, Rust, Ruby, PHP
- **Frameworks**: ROS2, standard Python projects
- **Deployment**: Docker, bare metal, cloud environments

## Requirements

- ReviewBot
- requests (for OpenWebUI integration)
- llama-cpp-python (for local llamacpp execution)
- Docker and docker-compose (for containerized deployment)

## Usage

1. Install and configure the extension in Review Board
2. Add the LLM Code Review tool to your review requests
3. The tool will automatically analyze code files and provide review comments
4. Comments will appear as regular review comments in Review Board

## Supported File Types

- Python (*.py)
- JavaScript (*.js)
- TypeScript (*.ts)
- Java (*.java)
- C/C++ (*.c, *.cpp, *.h)
- Go (*.go)
- Rust (*.rs)
- Ruby (*.rb)
- PHP (*.php)

## Backend Details

### OpenWebUI
- Uses HTTP API calls to your OpenWebUI instance
- Supports both OpenAI-compatible (`/v1/chat/completions`) and native (`/api/chat`) endpoints
- Automatic fallback between endpoints
- Optional API key authentication

### llamacpp
- Direct local execution using llama-cpp-python
- Model caching for performance
- Configurable context size and threading
- Supports GGUF model format

## Error Handling

The extension includes comprehensive error handling for:
- Network connectivity issues (OpenWebUI)
- Model loading failures (llamacpp)
- Invalid JSON responses
- File encoding issues
- API authentication errors

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the ReviewBot documentation
- Verify your OpenWebUI or llamacpp setup
