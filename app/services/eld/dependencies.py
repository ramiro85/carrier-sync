from app.config import settings
from app.services.eld.driver.controller import ELDDriverController
from app.services.eld.eld_api import ReliableApi

# Shared instance of ReliableApi to maintain session across requests
_eld_api_instance = None


def get_eld_api() -> ReliableApi:
    """
    Get or create the shared ReliableApi instance.
    """
    global _eld_api_instance
    if _eld_api_instance is None:
        _eld_api_instance = ReliableApi()
    return _eld_api_instance


def get_eld_controller() -> ELDDriverController:
    """
    Dependency to get a fresh ELD driver controller instance.
    Ensures authentication before returning the controller.
    Uses dependency injection to allow automatic token refresh.
    """
    # Get the shared API instance
    eld_api = get_eld_api()

    # Get a valid token (will login if needed)
    token = eld_api.get_valid_token()

    if not token:
        raise Exception("Failed to obtain authentication token")

    # Create controller with authenticated token and API reference for refresh
    controller = ELDDriverController(
        base_url=settings.eld_base_url,
        authorization_token=token,
        eld_api=eld_api,  # Pass API instance for token refresh
    )

    return controller
