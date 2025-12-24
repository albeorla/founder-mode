import os

import pytest


def test_pyproject_toml_exists() -> None:
    assert os.path.exists("pyproject.toml")


def test_pyproject_toml_valid() -> None:
    if not os.path.exists("pyproject.toml"):
        pytest.fail("pyproject.toml not found")
    with open("pyproject.toml") as f:
        content = f.read()
    assert "[project]" in content
