import pytest

def test_import_foundermode():
    try:
        import foundermode
    except ImportError:
        pytest.fail("Could not import foundermode package")
