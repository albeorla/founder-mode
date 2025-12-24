import os


def test_precommit_config_exists() -> None:
    assert os.path.exists(".pre-commit-config.yaml")


def test_precommit_config_content() -> None:
    if not os.path.exists(".pre-commit-config.yaml"):
        return  # Checked by previous test
    with open(".pre-commit-config.yaml") as f:
        content = f.read()
    assert "repos:" in content
    assert "pre-commit-hooks" in content
    assert "ruff-pre-commit" in content
    assert "mirrors-mypy" in content
