from typing import Final


class Settings:
	"""Settings for UI elements."""
	WINDOW_TITLE: Final[str] = "Tasks"
	WINDOW_WIDTH: Final[int] = 1280
	WINDOW_HEIGHT: Final[int] = 720

	CONFIRM_BUTTON_TEXT: Final[str] = "Confirm"

	PREVIOUS_DAY_BUTTON_TEXT: Final[str] = "Previous day"
	NEXT_DAY_BUTTON_TEXT: Final[str] = "Next day"
	CREATE_TASK_BUTTON_TEXT: Final[str] = "Create task"

	SUMMARY_TEXT: Final[str] = "Summary"
	SUMMARY_TEXT_MAX_LENGTH: Final[int] = 100
	DESCRIPTION_TEXT: Final[str] = "Description"
	CANCEL_BUTTON_TEXT: Final[str] = "Cancel"

	SAVE_CHANGES_BUTTON_TEXT: Final[str] = "Save changes"
	EDIT_TASK_BUTTON_TEXT: Final[str] = "Edit"
	DELETE_TASK_BUTTON_TEXT: Final[str] = "Delete"
