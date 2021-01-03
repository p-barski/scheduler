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
		day_label = qtw.QLabel(
		    str(day.day), alignment=qtc.Qt.AlignCenter, styleSheet=style
		)
		font = day_label.font()
		font.setPixelSize(75)
		day_label.setFont(font)

		tasks_label = qtw.QLabel(str(num_of_tasks), alignment=qtc.Qt.AlignCenter)
		font = tasks_label.font()
		font.setPixelSize(30)
		tasks_label.setFont(font)

		main_layout = qtw.QGridLayout()
		main_layout.addWidget(day_label, 0, 0)
		main_layout.addWidget(tasks_label, 0, 0)

		self.setLayout(main_layout)
		self.setMinimumWidth(100)
		self.setMinimumHeight(100)

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