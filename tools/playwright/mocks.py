from playwright.sync_api import Page

def mock_static_resources(page: Page):
    page.route("**/*.{ico,jpg,svg,webp,mp3,woff,woff2}", lambda route: route.abort())
