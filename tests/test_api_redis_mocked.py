"""Root-level tests for automated checks.

Redis must be mocked (no live Redis).
"""

from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint_with_redis_mock():
    with patch("main.r") as mock_redis:
        mock_redis.ping.return_value = True
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


def test_create_job_pushes_to_redis():
    with patch("main.r") as mock_redis:
        response = client.post("/jobs")
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert mock_redis.lpush.called
        assert mock_redis.hset.called


def test_get_job_missing_returns_error():
    with patch("main.r") as mock_redis:
        mock_redis.hget.return_value = None
        response = client.get("/jobs/does-not-exist")
        assert response.status_code == 200
        assert response.json() == {"error": "not found"}
