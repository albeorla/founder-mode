from foundermode.api.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def test_cli_run_success() -> None:
    result = runner.invoke(app, ["run", "Test Idea"])
    assert result.exit_code == 0
    assert "FounderMode" in result.stdout
    assert "Researching: Test Idea" in result.stdout
    assert "Mock Executive Summary" in result.stdout
