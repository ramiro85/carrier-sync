import os
import sys
from pathlib import Path


def pytest_configure() -> None:
    """Set safe defaults so app settings can load during tests."""
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    defaults = {
        "SAFER_COOKIE": "test-cookie",
        "TAFS_PORTAL_USERNAME": "test-user",
        "TAFS_PORTAL_PASSWORD": "test-pass",
        "TAFS_PORTAL_URL": "https://tafs.example.com",
        "SAFER_BASE_URL": "https://safer.example.com",
        "ELD_BASE_URL": "https://eld.example.com/api",
        "ELD_USERNAME": "eld-user@example.com",
        "ELD_PASSWORD": "eld-password",
        "ELD_ORIGIN": "https://eld.example.com",
        "GOOGLE_WORKSPACE_DOMAIN_ACCOUNT1": "example.com",
        "GOOGLE_WORKSPACE_DOMAIN_ACCOUNT2": "example.org",
        "GOOGLE_WORKSPACE_IMPERSONATED_USER_ACCOUNT1": "mailer@example.com",
        "GOOGLE_WORKSPACE_IMPERSONATED_USER_ACCOUNT2": "mailer@example.org",
        "GOOGLE_SERVICE_ACCOUNT_FILE_ACCOUNT1": "service-account-1.json",
        "GOOGLE_SERVICE_ACCOUNT_FILE_ACCOUNT2": "service-account-2.json",
    }

    for key, value in defaults.items():
        os.environ.setdefault(key, value)
