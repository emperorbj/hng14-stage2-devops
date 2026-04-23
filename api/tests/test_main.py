from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


def test_health():
    with patch("main.r") as mock_redis:
        mock_redis.ping.return_value = True
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


def test_create_job():
    with patch("main.r") as mock_redis:
        response = client.post("/jobs")
        data = response.json()
        assert response.status_code == 200
        assert "job_id" in data
        assert mock_redis.lpush.called
        assert mock_redis.hset.called


def test_job_not_found():
    with patch("main.r") as mock_redis:
        mock_redis.hget.return_value = None
        response = client.get("/jobs/123")
        assert response.status_code == 200
        assert response.json() == {"error": "not found"}
