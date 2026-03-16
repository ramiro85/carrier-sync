from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Google Cloud Service Configuration
    attachment_path: str = Field(default="", alias="ATTACHMENTS_PATH")
    gcp_project_id: str = Field(default="", alias="GCP_PROJECT_ID")
    gcp_region: str = Field(default="us-central1", alias="GCP_REGION")
    google_service_account_file_account1: str = Field(
        default="",
        alias="GOOGLE_SERVICE_ACCOUNT_FILE_ACCOUNT1",
    )
    google_service_account_file_account2: str = Field(
        default="",
        alias="GOOGLE_SERVICE_ACCOUNT_FILE_ACCOUNT2",
    )
    google_workspace_impersonated_user_account1: str = Field(
        default="",
        alias="GOOGLE_WORKSPACE_IMPERSONATED_USER_ACCOUNT1",
    )
    google_workspace_impersonated_user_account2: str = Field(
        default="",
        alias="GOOGLE_WORKSPACE_IMPERSONATED_USER_ACCOUNT2",
    )
    google_workspace_domain_account1: str = Field(
        default="",
        alias="GOOGLE_WORKSPACE_DOMAIN_ACCOUNT1",
    )
    google_workspace_domain_account2: str = Field(
        default="",
        alias="GOOGLE_WORKSPACE_DOMAIN_ACCOUNT2",
    )

    # SAFER Service Configuration
    safer_base_url: str = Field(
        default="https://safer.example.com", alias="SAFER_BASE_URL"
    )
    safer_base_cookie: str = Field(alias="SAFER_COOKIE")

    # TAFS Service Configuration
    tafs_portal_url: str = Field(
        default="https://tafs.example.com", alias="TAFS_PORTAL_URL"
    )
    tafs_portal_username: str = Field(alias="TAFS_PORTAL_USERNAME")
    tafs_portal_password: str = Field(alias="TAFS_PORTAL_PASSWORD")

    # ELD Service Configuration
    eld_base_url: str = Field(alias="ELD_BASE_URL")
    eld_username: str = Field(alias="ELD_USERNAME")
    eld_password: str = Field(alias="ELD_PASSWORD")
    eld_origin: str = Field(alias="ELD_ORIGIN")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )


settings = Settings()
