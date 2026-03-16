import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

pytest.importorskip("bs4")

from app.services.safer.endpoints import router

client = TestClient(FastAPI())
client.app.include_router(router)


def test_search_company_returns_controller_payload(monkeypatch):
    expected = {"founded": True, "mc_number": "12345"}

    monkeypatch.setattr(
        "app.services.safer.endpoints.check_company", lambda *_: expected
    )

    response = client.get("/api/safer/search/MC_MX/12345")

    assert response.status_code == 200
    assert response.json() == expected
