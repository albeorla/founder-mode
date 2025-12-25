# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# Copy dependency definition files
COPY pyproject.toml uv.lock ./

# 1. Install Python dependencies
ARG INCLUDE_DEV=false
RUN if [ "$INCLUDE_DEV" = "true" ] ; then uv sync --frozen --no-install-project --extra dev ; else uv sync --frozen --no-install-project --no-dev ; fi

# 2. Install Playwright Browsers and OS Dependencies
# We activate the virtual environment to ensure playwright is found
ENV PATH="/app/.venv/bin:$PATH"
RUN playwright install-deps chromium && \
    playwright install chromium

# Copy the project source code
COPY . .

# 3. Install the project itself
RUN if [ "$INCLUDE_DEV" = "true" ] ; then uv sync --frozen --extra dev ; else uv sync --frozen --no-dev ; fi

# Set the entrypoint
# We use 'uv run' to ensure we are in the correct venv context
ENTRYPOINT ["uv", "run", "foundermode"]
CMD ["--help"]
