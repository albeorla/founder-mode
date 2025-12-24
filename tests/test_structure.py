import importlib.util

import pytest


def test_import_foundermode() -> None:
    if not importlib.util.find_spec("foundermode"):
        pytest.fail("Could not import foundermode package")
