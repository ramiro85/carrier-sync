from fastapi import HTTPException

from app.services.googleCloud.dependencies import GoogleServiceAccountApiController


def test_resolve_subject_uses_username_for_supported_domain():
    controller = GoogleServiceAccountApiController()

    subject = controller._resolve_subject("agent@jobeeexpress.com", "noreply@jobeeexpress.com")

    assert subject == "agent@jobeeexpress.com"


def test_resolve_subject_uses_default_when_username_missing():
    controller = GoogleServiceAccountApiController()

    subject = controller._resolve_subject(None, "noreply@jobeeexpress.com")

    assert subject == "noreply@jobeeexpress.com"


def test_resolve_subject_rejects_external_domain():
    controller = GoogleServiceAccountApiController()

    try:
        controller._resolve_subject("person@gmail.com", "noreply@jobeeexpress.com")
        assert False, "Expected HTTPException for unsupported impersonation domain"
    except HTTPException as exc:
        assert exc.status_code == 400
        assert "Workspace delegation" in exc.detail
