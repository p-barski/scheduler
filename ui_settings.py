class Settings:
	"""Settings for UI elements.
	Supported languages:
	ENG - English,
	PL - Polish."""
	def __init__(self, language: str):
		self.SUMMARY_TEXT_MAX_LENGTH = 100
		self.DESCRIPTION_TEXT_MAX_LENGTH = 200
		self.TIME_FORMAT = "%H:%M"
		self.DATE_FORMAT = "%d.%m.%Y"

		if language.upper() == "ENG":
			self.WINDOW_TITLE = "Tasks"
			self.CONFIRM_BUTTON_TEXT = "Confirm"
			self.PREVIOUS_DAY_BUTTON_TEXT = "Previous day"
			self.NEXT_DAY_BUTTON_TEXT = "Next day"
			self.CREATE_TASK_BUTTON_TEXT = "Create task"
			self.CANCEL_BUTTON_TEXT = "Cancel"
			self.SAVE_CHANGES_BUTTON_TEXT = "Save changes"
			self.EDIT_TASK_BUTTON_TEXT = "Edit"
			self.DELETE_TASK_BUTTON_TEXT = "Delete"

			self.SUMMARY_TEXT = "Summary"
			self.DESCRIPTION_TEXT = "Description"
			self.NOTIFICATION_TITLE = "Task reminder"
		elif language.upper() == "PL":
			self.WINDOW_TITLE = "Terminarz"
			self.CONFIRM_BUTTON_TEXT = "Potwierdź"
			self.PREVIOUS_DAY_BUTTON_TEXT = "Poprzedni dzień"
			self.NEXT_DAY_BUTTON_TEXT = "Następny dzień"
			self.CREATE_TASK_BUTTON_TEXT = "Stwórz zadanie"
			self.CANCEL_BUTTON_TEXT = "Anuluj"
			self.SAVE_CHANGES_BUTTON_TEXT = "Zapisz zmiany"
			self.EDIT_TASK_BUTTON_TEXT = "Edytuj"
			self.DELETE_TASK_BUTTON_TEXT = "Usuń"

			self.SUMMARY_TEXT = "Podsumowanie"
			self.DESCRIPTION_TEXT = "Opis"
			self.NOTIFICATION_TITLE = "Przypomnienie o zadaniu"
		else:
			raise ValueError(f"'{language}' language is not supported.")