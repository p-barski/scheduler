from typing import Callable
from datetime import date, timedelta
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from task_widget import TaskWidgetFactory
from ui_settings import Settings
from database import DB


class TaskViewingWidget(qtw.QWidget):
	"""Displays all the tasks."""
	def __init__(
	    self, settings: Settings, db: DB, on_create: Callable,
	    on_date_click: Callable, tasks_changed_event: qtc.pyqtSignal,
	    factory: TaskWidgetFactory
	):
		super().__init__()
		tasks_changed_event.connect(self._redraw_tasks)

		self._db = db
		self._factory = factory
		self._settings = settings

		main_layout = qtw.QVBoxLayout()
		self.setLayout(main_layout)

		self._current_date = date.today()
		self._date_button = qtw.QPushButton(clicked=on_date_click)
		font = self._date_button.font()
		font.setPixelSize(20)
		self._date_button.setFont(font)
		self._update_date_label()

		tasks_scroll_area = qtw.QScrollArea(widgetResizable=True)
		tasks_scroll_area_content = qtw.QWidget()
		tasks_scroll_area.setWidget(tasks_scroll_area_content)

		self._tasks_layout = qtw.QVBoxLayout(tasks_scroll_area_content)
		self._tasks_layout.setAlignment(qtc.Qt.AlignTop)

		self._prev_day_button = qtw.QPushButton(
		    text=settings.PREVIOUS_DAY_BUTTON_TEXT,
		    clicked=lambda: self._change_day(-1)
		)

		self._create_task_button = qtw.QPushButton(
		    text=settings.CREATE_TASK_BUTTON_TEXT, clicked=on_create
		)

		self._next_day_button = qtw.QPushButton(
		    text=settings.NEXT_DAY_BUTTON_TEXT, clicked=lambda: self._change_day(1)
		)

		buttons_layout = qtw.QHBoxLayout()
		buttons_layout.addWidget(self._prev_day_button)
		buttons_layout.addWidget(self._create_task_button)
		buttons_layout.addWidget(self._next_day_button)

		main_layout.addWidget(self._date_button)
		main_layout.addWidget(tasks_scroll_area)
		main_layout.addLayout(buttons_layout)

	def change_day(self, day: date):
		self._current_date = day
		self._change_day(0)

	def retranslate(self, settings: Settings):
		self._settings = settings
		self._prev_day_button.setText(settings.PREVIOUS_DAY_BUTTON_TEXT)
		self._create_task_button.setText(settings.CREATE_TASK_BUTTON_TEXT)
		self._next_day_button.setText(settings.NEXT_DAY_BUTTON_TEXT)
		self._factory.settings = settings
		self._redraw_tasks()

	def showEvent(self, event):
		"""Overridden method, called upon self.show()."""
		self._redraw_tasks()

	def _change_day(self, days: int):
		self._current_date = self._current_date + timedelta(days=days)
		self._update_date_label()
		self._redraw_tasks()

	def _update_date_label(self):
		self._date_button.setText(
		    self._current_date.strftime(self._settings.DATE_FORMAT)
		)

	def _redraw_tasks(self):
		"""Redraws task widgets."""
		#Clearing all widgets
		for i in range(self._tasks_layout.count()):
			self._tasks_layout.itemAt(i).widget().close()

		for t in sorted(
		    self._db.get_tasks(self._current_date),
		    key=lambda task: task.scheduled_date
		):
			self._tasks_layout.addWidget(self._factory.create(t))