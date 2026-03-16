import pytest
from app.services.safer.controller import parse_address, is_inactive, find_value_of

BeautifulSoup = pytest.importorskip("bs4").BeautifulSoup



def test_parse_address_returns_model_for_valid_address():
    address = "123 Main St, Austin, TX 78701"

    parsed = parse_address(address)

    assert parsed is not None
    assert parsed.city == "Austin"
    assert parsed.state == "TX"
    assert parsed.zip == "78701"


def test_parse_address_returns_none_for_invalid_input():
    assert parse_address("invalid") is None


def test_is_inactive_detects_inactive_table():
    soup = BeautifulSoup('<table summary="Record Inactive"></table>', "html.parser")

    assert is_inactive(soup) is True


def test_find_value_of_extracts_next_cell_value():
    soup = BeautifulSoup(
        "<table><tr><th>USDOT Number:</th><td>123456</td></tr></table>",
        "html.parser",
    )

    assert find_value_of(soup, "USDOT Number:") == "123456"
