import os
from datetime import datetime, timezone

# Required settings for app.config at import time.
os.environ.setdefault("SAFER_COOKIE", "test-cookie")
os.environ.setdefault("TAFS_PORTAL_USERNAME", "test-user")
os.environ.setdefault("TAFS_PORTAL_PASSWORD", "test-pass")
os.environ.setdefault("ELD_BASE_URL", "https://eld.example.com")

from app.config import settings
from app.services.googleCloud.dependencies import GoogleServiceAccountApiController
from app.services.googleCloud.schemas import TmsMessage


def test_real_controller_send_message_to_ramirio_gmail():
    controller = GoogleServiceAccountApiController()
    sender = settings.google_workspace_impersonated_user_jobee
    timestamp = datetime.now(timezone.utc).isoformat()
    message = TmsMessage(
        From={sender: "Jobee API Test"},
        To=["ramirez.garcia.ramiro85@gmail.com"],
        Subject=f"[Integration] Jobee Gmail Send Test {timestamp}",
        body="<p>Integration test email from real Google service-account controller.</p>",
    )

    response = controller.send_message(message)

    assert response.success is True
    assert response.data is not None
    assert response.data.get("id")
