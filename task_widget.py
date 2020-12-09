from typing import Callable, Final
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
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
		date_label = qtw.QLabel(task.scheduled_date.strftime(settings.TIME_FORMAT))
		notification_label = qtw.QLabel(str(task.notification))

		edit_button = qtw.QPushButton(
		    text=settings.EDIT_TASK_BUTTON_TEXT, clicked=lambda: on_edit(task)
		)
		delete_button = qtw.QPushButton(
		    text=settings.DELETE_TASK_BUTTON_TEXT,
		    clicked=lambda: self._on_delete(settings, on_delete)
		)

		task_details_layout.addWidget(summary_label)
		task_details_layout.addWidget(description_label)
		task_details_layout.addWidget(date_label)
		task_details_layout.addWidget(notification_label)

		main_layout.addLayout(task_details_layout)
		main_layout.addWidget(edit_button)
		main_layout.addWidget(delete_button)
		self.setMaximumHeight(200)

		#TODO better button sizes

	def _on_delete(self, settings: Settings, on_delete: Callable[[Task], None]):
		popup = qtw.QMessageBox(
		    windowTitle=settings.ON_DELETE_POPUP_TITLE,
		    text=settings.ON_DELETE_POPUP_QUESTION,
		    standardButtons=qtw.QMessageBox.Yes | qtw.QMessageBox.No
		)
		yes_button = popup.button(qtw.QMessageBox.Yes)
		yes_button.setText(settings.YES_BUTTON_TEXT)
		no_button = popup.button(qtw.QMessageBox.No)
		no_button.setText(settings.NO_BUTTON_TEXT)
		no_button.setFocus()
		popup.exec_()
		if popup.clickedButton() == yes_button:
			on_delete(self.task)


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
