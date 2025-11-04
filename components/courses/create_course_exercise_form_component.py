from components.base_component import BaseComponent
from playwright.sync_api import Page, expect

from elements.button import Button
from elements.text import Text
from elements.input import Input


class CreateCourseExerciseFormComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        self.delete_exercise_button = Button(
            page, "create-course-exercise-{index}-box-toolbar-delete-exercise-button", "Delete exercise")
        self.subtitle = Text(
            page, "create-course-exercise-{index}-box-toolbar-subtitle-text", "Exercise subtitle"
        )
        self.title_input = Input(
            page, "create-course-exercise-form-title-{index}-input", "Subtitle"
        )
        self.description_input = Input(
            page, "create-course-exercise-form-description-{index}-input", "Description"
        )

    def click_delete_button(self, index: int):
        self.delete_exercise_button.click(index=index)

    def check_visible(self, index: int, title: str, description: str):
        self.subtitle.check_visible(index=index)
        self.subtitle.check_have_text(f"#{index + 1} Exercise", index=index)

        self.title_input.check_visible(index=index)
        self.title_input.check_have_value(value=title, index=index)

        self.description_input.check_visible(index=index)
        self.description_input.check_have_value(value=description, index=index)

    def fill(self, index: int, title: str, description: str):
        self.title_input.fill(title, index=index)
        self.title_input.check_have_value(title, index=index)

        self.description_input.fill(description, index=index)
        self.title_input.check_have_value(description, index=index)

