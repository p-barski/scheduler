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

		self.summary_line_edit.textChanged.connect(self._enforce_task_change)
		self.description_text_edit.textChanged.connect(self._enforce_task_change)
		self.notification_checkbox.stateChanged.connect(self._enforce_task_change)
		self.time_edit.dateTimeChanged.connect(self._enforce_task_change)

	def set_task(self, task: Task):
		self._task = task
		self.summary_line_edit.setText(task.summary)
		self.description_text_edit.setText(task.description)
		self.time_edit.setDateTime(self._task.datetime)
		self.notification_checkbox.setChecked(self._task.notification)

	def _enforce_task_change(self):
		if self._task is None:
			return
		summary = self.summary_line_edit.text()
		descr = self.description_text_edit.toPlainText()
		time = self.time_edit.dateTime().toPyDateTime()
		notification = self.notification_checkbox.isChecked()

		if (summary, descr, time, notification) == (
		    self._task.summary, self._task.description, self._task.datetime,
		    self._task.notification
		):
			self.confirm_button.setEnabled(False)
		else:
			self._enforce_summary_not_empty()

	def _on_edit(self):
		if self._task is None:
			return
		summary = self.summary_line_edit.text()
		descr = self.description_text_edit.toPlainText()
		time = self.time_edit.dateTime().toPyDateTime()
		notification = self.notification_checkbox.isChecked()
		self._task.summary = summary
		self._task.description = descr
		self._task.datetime = time
		self._task.notification = notification
		self._db.save_task(self._task)