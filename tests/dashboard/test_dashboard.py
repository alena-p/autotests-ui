import allure
import pytest
from tools.allure.tags import AllureTag
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from allure_commons.types import Severity

from pages.dashboard.dashboard_page import DashboardPage

@pytest.mark.dashboard
@pytest.mark.regression
@allure.tag(AllureTag.DASHBOARD, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.DASHBOARD)
@allure.story(AllureStory.DASHBOARD)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.DASHBOARD)
@allure.sub_suite(AllureStory.DASHBOARD)
class TestDashboard:
    @allure.severity(Severity.CRITICAL)
    @allure.title("Checking charts on dashboard")
    def test_dashboard_displaying(self, dashboard_page_with_state: DashboardPage):
        dashboard_page_with_state.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/dashboard")
        dashboard_page_with_state.sidebar.check_visible()
        dashboard_page_with_state.navbar.check_visible("username")
        dashboard_page_with_state.dashboard_toolbar.check_visible()
        dashboard_page_with_state.check_visible_scores_chart()
        dashboard_page_with_state.check_visible_courses_chart()
        dashboard_page_with_state.check_visible_students_chart()
        dashboard_page_with_state.check_visible_activities_chart()
