from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from ui_settings import Settings


class TaskFormTemplate(qtw.QWidget):
	"""UI template for creating and editing tasks."""
	def __init__(self, settings: Settings):
		super().__init__()
		main_layout = qtw.QVBoxLayout()
		self.setLayout(main_layout)

		self.summary_line_edit = qtw.QLineEdit(
		    placeholderText=settings.SUMMARY_TEXT,
		    maxLength=settings.SUMMARY_TEXT_MAX_LENGTH
		)

		self.description_text_edit = qtw.QTextEdit(
		    placeholderText=settings.DESCRIPTION_TEXT
		)

		text_layout = qtw.QVBoxLayout()
		text_layout.addWidget(self.summary_line_edit)
		text_layout.addWidget(self.description_text_edit)

		#TODO current date
		self.time_edit = qtw.QDateTimeEdit(
		    dateTime=qtc.QDateTime(qtc.QDate(2020, 11, 30), qtc.QTime(8, 30, 0))
		)

		self.cancel_button = qtw.QPushButton(text=settings.CANCEL_BUTTON_TEXT)

		self.confirm_button = qtw.QPushButton(text=settings.CONFIRM_BUTTON_TEXT)

		button_layout = qtw.QHBoxLayout()
		button_layout.addWidget(self.cancel_button)
		button_layout.addWidget(self.confirm_button)

		main_layout.addLayout(text_layout)
		main_layout.addWidget(self.time_edit)
		main_layout.addLayout(button_layout)