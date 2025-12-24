from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from foundermode.api.server import app

client = TestClient(app)


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

    # Mock snapshot
    mock_snapshot = MagicMock()
    mock_snapshot.next = ("researcher",)
    mock_snapshot.values = {"next_step": "research"}
    mock_workflow.get_state.return_value = mock_snapshot

    run_id = "test_run_123"
    response = client.get(f"/run/{run_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["run_id"] == run_id
    assert data["next_node"] == "researcher"
