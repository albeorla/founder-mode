import os


def test_uv_lockfile_exists() -> None:
    """Verify that the uv.lock file has been generated."""
    assert os.path.exists("uv.lock"), "uv.lock file not found. Please run 'uv lock'."
