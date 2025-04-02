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
    report.title = f"Login test report - {formatted_title_time}"

# link the video in the report
def pytest_html_results_table_row(report, cells):
    video_url = None
    for name, value in getattr(report, "user_properties", []):
        if name == "video_path":
            video_url = value
            break

    if video_url and len(cells) >= 4:
        cells[3] = HTMLExtra(f'<a href="{video_url}" target="_blank">Video</a>')

# __module__HTML wrapper
class HTMLExtra:
    __module__ = "pytest_html.extra"
    def __init__(self, content):
        self.content = content
    def __str__(self):
        return self.content

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

        page = item.funcargs.get("page", None)
        if page and hasattr(page, "video"):
            try:
                video_path = page.video.path().replace("\\", "/")
                if hasattr(rep, "user_properties"):
                    rep.user_properties.append(("video_path", video_path))
            except Exception:
                pass
