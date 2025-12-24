import os
import importlib.util

def test_directories_exist() -> None:
    dirs = [
        "src/foundermode/domain",
        "src/foundermode/graph",
        "src/foundermode/memory",
        "src/foundermode/tools",
        "src/foundermode/api",
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} does not exist"

def test_dependencies_installed() -> None:
    packages = ["langgraph", "langchain_core", "typer", "langsmith"]
    for p in packages:
        assert importlib.util.find_spec(p) is not None, f"Package {p} is not installed"
