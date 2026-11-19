# Sauce Demo: Selenium + Python Test Automation

[![UI tests](https://github.com/Prkhedekar/saucedemo-selenium-automation/actions/workflows/tests.yml/badge.svg)](https://github.com/Prkhedekar/saucedemo-selenium-automation/actions/workflows/tests.yml)

Automated UI test suite for [Sauce Demo (Swag Labs)](https://www.saucedemo.com/), built with **Selenium 4, Python and pytest**
using the **Page Object Model**. It is the automation follow-up to my
[manual & UAT testing project](https://github.com/Prkhedekar/saucedemo-manual-uat-testing) on the same site: defects I
found by hand are now checked automatically on every run.

## Results (local run, 2026-11-19, Chrome 157, headless)

| | |
|---|---|
| Automated tests | **26**: 23 passed, 3 known defects reproduced (xfail) |
| Run time | ~2 minutes |
| Browsers | Chrome, Firefox, Edge (`--browser`) |
| CI | GitHub Actions on every push, a weekly schedule, Chrome + Firefox matrix |

## What's covered

| Area | Tests | Highlights |
|---|---|---|
| Login | 9 | Valid login, 6 data-driven negative cases (empty fields, wrong password, locked-out user), logout, direct-URL access blocked |
| Inventory | 6 | Sort by name and price (both directions), product count, cart badge on add/remove |
| Cart | 3 | Added items listed, remove from cart, cart kept after "Continue shopping" |
| Checkout | 5 | End-to-end purchase with total = subtotal + tax, each required field validated, 8% tax |
| Known defects | 3 | Reproduce bugs from the manual project ([details](#known-defects-as-regression-tests)) |

## Framework features

- **Page Object Model**: locators and page actions live in `pages/`, so tests read like test cases and a UI change is fixed in one place
- **Explicit waits only**: no `time.sleep`; every interaction waits for the element to be visible or clickable
- **Data-driven tests**: credentials, products and expected errors in `data/test_data.py`, run through `pytest.mark.parametrize`
- **HTML report** with a **screenshot and page URL attached to every failure**
- **Markers** to run a subset: `smoke`, `regression`, `known_defect`
- **Cross-browser** via `--browser chrome|firefox|edge`, and `--headless` for CI
- **CI pipeline** that uploads the HTML report as a build artifact

## Project structure

```
├── conftest.py              # driver fixture, CLI options, login fixture, screenshot-on-failure hook
├── pytest.ini               # report settings and markers
├── data/test_data.py        # users, products, customer details, expected error messages
├── pages/
│   ├── base_page.py         # shared waits, clicks, typing, header actions (cart, logout)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py     # info, overview and complete steps
├── tests/
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   └── test_known_defects.py
└── .github/workflows/tests.yml
```

## Run it

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

pytest                          # all tests, Chrome with a window
pytest --headless               # no window
pytest -m smoke                 # smoke tests only
pytest --browser firefox        # another browser
```

The report is written to `reports/report.html`. Selenium Manager downloads the right browser driver automatically.

## Known defects as regression tests

Each test asserts the **correct** behaviour and is marked `xfail(strict=True)`. While the bug exists the run shows
*xfailed*. Once it is fixed the test passes unexpectedly, which **fails the build** as a reminder to remove the marker
and keep it as a normal regression test.

| Test | Bug | Problem |
|---|---|---|
| `test_bug_001_item_total_is_formatted_as_currency` | [BUG-001](https://github.com/Prkhedekar/saucedemo-manual-uat-testing/blob/main/bug-reports/BUG-001.md) | Item total shows `$113.94999999999999` |
| `test_bug_007_checkout_form_keeps_last_name` | [BUG-007](https://github.com/Prkhedekar/saucedemo-manual-uat-testing/blob/main/bug-reports/BUG-007.md) | `problem_user`: Last Name input is written into First Name |
| `test_bug_010_finish_completes_order` | [BUG-010](https://github.com/Prkhedekar/saucedemo-manual-uat-testing/blob/main/bug-reports/BUG-010.md) | `error_user`: Finish button does nothing |

## Author

Pranav Khedekar, QA Engineer (manual + Selenium/Python automation).
Available for website testing and test automation work.
