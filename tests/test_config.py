import os
import pytest

def test_pyproject_toml_exists():
    assert os.path.exists("pyproject.toml")

def test_pyproject_toml_valid():
    if not os.path.exists("pyproject.toml"):
        pytest.fail("pyproject.toml not found")
    with open("pyproject.toml", "r") as f:
        content = f.read()
    assert "[project]" in content
