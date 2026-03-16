import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

pytest.importorskip("googleapiclient")

from app.services.googleCloud.dependencies import get_gmail_service_account_controller
from app.services.googleCloud.endpoints import router


class FakeGmailController:
    def __init__(self):
        self.calls = []

    def send_message(self, message):
        self.calls.append(("send_message", message))
        return {"success": True, "message": "ok", "data": {"id": "mock-send-id"}}

    def search_thread(self, query_subject, username, from_email):
        self.calls.append(
            (
                "search_thread",
                {
                    "query_subject": query_subject,
                    "username": username,
                    "from_email": from_email,
                },
            )
        )
        return {"success": True, "message": "ok", "data": {"thread_id": "thread-1"}}

    def find_messages(self, query_subject, username, from_email):
        self.calls.append(
            (
                "find_messages",
                {
                    "query_subject": query_subject,
                    "username": username,
                    "from_email": from_email,
                },
            )
        )
        return {"success": True, "message": "ok", "data": [{"id": "msg-1"}]}

    def save_attachment(self, thread_id, filename, username, save_dir):
        self.calls.append(
            (
                "save_attachment",
                {
                    "thread_id": thread_id,
                    "filename": filename,
                    "username": username,
                    "save_dir": save_dir,
                },
            )
        )
        return {"success": True, "message": "ok", "data": {}}

    def find_contacts(self, query_subject, username, from_email):
        self.calls.append(
            (
                "find_contacts",
                {
                    "query_subject": query_subject,
                    "username": username,
                    "from_email": from_email,
                },
            )
        )
        return {"success": True, "message": "ok", "data": [{"email": from_email}]}


def _build_client():
    fake_controller = FakeGmailController()
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_gmail_service_account_controller] = (
        lambda: fake_controller
    )
    return TestClient(app), fake_controller


def test_send_message_uses_dependency_and_sends_to_receipt_email():
    client, fake_controller = _build_client()
    response = client.post(
        "/api/gmail/send",
        json={
            "From": {"noreply@example.com": "Dispatch Bot"},
            "To": ["recipient@example.net"],
            "Subject": "Driver information",
            "body": "<p>Driver payload</p>",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    method, message = fake_controller.calls[0]
    assert method == "send_message"
    assert "recipient@example.net" in message.To
    assert message.username == "noreply@example.com"


def test_search_thread_forwards_query_fields():
    client, fake_controller = _build_client()
    response = client.post(
        "/api/gmail/search_thread",
        json={
            "subject": "Driver information",
            "username": "noreply@example.com",
            "from_email": "recipient@example.net",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    method, payload = fake_controller.calls[0]
    assert method == "search_thread"
    assert payload["query_subject"] == "Driver information"
    assert payload["username"] == "noreply@example.com"
    assert payload["from_email"] == "recipient@example.net"


def test_find_messages_forwards_query_fields():
    client, fake_controller = _build_client()
    response = client.post(
        "/api/gmail/find_messages",
        json={
            "subject": "Driver information",
            "username": "noreply@example.com",
            "from_email": "recipient@example.net",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    method, payload = fake_controller.calls[0]
    assert method == "find_messages"
    assert payload["query_subject"] == "Driver information"
    assert payload["username"] == "noreply@example.com"
    assert payload["from_email"] == "recipient@example.net"


def test_get_attachment_forwards_query_fields():
    client, fake_controller = _build_client()
    response = client.post(
        "/api/gmail/getAttachment",
        json={
            "thread_id": "thread-123",
            "filename": "driver.pdf",
            "username": "noreply@example.com",
            "save_dir": "docs",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    method, payload = fake_controller.calls[0]
    assert method == "save_attachment"
    assert payload["thread_id"] == "thread-123"
    assert payload["filename"] == "driver.pdf"
    assert payload["username"] == "noreply@example.com"
    assert payload["save_dir"] == "docs"


def test_get_contacts_forwards_query_fields():
    client, fake_controller = _build_client()
    response = client.post(
        "/api/gmail/get_contacts",
        json={
            "subject": "Driver information",
            "username": "noreply@example.com",
            "from_email": "recipient@example.net",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    method, payload = fake_controller.calls[0]
    assert method == "find_contacts"
    assert payload["query_subject"] == "Driver information"
    assert payload["username"] == "noreply@example.com"
    assert payload["from_email"] == "recipient@example.net"
