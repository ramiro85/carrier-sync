from fastapi import HTTPException, status
from google.auth.exceptions import RefreshError
from google.oauth2 import service_account
from googleapiclient.discovery import build
from pathlib import Path

from app.config import settings
from app.services.googleCloud.controller import GoogleApiController


class GoogleServiceAccountApiController(GoogleApiController):
    SUPPORTED_WORKSPACE_DOMAINS = {"jobeeexpress.com", "bwheelstransport.com"}
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/gmail.send",
    ]

    @staticmethod
    def _get_domain(email: str | None) -> str:
        if not email or "@" not in email:
            return ""
        return email.split("@", 1)[1].lower()

    def _resolve_account(self, username: str | None) -> tuple[str, str]:
        domain = self._get_domain(username)
        if domain == "bwheelstransport.com":
            return (
                settings.google_service_account_file_bwt,
                settings.google_workspace_impersonated_user_bwt,
            )
        return (
            settings.google_service_account_file_jobee,
            settings.google_workspace_impersonated_user_jobee,
        )

    @staticmethod
    def _resolve_service_account_file(path: str) -> str:
        candidate = Path(path)
        if candidate.exists():
            return str(candidate)
        return path

    def _resolve_subject(self, username: str | None, default_impersonated_user: str) -> str:
        if username:
            domain = self._get_domain(username)
            if domain not in self.SUPPORTED_WORKSPACE_DOMAINS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Invalid Gmail username for Workspace delegation. "
                        f"Use a user in one of: {', '.join(sorted(self.SUPPORTED_WORKSPACE_DOMAINS))}."
                    ),
                )
            return username
        return default_impersonated_user

    def authorize(self, username: str | None):
        service_account_file, default_impersonated_user = self._resolve_account(username)
        service_account_file = self._resolve_service_account_file(service_account_file)
        subject = self._resolve_subject(username, default_impersonated_user)
        # Log the identity before making the request
        try:
            creds = service_account.Credentials.from_service_account_file(
                service_account_file,
                scopes=self.SCOPES,
                subject=subject,
            )
            self.creds = creds
            self.service = build("gmail", "v1", credentials=self.creds)
            self.logged = True
        except FileNotFoundError as exc:
            self.logged = False
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Service account file not found: {service_account_file}",
            ) from exc
        except RefreshError as exc:
            self.logged = False
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=(
                    "Service account authentication failed. Verify Google Workspace "
                    "Domain-Wide Delegation and authorized Gmail scopes. "
                    f"service_account_file={service_account_file}, subject={subject}"
                ),
            ) from exc


gmail_service_account_api = GoogleServiceAccountApiController()


def get_gmail_service_account_controller() -> GoogleApiController:
    return gmail_service_account_api
