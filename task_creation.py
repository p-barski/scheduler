from typing import Callable
from task_form_template import TaskFormTemplate
from ui_settings import Settings
from database import DB
from task import Task


class TaskCreationWidget(TaskFormTemplate):
	"""Widget for creating tasks."""
	def __init__(self, settings: Settings, db: DB, on_cancel: Callable):
		super().__init__(settings)
		self._db = db

		self.cancel_button.clicked.connect(on_cancel)

		self.confirm_button.setText(settings.CREATE_TASK_BUTTON_TEXT)
		self.confirm_button.clicked.connect(self._on_create)

	def _on_create(self):
		"""Creates task."""
		#TODO fields should not be empty, disable confirm button when it's empty
		time = self.time_edit.dateTime().toPyDateTime()
		summary = self.summary_line_edit.text()
		descr = self.description_text_edit.toPlainText()
		self._db.save_task(Task(summary, descr))
		self.summary_line_edit.clear()
		self.description_text_edit.clear()
		print(f"{time}:{type(time)}:{summary}:{descr}")