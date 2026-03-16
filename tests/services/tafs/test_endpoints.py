import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

pytest.importorskip("bs4")

from app.services.tafs.dependencies import get_active_tafs_session
from app.services.tafs.endpoints import router


class FakeTafsController:
    def __init__(self):
        self.calls = []

    def search_broker(self, mc):
        self.calls.append(("search_broker", mc))
        return {"mc": mc}

    def load_debtor(self, account_id):
        self.calls.append(("load_debtor", account_id))
        return {"account_id": account_id}


def _build_client():
    fake = FakeTafsController()
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_active_tafs_session] = lambda: fake
    return TestClient(app), fake


def test_search_broker_uses_dependency_and_returns_payload():
    client, fake = _build_client()

    response = client.get("/api/tafs/search_broker/12345")

    assert response.status_code == 200
    assert response.json() == {"brokers": {"mc": "12345"}}
    assert fake.calls == [("search_broker", "12345")]


def test_load_debtor_passes_only_account_id_to_controller():
    client, fake = _build_client()

    response = client.get("/api/tafs/load_debtor/abc-1", params={"mc": "ignored"})

    assert response.status_code == 200
    assert response.json() == {"debtor": {"account_id": "abc-1"}}
    assert fake.calls == [("load_debtor", "abc-1")]
