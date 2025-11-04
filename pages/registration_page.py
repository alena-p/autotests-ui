from playwright.sync_api import Page, expect

from components.authentication.registration_form_component import RegistrationFormComponent
from pages.base_page import BasePage
from elements.text import Text
from elements.button import Button
from elements.link import Link

class RegistrationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.registration_form = RegistrationFormComponent(page)

        self.page_title = Text(page, "authentication-ui-course-title-text", "Authentication page title")
        self.registration_button = Button(
            page, "registration-page-registration-button", "Registration button"
        )
        self.login_link = Link(page, "registration-page-login-link", "Login link")


    def click_registration_button(self):
        self.registration_button.click()

    def check_enabled_registration_button(self):
        self.registration_button.check_enabled()