import os
from datetime import datetime, timezone

import pytest

pytest.importorskip("googleapiclient")

from app.config import settings
from app.services.googleCloud.dependencies import GoogleServiceAccountApiController
from app.services.googleCloud.schemas import TmsMessage


@pytest.mark.skipif(
    os.getenv("RUN_REAL_INTEGRATION_TESTS", "").lower() != "true",
    reason="Set RUN_REAL_INTEGRATION_TESTS=true to run live Gmail integration tests.",
)
def test_real_controller_send_message():
    controller = GoogleServiceAccountApiController()
    sender = os.getenv(
        "INTEGRATION_TEST_GMAIL_SENDER",
        settings.google_workspace_impersonated_user_account1,
    )
    recipient = os.getenv("INTEGRATION_TEST_GMAIL_RECIPIENT", "recipient@example.net")
    timestamp = datetime.now(timezone.utc).isoformat()
    message = TmsMessage(
        From={sender: "Integration Test Bot"},
        To=[recipient],
        Subject=f"[Integration] Gmail Send Test {timestamp}",
        body="<p>Integration test email from real Google service-account controller.</p>",
    )

    response = controller.send_message(message)

    assert response.success is True
    assert response.data is not None
    assert response.data.get("id")
