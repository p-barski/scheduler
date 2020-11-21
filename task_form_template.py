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

		self.cancel_button = qtw.QPushButton(text=settings.CANCEL_BUTTON_TEXT)

		self.confirm_button = qtw.QPushButton(text=settings.CONFIRM_BUTTON_TEXT)

		self.notification_checkbox = qtw.QCheckBox(
		    text=settings.NOTIFICATION_CHECKBOX_TEXT,
		    layoutDirection=qtc.Qt.RightToLeft,
		    sizePolicy=qtw.QSizePolicy(
		        qtw.QSizePolicy.MinimumExpanding, qtw.QSizePolicy.Fixed
		    )
		)

		self.time_edit = qtw.QDateTimeEdit(
		    dateTime=qtc.QDateTime.currentDateTime().addSecs(60 * 60),
		    sizePolicy=qtw.QSizePolicy(
		        qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed
		    )
		)

		second_layout = qtw.QHBoxLayout()
		second_layout.addWidget(self.time_edit)
		second_layout.addWidget(self.notification_checkbox)

		button_layout = qtw.QHBoxLayout()
		button_layout.addWidget(self.cancel_button)
		button_layout.addWidget(self.confirm_button)

		main_layout.addLayout(text_layout)
		main_layout.addLayout(second_layout)
		main_layout.addLayout(button_layout)