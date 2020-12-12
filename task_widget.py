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
		main_layout.setAlignment(qtc.Qt.AlignTop)

		task_date_and_notification_layout = qtw.QHBoxLayout()

		task_details_layout = qtw.QVBoxLayout()
		task_details_layout.setAlignment(qtc.Qt.AlignTop)

		buttons_layout = qtw.QVBoxLayout()
		buttons_layout.setAlignment(qtc.Qt.AlignTop)

		size_policy = qtw.QSizePolicy(
		    qtw.QSizePolicy.MinimumExpanding, qtw.QSizePolicy.Preferred
		)
		alignment = qtc.Qt.AlignTop | qtc.Qt.AlignLeft

		self._summary_label = qtw.QLabel(
		    task.summary, sizePolicy=size_policy, alignment=alignment
		)
		self._description_label = qtw.QLabel(
		    task.description,
		    sizePolicy=size_policy,
		    visible=False,
		    alignment=alignment
		)
		date_label = qtw.QLabel(
		    task.scheduled_date.strftime(settings.TIME_FORMAT),
		    sizePolicy=qtw.QSizePolicy(
		        qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed
		    ),
		    alignment=alignment
		)
		notification_label = qtw.QLabel(
		    settings.notification_description(self.task.notification),
		    sizePolicy=size_policy,
		    alignment=alignment,
		    wordWrap=True
		)

		size_policy = qtw.QSizePolicy(
		    qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed
		)
		self._edit_button = qtw.QPushButton(
		    text=settings.EDIT_TASK_BUTTON_TEXT,
		    clicked=lambda: on_edit(task),
		    sizePolicy=size_policy
		)
		delete_button = qtw.QPushButton(
		    text=settings.DELETE_TASK_BUTTON_TEXT,
		    clicked=lambda: self._on_delete(settings, on_delete),
		    sizePolicy=size_policy
		)

		task_date_and_notification_layout.addWidget(date_label)
		task_date_and_notification_layout.addWidget(notification_label)

		task_details_layout.addWidget(self._summary_label)
		task_details_layout.addLayout(task_date_and_notification_layout)
		task_details_layout.addWidget(self._description_label)

		buttons_layout.addWidget(self._edit_button)
		buttons_layout.addWidget(delete_button)

		main_layout.addLayout(buttons_layout)
		main_layout.addLayout(task_details_layout)

		self.setLayout(main_layout)
		self.setToolTip(settings.TASK_WIDGET_TOOLTIP)
		self.setMinimumWidth(500)

	def resizeEvent(self, event):
		"""Overriden method, called when widget is resized."""
		width = self.width() - self._edit_button.width()
		font_width = self._summary_label.fontInfo().pixelSize() / 1.8
		#this max value is not entirely accurate,
		#but I have no idea how to do it properly
		#and it works better than standard word wrap
		max_chars_per_line = int(width / font_width)

		self._summary_label.setText(
		    word_wrap(self.task.summary, max_chars_per_line)
		)
		self._description_label.setText(
		    word_wrap(self.task.description, max_chars_per_line)
		)

	def mousePressEvent(self, event):
		"""Overriden method, called when widget is clicked on."""
		if self._description_label.isHidden():
			self._description_label.show()
		else:
			self._description_label.hide()

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


def word_wrap(text: str, max_chars_per_line: int) -> str:
	"""Default word wrap implementations is buggy,
	so here is a function that divides text into lines."""
	lines = []
	current_line = []
	split = text.split(" ")
	for word in split:
		if len(" ".join(current_line + [word])) < max_chars_per_line:
			current_line.append(word)
		elif len(word) >= max_chars_per_line:
			if len(current_line) != 0:
				lines.append(" ".join(current_line))
				current_line = []
			else:
				current_line.append(word)
				lines.append(" ".join(current_line))
				current_line = []
		else:
			lines.append(" ".join(current_line))
			current_line = []
			current_line.append(word)

	if len(current_line) != 0:
		lines.append(" ".join(current_line))
	return "\n".join(lines)