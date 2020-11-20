from typing import Callable, Final
from PyQt5 import QtWidgets as qtw
from ui_settings import Settings
from task import Task


class TaskWidget(qtw.QWidget):
	"""Widget representing Task."""
	def __init__(
	    self, task: Task, settings: Settings, on_edit: Callable[[Task], None],
	    on_delete: Callable[[Task], None]
	):
		super().__init__()
		self.task: Final[Task] = task

		main_layout = qtw.QHBoxLayout()
		task_details_layout = qtw.QVBoxLayout()

		self.setLayout(main_layout)

		summary_label = qtw.QLabel(task.summary)
		description_label = qtw.QLabel(task.description)

		edit_button = qtw.QPushButton(
		    text=settings.EDIT_TASK_BUTTON_TEXT, clicked=lambda: on_edit(task)
		)
		delete_button = qtw.QPushButton(
		    text=settings.DELETE_TASK_BUTTON_TEXT, clicked=lambda: on_delete(task)
		)

		task_details_layout.addWidget(summary_label)
		task_details_layout.addWidget(description_label)

		main_layout.addLayout(task_details_layout)
		main_layout.addWidget(edit_button)
		main_layout.addWidget(delete_button)
		self.setMaximumHeight(200)

		#TODO better button sizes
		#TODO ask before deleting


class TaskWidgetFactory:
	"""Creates TaskWidget with predefined parameters."""
	def __init__(
	    self, settings: Settings, on_edit: Callable[[Task], None],
	    on_delete: Callable[[Task], None]
	):
		self.settings = settings
		self._on_edit = on_edit
		self._on_delete = on_delete

	def create(self, task: Task) -> TaskWidget:
		"""Creates and returns TaskWidget."""
		return TaskWidget(task, self.settings, self._on_edit, self._on_delete)
