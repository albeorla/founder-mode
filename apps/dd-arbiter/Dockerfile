# DD-Arbiter Development Image
# Pre-installs heavy ML dependencies (~4GB) to avoid repeated downloads

FROM python:3.12-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set up environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_CACHE_DIR=/root/.cache/uv \
    HF_HOME=/root/.cache/huggingface \
    TRANSFORMERS_CACHE=/root/.cache/transformers

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock ./
COPY libs/agentkit ./libs/agentkit
COPY apps/dd-arbiter/pyproject.toml ./apps/dd-arbiter/

# Install dependencies (this layer will be cached)
RUN uv sync --all-extras --dev

# Copy the rest of the code
COPY apps/dd-arbiter ./apps/dd-arbiter

# Set working directory to dd-arbiter
WORKDIR /workspace/apps/dd-arbiter

# Pre-download ML models to cache them in the image
RUN uv run python -c "\
try:\n\
    from transformers import AutoModel, AutoTokenizer;\n\
    print('Downloading DeBERTa-Large-MNLI...');\n\
    AutoTokenizer.from_pretrained('microsoft/deberta-large-mnli');\n\
    AutoModel.from_pretrained('microsoft/deberta-large-mnli');\n\
    print('Models cached successfully');\n\
except Exception as e:\n\
    print(f'Warning: Could not pre-cache models: {e}');\n\
" || true

# Default command
CMD ["uv", "run", "python", "-m", "ddarbiter", "--help"]
