from app.services.eld import dependencies


class FakeReliableApi:
    def __init__(self):
        self.called = 0

    def get_valid_token(self):
        self.called += 1
        return "token-123"


def test_get_eld_api_returns_singleton(monkeypatch):
    dependencies._eld_api_instance = None

    first = dependencies.get_eld_api()
    second = dependencies.get_eld_api()

    assert first is second


def test_get_eld_controller_returns_controller_with_token(monkeypatch):
    fake_api = FakeReliableApi()
    dependencies._eld_api_instance = fake_api

    controller = dependencies.get_eld_controller()

    assert controller.authorization_token == "token-123"
    assert fake_api.called == 1
