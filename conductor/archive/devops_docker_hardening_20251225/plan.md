# Implementation Plan: devops_docker_hardening_20251225

## Phase 1: Docker Infrastructure Update
- [x] Task: Update `Dockerfile` to use `uv` and install Playwright dependencies.
    - Implement multi-stage build (or robust single-stage) for optimized image.
    - Add `playwright install-deps chromium` and `playwright install chromium`.
    - Set `PATH` to include the container's virtual environment.
- [x] Task: Update `docker-compose.yml` for production-grade configuration.
    - Set `platform: linux/amd64`.
    - Configure volume mapping to exclude host's `.venv`.
    - Ensure environment variable pass-through.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Docker Infrastructure Update' (Protocol in workflow.md)

## Phase 2: Containerized Verification Suite
- [x] Task: Implement `tests/container/test_env.py` (Red).
    - Test for chromium binary availability.
    - Test for basic playwright rendering.
- [x] Task: Implement logic and verify tests pass inside container (Green).
- [x] Task: Implement `tests/container/test_integration.py` for full node execution.
    - Verify `researcher_node` completes successfully in the container.
    - Verify ChromaDB volume persistence.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Containerized Verification Suite' (Protocol in workflow.md)

## Phase 3: Final Validation & Documentation
- [x] Task: Update `README.md` with Docker-first instructions.
- [x] Task: Run full system smoke test via `docker compose run`.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Final Validation & Documentation' (Protocol in workflow.md)
