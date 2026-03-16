import json
import requests

from app.config import settings
from app.services.tafs.customHttpAdapter import get_legacy_session


class ReliableApi:
    headers_base = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://eld.hgrs.us",
        "priority": "u=1, i",
        "referer": "https://eld.hgrs.us/",
        "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    }

    violations = {
        "M30_REST_BREAK": "30 Minute Rest Break",
        "H14_DUTY_LIMIT": "14-Hour On Duty Limit",
        "H11_DRIVING": "11-Hour Driving Limit",
        "US_70_8": "USA 70/8",
        "DR_IND_PC": "Personal Use",
    }

    eventClasses = {
        "DS_D": "success",
        "VIOL": "danger",
        "DR_IND_PC": "secondary",
        "DS_OFF": "secondary",
        "DS_ON": "success",
        "DS_SB": "secondary",
        "DS_PC": "secondary",
        "DS_YM": "secondary",
        "DS_WT": "secondary",
    }

    auth_token = None
    is_auth = False
    authentication_url = "https://backend.apexhos.com/authentication"

    def __init__(self):
        self.auth_token = None
        self.is_auth = False

    def login(self, force=False):
        """
        Authenticate with the ELD API and obtain an access token.

        Args:
            force: Force re-authentication even if already authenticated

        Returns:
            dict: Response containing authentication token and user information
        """
        if self.is_auth and not force and self.auth_token:
            print("Already authenticated, using existing token")
            return {"accessToken": self.auth_token}

        payload = {
            "strategy": "local",
            "email": "vanessa@jobeeexpress.com",
            "password": "1234567899",
            "company": None,
            "rCode": "highest",
            "otp": None,
            "action": None,
            "twoFaIsEnabled": False,
            "browserFingerPrint": None
        }

        try:
            print("Attempting to authenticate with ELD API...")
            response = requests.post(
                self.authentication_url,
                headers=self.headers_base,
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()

            auth_data = response.json()

            # Store the authentication token
            if "accessToken" in auth_data:
                self.auth_token = auth_data["accessToken"]
                # Update headers with the new token
                self.headers_base["authorization"] = self.auth_token
                self.is_auth = True
                print(f"✓ Successfully authenticated. Token obtained.")
            else:
                raise Exception("No accessToken in response")

            return auth_data

        except requests.exceptions.RequestException as e:
            self.is_auth = False
            self.auth_token = None
            print(f"✗ Login failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            raise Exception(f"Authentication failed: {str(e)}")

    def refresh_token(self):
        """
        Refresh the authentication token by logging in again.

        Returns:
            str: New authentication token
        """
        print("🔄 Refreshing authentication token...")
        self.login(force=True)
        return self.auth_token

    def is_logged(self, carrier=None):
        """
        Check if the current session is authenticated.

        Args:
            carrier: Optional carrier parameter

        Returns:
            bool: True if authenticated, False otherwise
        """
        # If we don't have a token, we're not logged in
        if not self.auth_token:
            print("No token available, attempting login...")
            try:
                self.login()
                return self.is_auth
            except Exception as e:
                print(f"Login attempt failed: {str(e)}")
                return False

        # Verify token is still valid by making a test request
        url = f"https://backend.apexhos.com/maintenance_reminders"

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "authorization": self.auth_token,
            "Content-Type": "application/json",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            'If-None-Match': 'W/"2594a-ZblHutHTZYxIqRMZGJrBLDH++9I"',
        }

        try:
            response = get_legacy_session().get(
                url, headers=headers, allow_redirects=True, timeout=30
            )

            if response is not None and response.status_code == 401:
                print("Token expired (401), refreshing...")
                self.is_auth = False
                self.login(force=True)
            elif response is not None and response.status_code == 403:
                print("Token forbidden (403), refreshing...")
                self.is_auth = False
                self.login(force=True)
            else:
                self.is_auth = True

        except requests.exceptions.RequestException as e:
            print(f"Token validation failed: {str(e)}, attempting refresh...")
            self.is_auth = False
            try:
                self.login(force=True)
            except Exception:
                pass

        return self.is_auth

    def get_valid_token(self):
        """
        Get a valid authentication token, refreshing if necessary.

        Returns:
            str: Valid authentication token
        """
        if not self.is_auth or not self.auth_token:
            self.login(force=True)
        return self.auth_token