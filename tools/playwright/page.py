import allure
from playwright.sync_api import Page, Playwright


def initialize_playwright_page(playwright: Playwright, test_name: str, storage_state: str | None = None) -> Page:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(record_video_dir="./videos", storage_state=storage_state)

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )
    page = context.new_page()

    yield page

    context.tracing.stop(path=f"./tracing/{test_name}.zip")
    browser.close()

    allure.attach.file(source=f"./tracing/{test_name}.zip", name="tracing", extension="zip")
    allure.attach.file(source=f"{page.video.path()}", name="video", attachment_type=allure.attachment_type.WEBM)