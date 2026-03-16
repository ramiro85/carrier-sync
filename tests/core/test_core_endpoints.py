import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

pytest.importorskip("bs4")

from app.core.core_endpoints import router

client = TestClient(FastAPI())
client.app.include_router(router)


def test_health_returns_healthy_payload():
    response = client.post("/health")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "ok",
        "data": {"status": "healthy"},
    }
