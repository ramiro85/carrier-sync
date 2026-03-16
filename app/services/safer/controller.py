from bs4 import BeautifulSoup
import re
import requests
import certifi
from app.config import settings
from app.core.schemas import ResponseModel
from app.services.safer.schemas import Company, Address


def find_value_of(soup, text: str) -> str | None:
    """Find value in table by searching for a header containing the given text."""
    th = soup.find("th", string=lambda s: s and text in s)
    if th:
        td = th.find_next_sibling("td")
        if td:
            return td.text.strip().replace('\xa0', ' ')
    return None


def is_inactive(soup) -> bool:
    """Check if the record is marked as inactive."""
    return True if soup.find("table", summary="Record Inactive") else False


def find_operating_status(soup) -> dict[str, str | None]:
    """Extract operating authority status and details."""
    operating_authority_status = {'status': None, 'details': None}
    th = soup.find("th", string=lambda s: s and "Operating Authority Status:" in s)
    if th:
        td = th.find_next_sibling("td")
        if td:
            not_auth = td.find("font", color="#0000c0")
            if not_auth:
                status = not_auth.find_next("b").contents[0].text.strip().replace('\xa0', ' ')
                operating_authority_status['status'] = status
                details = not_auth.find_next("p").text.strip().replace('\xa0', ' ').replace('\n', ' ')
                operating_authority_status['details'] = details
            else:
                operating_authority_status['status'] = td.contents[0].strip().replace('\xa0', ' ')
    return operating_authority_status


def parse_address(address_string: str | None) -> Address | None:
    """Parse address string into Address model."""
    if not address_string:
        return None

    parts = re.split(',|\r\n|\xa0 ', address_string)
    if len(parts) < 3:
        return None

    city_zip = parts[2].strip().split()
    if len(city_zip) < 2:
        return None

    return Address(
        address=parts[0].strip(),
        city=parts[1].strip(),
        state=city_zip[0],
        zip=city_zip[1],
        full_address=f"{parts[0].strip()}, {parts[1].strip()}, {parts[2].strip()}"
    )


def check_company(query_param: str, query_string: str) -> Company:
    """
    Check company information from SAFER database.

    Args:
        query_param: The query parameter type (e.g., 'MC_MX')
        query_string: The search query string

    Returns:
        Company model if found, otherwise dict with error info
    """
    url = f"{settings.safer_base_url}/query.asp"
    payload = f"searchtype=ANY&query_type=queryCarrierSnapshot&query_param={query_param}&query_string={query_string}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': f"{settings.safer_base_url}/",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': settings.safer_base_url,
        'Connection': 'keep-alive',
        'Cookie': settings.safer_base_cookie,
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers'
    }

    try:
        response = requests.post(url, headers=headers, verify=certifi.where(), data=payload, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        return Company(
            founded=False,
            message=f'Error connecting to SAFER: {str(e)}')

    soup = BeautifulSoup(response.text, "html.parser")

    # Check if inactive
    if is_inactive(soup):
        return Company(
            founded=False,
            message=f'MC-{query_string} is inactive',
            operating_authority_status='Inactive'
        )

    # Check if MC number exists
    mc = find_value_of(soup, "MC/MX/FF Number(s):")
    if not mc:
        return Company(
            founded=False,
            message=f'There is no matching records in the SAFER database with the MC-{query_string}',
            operating_authority_status='Not Found'
        )

    # Extract operating status
    op_status = find_operating_status(soup)

    # Parse addresses
    physical_address_str = find_value_of(soup, "Physical Address:")
    mailing_address_str = find_value_of(soup, "Mailing Address:")

    physical_address = parse_address(physical_address_str)
    mailing_address = parse_address(mailing_address_str)

    # If addresses couldn't be parsed, use empty Address objects
    if not physical_address:
        physical_address = Address(address='', city='', state='', zip='', full_address='')
    if not mailing_address:
        mailing_address = Address(address='', city='', state='', zip='', full_address='')

    # Create a Company model
    company = Company(
        founded=True,
        entity_type=find_value_of(soup, "Entity Type:") or '',
        mc_number=mc.split('-')[1].strip(),
        usdot_number=find_value_of(soup, "USDOT Number:") or '',
        usdot_status=find_value_of(soup, "USDOT Status:") or '',
        legal_name=find_value_of(soup, "Legal Name:") or '',
        dba_name=find_value_of(soup, "DBA Name:") or '',
        phone=find_value_of(soup, "Phone:") or '',
        message=op_status.get('details'),
        operating_authority_status=op_status.get('status') or 'Inactive',
        physical_address=physical_address,
        mailing_address=mailing_address
    )

    return company
