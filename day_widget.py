from datetime import date
from typing import Callable
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from database import DB


class DayWidget(qtw.QPushButton):
	def __init__(self, day: date, num_of_tasks: int, on_click: Callable):
		super().__init__()
		self._day = day
		self.clicked.connect(lambda: on_click(day))
		size_policy = qtw.QSizePolicy(
		    qtw.QSizePolicy.MinimumExpanding, qtw.QSizePolicy.MinimumExpanding
		)
		self.setSizePolicy(size_policy)

		style = f"color: {self._calculate_background_letter_color()};"
		self._day_label = qtw.QLabel(
		    str(day.day), alignment=qtc.Qt.AlignCenter, styleSheet=style
		)
		self._resize_day_label_font()

		if num_of_tasks == 0:
			tasks_label_text = ""
		else:
			tasks_label_text = str(num_of_tasks)

		self._tasks_label = qtw.QLabel(
		    tasks_label_text, alignment=qtc.Qt.AlignCenter
		)
		self._resize_tasks_label_font()

		main_layout = qtw.QGridLayout()
		main_layout.addWidget(self._day_label, 0, 0)
		main_layout.addWidget(self._tasks_label, 0, 0)

		self.setLayout(main_layout)
		self.setMinimumWidth(100)
		self.setMinimumHeight(100)

	def resizeEvent(self, event):
		"""Overriden method, called when widget is resized."""
		self._resize_day_label_font()
		self._resize_tasks_label_font()

	def _resize_day_label_font(self):
		font_size = min(self.width(), self.height()) / 2
		font = self._day_label.font()
		font.setPointSizeF(font_size)
		self._day_label.setFont(font)

	def _resize_tasks_label_font(self):
		font_size = min(self.width(), self.height()) / 5
		font = self._tasks_label.font()
		font.setPointSizeF(font_size)
		self._tasks_label.setFont(font)

	def _calculate_background_letter_color(self):
		color = self.palette().color(self.backgroundRole())
		diff = 0x202020
		if color.red() + color.green() + color.blue() < 500:
			#dark mode, color should be lighter
			hex_color = f"#{hex(color.rgb() + diff)[2:]}"
		else:
			#light mode, color should be darker
			hex_color = f"#{hex(color.rgb() - diff)[2:]}"
		return hex_color


class DayWidgetFactory:
	def __init__(self, db: DB, on_click: Callable):
		self.db = db
		self.on_click = on_click

	def create(self, day: date) -> DayWidget:
		num_of_tasks = len(self.db.get_tasks(day))
		return DayWidget(day, num_of_tasks, self.on_click)