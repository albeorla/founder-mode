# Track Spec: devops_docker_hardening_20251225

## Overview
This track addresses the "Critical Blocker" where the current slim Docker image lacks the OS-level libraries and browser binaries required for Playwright. By hardening the Docker infrastructure, we ensure that the "Deep Research" capabilities are fully functional in any containerized environment (local or cloud).

## Functional Requirements
- **Dockerfile Modernization:**
    - Update to use `ghcr.io/astral-sh/uv` for high-speed, deterministic builds.
    - Implement a robust build process that installs Playwright OS dependencies (`playwright install-deps`).
    - Explicitly install the Chromium browser binary within the container.
    - Ensure the environment path is correctly configured to use the internal virtual environment.
- **Docker Compose Optimization:**
    - Configure `platform: linux/amd64` for broad compatibility.
    - Implement volume mapping that excludes the host's `.venv` to prevent binary conflicts between macOS/Windows and the Linux container.
    - Ensure all necessary environment variables are passed through.
- **Container-Internal Verification Suite:**
    - Develop a `pytest` suite designed to run inside the container to verify:
        - `chromium` binary accessibility.
        - Successful browser rendering and text extraction.
        - Error-free execution of the `researcher_node`.
        - Persistence of ChromaDB data across container restarts.

## Acceptance Criteria
- `docker compose build` completes successfully without errors.
- `docker compose run --rm app pytest tests/container` (or similar) passes all tests, proving the environment is healthy.
- A full research run (e.g., `foundermode run "Stripe Pricing"`) succeeds inside the container without "Playwright not found" or "Shared object" errors.

## Out of Scope
- Implementing the web UI/Streaming API (reserved for Track 5).
- Setting up CI/CD pipelines for automated deployment to specific cloud providers (e.g., Railway, Render).
