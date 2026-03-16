import requests
from urllib3.util import create_urllib3_context


class LegacyAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        # Allows for legacy connection negotiation if the server is old
        context.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        kwargs["ssl_context"] = context
        return super(LegacyAdapter, self).init_poolmanager(*args, **kwargs)


def get_legacy_session():
    """
    Creates a requests.Session that automatically handles:
    - Cookie persistence across requests
    - Connection pooling
    - Legacy SSL/TLS support
    """
    # Mount the adapter for both http and https
    session = requests.Session()
    adapter = LegacyAdapter()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session
