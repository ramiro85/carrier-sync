from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    #Google Cloud Service Configuration
    gcp_project_id: str = Field(default="", alias="GCP_PROJECT_ID")
    gcp_region: str = Field(default="us-central1", alias="GCP_REGION")
    google_service_account_file_jobee: str = Field(
        default="app/services/googleCloud/service-account-jobee.json",
        alias="GOOGLE_SERVICE_ACCOUNT_FILE_JOBEE",
    )
    google_service_account_file_bwt: str = Field(
        default="app/services/googleCloud/service-account-bwt.json",
        alias="GOOGLE_SERVICE_ACCOUNT_FILE_BWT",
    )
    google_workspace_impersonated_user_jobee: str = Field(
        default="noreply@jobeeexpress.com",
        alias="GOOGLE_WORKSPACE_IMPERSONATED_USER_JOBEE",
    )
    google_workspace_impersonated_user_bwt: str = Field(
        default="noreply@bwheelstransport.com",
        alias="GOOGLE_WORKSPACE_IMPERSONATED_USER_BWT",
    )

    #SAFER Service Configuration
    safer_base_url: str = Field(default="https://safer.fmcsa.dot.gov", alias="SAFER_BASE_URL")
    safer_base_cookie: str = Field(alias="SAFER_COOKIE")

    #TAFS Service Configuration
    tafs_portal_url: str = Field(default="https://safer.fmcsa.dot.gov", alias="TAFS_PORTAL_URL")
    tafs_portal_username: str = Field(alias="TAFS_PORTAL_USERNAME")
    tafs_portal_password: str = Field(alias="TAFS_PORTAL_PASSWORD")

    # ELD Service Configuration
    eld_base_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )
settings = Settings()
