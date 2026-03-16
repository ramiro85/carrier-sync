import requests
import json
import time
from typing import Optional, Dict, Any
from app.services.eld.driver.schemas import DriverCreateRequest, DriverUpdateRequest, DriverResponse


class ELDDriverController:
    def __init__(self, base_url: str, authorization_token: str = None, eld_api=None):
        self.base_url = base_url
        self.authorization_token = authorization_token
        self.eld_api = eld_api  # Keep reference to API for token refresh
        self.headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.authorization_token,
            'content-type': 'application/json',
            'origin': 'https://eld.hgrs.us',
            'priority': 'u=1, i',
            'referer': 'https://eld.hgrs.us/',
            'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
        }

    def _refresh_token(self):
        """Refresh the authentication token."""
        if self.eld_api:
            print("🔄 Refreshing token via ELD API...")
            new_token = self.eld_api.refresh_token()
            self.update_authorization_token(new_token)
            print(f"✓ Token refreshed: {new_token[:50]}...")
            return new_token
        return None

    def _make_request(self, method: str, url: str, **kwargs):
        """
        Make an HTTP request with automatic token refresh on 403 errors.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            url: Request URL
            **kwargs: Additional arguments to pass to requests

        Returns:
            Response object
        """
        print(f"\n📡 Making {method} request to: {url}")
        print(f"   Authorization header: {self.headers.get('authorization', 'N/A')[:50]}...")

        # First attempt
        response = requests.request(method, url, headers=self.headers, **kwargs)
        print(f"   Response Status: {response.status_code}")

        # If we get a 403, try refreshing the token and retry once
        if response.status_code == 403 and self.eld_api:
            print("⚠ Got 403 Forbidden, refreshing token and retrying...")
            print(f"   Response Body: {response.text[:200]}")

            self._refresh_token()

            print(f"   Retrying with new token: {self.headers.get('authorization', 'N/A')[:50]}...")
            # Retry with new token
            response = requests.request(method, url, headers=self.headers, **kwargs)
            print(f"   Retry Response Status: {response.status_code}")

            if response.status_code == 403:
                print(f"✗ Still getting 403 after token refresh!")
                print(f"   Response Body: {response.text[:500]}")

        response.raise_for_status()
        return response

    def update_authorization_token(self, token: str):
        """
        Update the authorization token and refresh headers.

        Args:
            token: New authorization token
        """
        self.authorization_token = token
        self.headers['authorization'] = token
        print(f"✓ Authorization token updated in headers")

    def create_driver(self, driver_id: str, driver_data: DriverCreateRequest) -> Dict[str, Any]:
        """
        Create a new driver in the ELD system.

        Args:
            driver_id: Unique identifier for the driver (e.g., "User:ebIdZ-83s")
            driver_data: Driver information

        Returns:
            Response data from the API
        """
        url = f"{self.base_url}/drivers/{driver_id}"
        url += "?$client[ignoreRev]=true&$client[createIfNotExist]=true&$client[useServerAuditTime]=true"

        current_time = int(time.time() * 1000)

        payload = driver_data.model_dump()
        payload['_id'] = driver_id
        payload['type'] = {'id': 'User'}
        payload['createdAt'] = current_time
        payload['stime'] = current_time
        payload['dSTime'] = -1

        try:
            response = self._make_request('PUT', url, data=json.dumps(payload))
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Failed to create driver: {str(e)}")

    def get_driver(self, driver_id: str) -> Dict[str, Any]:
        """
        Retrieve driver information by ID.

        Args:
            driver_id: Unique identifier for the driver

        Returns:
            Driver information
        """
        url = f"{self.base_url}/drivers/{driver_id}"

        try:
            response = self._make_request('GET', url)
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Failed to get driver: {str(e)}")

    def update_driver(self, driver_id: str, driver_data: DriverUpdateRequest, rev: Optional[str] = None) -> Dict[
        str, Any]:
        """
        Update an existing driver.

        Args:
            driver_id: Unique identifier for the driver
            driver_data: Updated driver information
            rev: Document revision (if known)

        Returns:
            Response data from the API
        """
        url = f"{self.base_url}/drivers/{driver_id}"

        if rev:
            url += f"?rev={rev}"
        else:
            url += "?$client[ignoreRev]=true"

        url += "&$client[useServerAuditTime]=true"

        payload = driver_data.model_dump(exclude_none=True)
        payload['_id'] = driver_id
        print(f"📝 Update Driver Payload: {json.dumps(payload, indent=2)}")

        try:
            response = self._make_request('PUT', url, data=json.dumps(payload))
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Failed to update driver: {str(e)}")

    def delete_driver(self, driver_id: str, rev: Optional[str] = None) -> Dict[str, Any]:
        """
        Delete (deactivate) a driver.

        Args:
            driver_id: Unique identifier for the driver
            rev: Document revision (if known)

        Returns:
            Response data from the API
        """
        url = f"{self.base_url}/drivers/{driver_id}"

        if rev:
            url += f"?rev={rev}"

        try:
            response = self._make_request('DELETE', url)
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Failed to delete driver: {str(e)}")

    def list_drivers(self, company_id: str, limit: int = 100, skip: int = 0) -> Dict[str, Any]:
        """
        List all drivers for a company.

        Args:
            company_id: Company identifier
            limit: Maximum number of drivers to return
            skip: Number of drivers to skip (for pagination)

        Returns:
            List of drivers
        """
        url = f"{self.base_url}/drivers"
        params = {
            'companyId': company_id,
            'limit': limit,
            'skip': skip
        }

        try:
            response = self._make_request('GET', url, params=params)
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Failed to list drivers: {str(e)}")

    def activate_driver(self, driver_id: str, rev: Optional[str] = None) -> Dict[str, Any]:
        """
        Activate a driver.

        Args:
            driver_id: Unique identifier for the driver
            rev: Document revision (if known)

        Returns:
            Response data from the API
        """
        update_data = DriverUpdateRequest(active=True)
        return self.update_driver(driver_id, update_data, rev)

    def deactivate_driver(self, driver_id: str, rev: Optional[str] = None) -> Dict[str, Any]:
        """
        Deactivate a driver.

        Args:
            driver_id: Unique identifier for the driver
            rev: Document revision (if known)

        Returns:
            Response data from the API
        """
        update_data = DriverUpdateRequest(active=False)
        return self.update_driver(driver_id, update_data, rev)