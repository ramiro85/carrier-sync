import pytest

pytest.importorskip("bs4")

from app.services.tafs.controller import select_best_debtor
from app.services.tafs.schemas import TafDebtor


def test_select_best_debtor_prefers_non_denied_status():
    denied = TafDebtor(account_id="1", debtor_buy_status="Denied")
    approved = TafDebtor(account_id="2", debtor_buy_status="Approved")

    result = select_best_debtor([denied, approved])

    assert result.account_id == "2"


def test_select_best_debtor_returns_first_when_no_better_match():
    first = TafDebtor(account_id="1", debtor_buy_status="Denied")
    second = TafDebtor(account_id="2", debtor_buy_status="Denied")

    result = select_best_debtor([first, second])

    assert result.account_id == "1"
