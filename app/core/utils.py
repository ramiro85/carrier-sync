import re
from typing import List

from app.services.googleCloud.schemas import Headers


def get_headers_object(headers: List):
    """Convert a list of Gmail header dicts into the typed Headers dataclass."""
    headers_dict = {t["name"]: t["value"] for t in headers}
    return Headers.from_dict(headers_dict)


def clean_email(str_emails):
    """Normalize comma-separated email strings into a plain list of addresses."""
    parts = str_emails.split(",")
    emails = []
    for part in parts:
        part = part.strip().lower()
        match = re.match(r"^(.*)<(.+)>$", part)
        if match:
            emails.append(match.group(2))
        else:
            emails.append(part)

    return emails


def get_contact_list(str_emails):
    """Parse comma-separated emails into a list of `{email, name}` contact dicts."""
    parts = str_emails.split(",")
    contacts = []
    for part in parts:
        part = part.strip().lower()
        match = re.match(r"^(.*)<(.+)>$", part)
        if match:
            contacts.append({"email": match.group(2), "name": match.group(1)})
        else:
            contacts.append({"email": part, "name": part.split("@")[0]})

    return contacts
