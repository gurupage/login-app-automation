import os
import pytest
from playwright.async_api import async_playwright
import datetime
from pytest_html import extras


# get a current time 
now = datetime.datetime.now()
formatted_time = now.strftime("%Y%m%d_%H%M") #format for file name
formatted_title_time = now.strftime("%Y-%m-%d %H:%M") #format for title of report

# configuration for file name
def pytest_configure(config):
    config.option.htmlpath = f"report_{formatted_time}.html"

# configuration for title of report
def pytest_html_report_title(report):
    report.title = f"My test report - {formatted_title_time}"

class ScreenshotHelper:
    def __init__(self, test_name, screenshot_dir="screenshots"):
        self.test_name = test_name
        self.screenshot_dir = screenshot_dir
        self.step = 1
        self.screenshots = []
        os.makedirs(screenshot_dir, exist_ok=True)

    def capture(self, page, step_description="step"):
        filename = f"{self.test_name}_step{self.step:02d}_step{step_description}.png"
        path = os.path.join(self.screenshot_dir, filename)
        page.screenshot(path=path)
        self.screenshots.append(path)
        self.step += 1

@pytest.fixture
def screenshot_helper(request):
    helper = ScreenshotHelper(request.node.name)
    request.node.screenshot_helper = helper
    return helper

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        helper = getattr(item, "screenshot_helper", None)
        if helper and helper.screenshots:
            extra = getattr(rep, "extra", [])
            for screenshot in helper.screenshots:
                extra.append(extras.image(screenshot, mime_type="image/png"))

            rep.extra = extra
