import os


def test_ci_workflow_exists() -> None:
    assert os.path.exists(".github/workflows/ci.yml")


def test_ci_workflow_content() -> None:
    if not os.path.exists(".github/workflows/ci.yml"):
        return
    with open(".github/workflows/ci.yml") as f:
        content = f.read()
    assert "name: CI" in content
    assert "jobs:" in content
    assert "quality:" in content
    assert "test:" in content
    assert "uv run ruff check" in content
    assert "uv run pytest" in content
