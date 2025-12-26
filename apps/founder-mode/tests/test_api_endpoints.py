from typing import Any, NamedTuple
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from foundermode.api.server import app

client = TestClient(app)


class MockSnapshot(NamedTuple):
    next: tuple[str, ...]
    values: dict[str, Any]


@patch("foundermode.api.server.workflow")
def test_create_run(mock_workflow: MagicMock) -> None:
    """Test creating a new research run."""
    # Payload
    payload = {"idea": "AI for restaurants"}

    response = client.post("/run", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "run_id" in data
    assert data["status"] == "started"
    assert mock_workflow.invoke.called


@patch("foundermode.api.server.workflow")
def test_get_run_status(mock_workflow: MagicMock) -> None:
    """Test getting the status of a run."""
    # Mock snapshot using a real object instead of just MagicMock to avoid FastAPI serialization issues
    mock_workflow.get_state.return_value = MockSnapshot(
        next=("researcher",), values={"next_step": "research", "research_facts": []}
    )

    run_id = "test_run_123"
    response = client.get(f"/run/{run_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["run_id"] == run_id
    assert data["next_node"] == "researcher"


@patch("foundermode.api.server.workflow")
def test_resume_run(mock_workflow: MagicMock) -> None:
    """Test resuming a run."""
    run_id = "test_run_123"

    # Mock behavior
    mock_workflow.invoke.return_value = {"next_step": "research"}

    response = client.post(f"/run/{run_id}/resume")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "resumed"
    assert mock_workflow.invoke.called
