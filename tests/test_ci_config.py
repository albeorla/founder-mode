import os


def test_ci_workflow_exists():
    assert os.path.exists(".github/workflows/ci.yml")

def test_ci_workflow_content():
    if not os.path.exists(".github/workflows/ci.yml"):
        return
    with open(".github/workflows/ci.yml") as f:
        content = f.read()
    assert "name: CI" in content
    assert "jobs:" in content
    assert "quality:" in content
    assert "test:" in content
    assert "ruff check" in content
    assert "pytest" in content
