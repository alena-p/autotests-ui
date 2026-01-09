from playwright.sync_api import Page, expect

from components.charts.chart_view_component import ChartViewComponent
from components.dashboard.dashboard_toolbar_view_component import DashboardToolbarViewComponent
from components.navigation.navbar_component import NavbarComponent
from components.navigation.sidebar_component import SidebarComponent
from pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.sidebar = SidebarComponent(page)
        self.navbar = NavbarComponent(page)
        self.dashboard_toolbar = DashboardToolbarViewComponent(page)
        self.chart_view_students = ChartViewComponent(page, "students", "bar")
        self.chart_view_activities = ChartViewComponent(page, "activities", "line")
        self.chart_view_courses = ChartViewComponent(page, "courses", "pie")
        self.chart_view_scores = ChartViewComponent(page, "scores", "scatter")

    def check_visible_students_chart(self):
        self.chart_view_students.check_visible(title="Students")

    def check_visible_activities_chart(self):
        self.chart_view_activities.check_visible(title="Activities")

    def check_visible_courses_chart(self):
        self.chart_view_courses.check_visible(title="Courses")

    def check_visible_scores_chart(self):
        self.chart_view_scores.check_visible(title="Scores")
