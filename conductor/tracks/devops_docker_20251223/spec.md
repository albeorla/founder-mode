# Specification: DevOps: Docker & CI/CD

## Context
To ensure reproducibility and deployment readiness, we need to containerize the FounderMode application. We will use Docker to package the application and update our GitHub Actions pipeline to build and push this image.

## Requirements

### 1. Dockerfile
- **Base Image:** `python:3.12-slim`
- **Builder Pattern:** Use a multi-stage build or `uv`'s optimized Docker pattern to keep the image small.
- **Dependencies:** Install `uv` and use it to install project dependencies from `pyproject.toml` and `uv.lock`.
- **Source:** Copy `src` code into the container.
- **Entrypoint:** Default to the CLI (`foundermode`), but allow overriding.

### 2. Docker Compose (Optional but recommended)
- Create a `docker-compose.yml` to easily run the app with environment variables from `.env`.

### 3. CI/CD Update (`.github/workflows/ci.yml`)
- Add a job to **Build** the Docker image.
- (Optional for now, but good practice) Add a job to **Push** to GitHub Container Registry (GHCR) on `main` branch.

## Acceptance Criteria
- [ ] `docker build -t foundermode .` succeeds.
- [ ] `docker run --rm foundermode run "Test"` runs the CLI inside the container successfully.
- [ ] GitHub Actions workflow passes the build step.
