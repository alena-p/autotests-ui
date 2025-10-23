from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class RegistrationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.page_title = page.get_by_test_id("authentication-ui-course-title-text")
        self.email_input = page.get_by_test_id("registration-form-email-input").locator("input")
        self.username_input = page.get_by_test_id("registration-form-username-input").locator("input")
        self.password_input = page.get_by_test_id("registration-form-password-input").locator("input")
        self.registration_button = page.get_by_test_id("registration-page-registration-button")
        self.login_link = page.get_by_test_id("registration-page-login-link")

    def fill_registration_form(self, email: str, username: str, password: str):
        self.email_input.fill(email)
        self.username_input.fill(username)
        self.password_input.fill(password)

    def click_registration_button(self):
        self.registration_button.click()

    def check_enabled_registration_button(self):
        expect(self.registration_button).to_be_enabled()
