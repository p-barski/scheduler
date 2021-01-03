from datetime import date
from calendar import monthrange
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from day_widget import DayWidgetFactory
from ui_settings import Settings


class MonthlyViewWidget(qtw.QWidget):
	def __init__(self, settings: Settings, factory: DayWidgetFactory):
		super().__init__()

		self._factory = factory
		self._settings = settings

		self._current_date = date.today().replace(day=1)
		self._date_label = qtw.QLabel(alignment=qtc.Qt.AlignCenter)
		font = self._date_label.font()
		font.setPixelSize(30)
		self._date_label.setFont(font)
		self._update_date_label()

		days_scroll_area = qtw.QScrollArea(widgetResizable=True)
		days_scroll_area_content = qtw.QWidget()
		days_scroll_area.setWidget(days_scroll_area_content)

		self._days_layout = qtw.QGridLayout(days_scroll_area_content)
		self._days_layout.setAlignment(qtc.Qt.AlignTop)

		self._prev_month_button = qtw.QPushButton(
		    text=settings.PREVIOUS_MONTH_BUTTON_TEXT,
		    clicked=lambda: self._change_month(-1)
		)

		self._next_month_button = qtw.QPushButton(
		    text=settings.NEXT_MONTH_BUTTON_TEXT,
		    clicked=lambda: self._change_month(1)
		)

		buttons_layout = qtw.QHBoxLayout()
		buttons_layout.addWidget(self._prev_month_button)
		buttons_layout.addWidget(self._next_month_button)

		main_layout = qtw.QVBoxLayout()
		main_layout.addWidget(self._date_label)
		main_layout.addWidget(days_scroll_area)
		main_layout.addLayout(buttons_layout)
		self.setLayout(main_layout)

	def retranslate(self, settings):
		self._settings = settings
		self._prev_month_button.setText(settings.PREVIOUS_MONTH_BUTTON_TEXT)
		self._next_month_button.setText(settings.NEXT_MONTH_BUTTON_TEXT)

	def showEvent(self, event):
		"""Overridden method, called upon self.show()."""
		self._redraw_widgets()

	def _redraw_widgets(self):
		#Clearing all widgets
		for i in range(self._days_layout.count()):
			self._days_layout.itemAt(i).widget().close()

		days = monthrange(self._current_date.year, self._current_date.month)[1]
		counter = 0
		divider = 5
		for day in range(1, days + 1):
			widget = self._factory.create(self._current_date.replace(day=day))
			self._days_layout.addWidget(widget, counter // divider, counter % divider)
			counter += 1

	def _change_month(self, months: int):
		month = self._current_date.month + months
		year = self._current_date.year
		while month < 1:
			month = 12 - month
			year -= 1
		while month > 12:
			month -= 12
			year += 1
		self._current_date = self._current_date.replace(month=month, year=year)
		self._update_date_label()
		self._redraw_widgets()

	def _update_date_label(self):
		self._date_label.setText(self._current_date.strftime("%m.%Y"))
