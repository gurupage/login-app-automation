import pytest
from playwright.sync_api import sync_playwright
from test_data import load_csv_data, determine_expected_message

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.mark.parametrize("username, password", load_csv_data())
def test_login(page, screenshot_helper, username, password):
    expected_message = determine_expected_message(username, password)
    page.goto("https://the-internet.herokuapp.com/login")
    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)
    screenshot_helper.capture(page, "fillOut")
    page.click("button[type='submit']")
    screenshot_helper.capture(page, "afterLogin")
    flash_message = page.inner_text("div#flash")
    assert expected_message in flash_message
