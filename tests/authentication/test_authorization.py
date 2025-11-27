import allure
import pytest
from pages.authentication.login_page import LoginPage
from pages.authentication.login_page import AgentqlLoginPage
from tools.allure.tags import AllureTag
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from allure_commons.types import Severity
from playwright.sync_api import expect



@pytest.mark.regression
@pytest.mark.authorization
@allure.tag(AllureTag.AUTHORIZATION, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.story(AllureStory.AUTHORIZATION)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.AUTHENTICATION)
@allure.sub_suite(AllureStory.AUTHORIZATION)
class TestAuthorization:
    @pytest.mark.flaky(reruns=5)
    @pytest.mark.parametrize(
        "email, password",
        [
            ("user.name@gmail.com", "password"),
            ("user.name@gmail.com", "  "),
            ("  ", "password")
        ]
    )
    @allure.severity(Severity.CRITICAL)
    @allure.title("User login with wrong email or password")
    def test_wrong_email_or_password_authorization(self, login_page: LoginPage, email: str, password: str):
        login_page.visit(url="https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")
        login_page.login_form.fill(email=email, password=password)
        login_page.click_login_button()
        login_page.check_visible_wrong_email_or_password_alert()

    def test_agentql_fill_email(self, agentql_login_page: AgentqlLoginPage):
        agentql_login_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")

        email_input = agentql_login_page.find_agentql_element(
            """
                {
                    email_input
                }
            """
        )
        password_input = agentql_login_page.find_agentql_element(
            """
                {
                    password_input
                }
            """
        )

        login_button = agentql_login_page.find_agentql_element(
            """
                {
                    login_button
                }
            """
        )

        alert = agentql_login_page.find_agentql_element(
            """
                {
                    wrong_email_or_password_alert
                }
            """
        )

        expect(login_button.login_button).to_be_disabled()

        email_input.email_input.fill("test@test.ru")
        expect(email_input.email_input).to_have_value("test@test.ru")
        password_input.password_input.fill("password")
        expect(login_button.login_button).to_be_enabled()
        login_button.login_button.click()

        alert = agentql_login_page.find_agentql_element(
            """
                {
                    wrong_email_or_password_alert
                }
            """
        )

        expect(alert.wrong_email_or_password_alert).to_be_visible()
        expect(alert.wrong_email_or_password_alert).to_have_text("Wrong email or password")




