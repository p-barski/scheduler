from typing import Callable, Optional
from task import Task
from database import DB
from ui_settings import Settings
from task_form_template import TaskFormTemplate


class TaskEditionWidget(TaskFormTemplate):
	"""Widget for editing tasks."""
	def __init__(self, settings: Settings, db: DB, on_cancel: Callable):
		super().__init__(settings)
		self._db = db

		self.cancel_button.clicked.connect(on_cancel)
		self.confirm_button.setText(settings.SAVE_CHANGES_BUTTON_TEXT)
		self.confirm_button.clicked.connect(self._on_edit)
		self._task: Optional[Task]

	def set_task(self, task: Task):
		self._task = task
		self.summary_line_edit.setText(task.summary)
		self.description_text_edit.setText(task.description)

	def _on_edit(self):
		print(f"{self._on_edit.__name__}")
		#TODO edit task