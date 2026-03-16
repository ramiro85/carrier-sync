from app.core.utils import clean_email, get_contact_list, get_headers_object


def test_clean_email_normalizes_values():
    raw = "User One <ONE@example.com>, plain@example.org"

    assert clean_email(raw) == ["one@example.com", "plain@example.org"]


def test_get_contact_list_extracts_name_and_email():
    raw = "User One <one@example.com>, plain@example.org"

    assert get_contact_list(raw) == [
        {"email": "one@example.com", "name": "user one "},
        {"email": "plain@example.org", "name": "plain"},
    ]


def test_get_headers_object_builds_header_dataclass():
    headers = [
        {"name": "Subject", "value": "Hello"},
        {"name": "From", "value": "sender@example.com"},
        {"name": "To", "value": "recipient@example.com"},
        {"name": "Message-ID", "value": "<msg-1>"},
    ]

    header_obj = get_headers_object(headers)

    assert header_obj.Subject == "Hello"
    assert header_obj.From == "sender@example.com"
    assert header_obj.To == "recipient@example.com"
    assert header_obj.Message_ID == "<msg-1>"
