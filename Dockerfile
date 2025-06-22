# Dockerfile for ReviewBot LLM Extension
# Extends the official beanbag/reviewbot-base image with LLM capabilities

FROM beanbag/reviewbot-base:latest

# Install the LLM extension dependencies
RUN pip install --no-cache-dir requests

# Copy the extension source code
COPY . /app/reviewbot-llm-extension/

# Install the LLM extension
WORKDIR /app/reviewbot-llm-extension
RUN pip install --no-cache-dir -e .

# Verify the extension is properly installed
RUN python -c "from reviewbot_llm.llm_tool import LLMTool; print('LLM extension installed successfully')"

# Set default environment variables for LLM backends
ENV REVIEWBOT_LLM_BACKEND=openwebui
ENV REVIEWBOT_LLM_OPENWEBUI_URL=http://localhost:3000
ENV REVIEWBOT_LLM_LLAMACPP_URL=http://localhost:8080
ENV REVIEWBOT_LLM_MODEL_NAME=llama2
ENV REVIEWBOT_LLM_MAX_TOKENS=1000

# Set working directory back to default
WORKDIR /

# Use the same entrypoint as the base image
# The base image already sets up ReviewBot worker configuration
