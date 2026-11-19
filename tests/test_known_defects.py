"""Automated checks for defects found during manual testing.

Bug IDs refer to https://github.com/Prkhedekar/saucedemo-manual-uat-testing/tree/main/bug-reports.
Each test asserts the CORRECT behaviour and is marked xfail(strict=True): it is reported as
"xfailed" while the bug exists, and fails the build (XPASS) once the bug is fixed, so the
marker gets removed and the test becomes a normal regression check.
"""

import pytest

from data.test_data import CUSTOMER, ERROR_USER, PASSWORD, PRODUCTS, PROBLEM_USER

pytestmark = pytest.mark.known_defect


@pytest.mark.xfail(strict=True, reason="BUG-001: item total shows $113.94999999999999 for this add order")
def test_bug_001_item_total_is_formatted_as_currency(login_as):
    inventory = login_as()
    for key in ("onesie", "fleece_jacket", "bolt_tshirt", "bike_light", "backpack"):
        inventory.add_to_cart(PRODUCTS[key][0])
    overview = inventory.open_cart().checkout().fill(**CUSTOMER).continue_to_overview()
    assert overview.subtotal_text() == "Item total: $113.95"


@pytest.mark.xfail(strict=True, reason="BUG-007: problem_user's Last Name typing goes into First Name")
def test_bug_007_checkout_form_keeps_last_name(login_as):
    inventory = login_as(PROBLEM_USER, PASSWORD).add_to_cart(PRODUCTS["backpack"][0])
    info = inventory.open_cart().checkout().fill(**CUSTOMER)
    assert info.field_values() == CUSTOMER


@pytest.mark.xfail(strict=True, reason="BUG-010: error_user's Finish button does nothing")
def test_bug_010_finish_completes_order(login_as):
    inventory = login_as(ERROR_USER, PASSWORD).add_to_cart(PRODUCTS["backpack"][0])
    overview = inventory.open_cart().checkout().fill(**CUSTOMER).continue_to_overview()
    assert overview.finish().header() == "Thank you for your order!"
