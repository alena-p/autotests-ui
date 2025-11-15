import allure
import pytest

from pages.courses.courses_list_page import CoursesListPage
from pages.courses.create_course_page import CreateCoursePage
from tools.allure.tags import AllureTag
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from allure_commons.types import Severity


@pytest.mark.courses
@pytest.mark.regression
@allure.tag(AllureTag.COURSES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@allure.story(AllureStory.COURSES)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.COURSES)
@allure.sub_suite(AllureStory.COURSES)
class TestCourses:
    @allure.severity(Severity.NORMAL)
    @allure.title("Checking empty courses list view")
    def test_empty_courses_list(self, courses_list_page: CoursesListPage):
        courses_list_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses")
        courses_list_page.navbar.check_visible(username="username")
        courses_list_page.sidebar.check_visible()
        courses_list_page.toolbar_view.check_visible()
        courses_list_page.check_visible_empty_view()

    @allure.severity(Severity.BLOCKER)
    @allure.title("Successful course creation")
    def test_create_course(self, courses_list_page: CoursesListPage, create_course_page: CreateCoursePage):
        create_course_page.visit(
            url="https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses/create"
        )
        create_course_page.create_course_toolbar.check_visible(is_create_course_disabled=True)
        create_course_page.image_upload_widget.check_visible(is_image_uploaded=False)
        create_course_page.create_course_form.check_visible(
            title="",
            description="",
            estimated_time="",
            min_score="0",
            max_score="0"
        )
        create_course_page.exercises_toolbar.check_visible()
        create_course_page.check_visible_exercises_empty_view()
        create_course_page.image_upload_widget.upload_preview_image(file="./testdata/files/image.png")
        create_course_page.image_upload_widget.check_visible(is_image_uploaded=True)
        create_course_page.create_course_form.fill(
            title="Playwright",
            estimated_time="2 weeks",
            description="Playwright",
            max_score="100",
            min_score="10"
        )
        create_course_page.create_course_toolbar.click_create_course_button()
        courses_list_page.toolbar_view.check_visible()
        courses_list_page.course_view.check_visible(
            index=0, title="Playwright", max_score="100", min_score="10", estimated_time="2 weeks"
        )

    @allure.severity(Severity.CRITICAL)
    @allure.title("Successful course edition")
    def test_edit_course(self, create_course_page: CreateCoursePage, courses_list_page: CoursesListPage
    ):
        create_course_page.visit(
            url="https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses/create"
        )
        create_course_page.create_course_form.fill(
            title="Супер курс",
            estimated_time="2 недели",
            description="Описание супер курса",
            max_score="50",
            min_score="10"
        )

        create_course_page.create_course_form.check_visible(
            title="Супер курс",
            estimated_time="2 недели",
            description="Описание супер курса",
            max_score="50",
            min_score="10"
        )

        create_course_page.image_upload_widget.upload_preview_image(file="./testdata/files/image.png")

        create_course_page.create_course_toolbar.create_course_button.click()

        courses_list_page.course_view.check_visible(
            index=0,
            title="Супер курс",
            estimated_time="2 недели",
            max_score="50",
            min_score="10"
        )

        courses_list_page.course_view.menu.click_edit_course(index=0)

        create_course_page.create_course_form.fill(
            title="Пупер курс",
            estimated_time="3 недели",
            description="Описание пупер курса",
            max_score="100",
            min_score="20"
        )

        create_course_page.create_course_form.check_visible(
            title="Пупер курс",
            estimated_time="3 недели",
            description="Описание пупер курса",
            max_score="100",
            min_score="20"
        )

        create_course_page.create_course_toolbar.create_course_button.click()

        courses_list_page.course_view.check_visible(
            index=0,
            title="Пупер курс",
            estimated_time="3 недели",
            max_score="100",
            min_score="20"
        )
