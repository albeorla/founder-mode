import importlib.util
import os


def test_directories_exist() -> None:
    dirs = [
        "apps/founder-mode/src/foundermode/domain",
        "apps/founder-mode/src/foundermode/graph",
        "apps/founder-mode/src/foundermode/memory",
        "apps/founder-mode/src/foundermode/tools",
        "apps/founder-mode/src/foundermode/api",
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} does not exist"


def test_dependencies_installed() -> None:
    packages = ["langgraph", "langchain_core", "typer", "langsmith"]
    for p in packages:
        assert importlib.util.find_spec(p) is not None, f"Package {p} is not installed"
