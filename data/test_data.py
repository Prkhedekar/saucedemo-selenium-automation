"""Test data shared across the suite. Sauce Demo publishes these credentials on its login page."""

BASE_URL = "https://www.saucedemo.com/"
PASSWORD = "secret_sauce"

STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PROBLEM_USER = "problem_user"
ERROR_USER = "error_user"

CUSTOMER = {"first_name": "Pranav", "last_name": "Khedekar", "postal_code": "411001"}

# (username, password, expected error) for data-driven negative login tests
INVALID_LOGINS = [
    ("", "", "Epic sadface: Username is required"),
    (STANDARD_USER, "", "Epic sadface: Password is required"),
    ("", PASSWORD, "Epic sadface: Username is required"),
    (STANDARD_USER, "wrong_password", "Epic sadface: Username and password do not match any user in this service"),
    ("unknown_user", PASSWORD, "Epic sadface: Username and password do not match any user in this service"),
    (LOCKED_OUT_USER, PASSWORD, "Epic sadface: Sorry, this user has been locked out."),
]

PRODUCTS = {
    "backpack": ("sauce-labs-backpack", "Sauce Labs Backpack", 29.99),
    "bike_light": ("sauce-labs-bike-light", "Sauce Labs Bike Light", 9.99),
    "bolt_tshirt": ("sauce-labs-bolt-t-shirt", "Sauce Labs Bolt T-Shirt", 15.99),
    "fleece_jacket": ("sauce-labs-fleece-jacket", "Sauce Labs Fleece Jacket", 49.99),
    "onesie": ("sauce-labs-onesie", "Sauce Labs Onesie", 7.99),
}
