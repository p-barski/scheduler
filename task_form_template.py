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
		    maxLength=settings.SUMMARY_TEXT_MAX_LENGTH,
		    textChanged=self._enforce_summary_not_empty
		)

		self.description_text_edit = qtw.QTextEdit(
		    placeholderText=settings.DESCRIPTION_TEXT,
		    textChanged=lambda: self.
		    _enforce_text_edit_length(settings.DESCRIPTION_TEXT_MAX_LENGTH)
		)

		text_layout = qtw.QVBoxLayout()
		text_layout.addWidget(self.summary_line_edit)
		text_layout.addWidget(self.description_text_edit)

		self.cancel_button = qtw.QPushButton(text=settings.CANCEL_BUTTON_TEXT)

		self.confirm_button = qtw.QPushButton(
		    text=settings.CONFIRM_BUTTON_TEXT, enabled=False
		)

		self.notification_choice = qtw.QComboBox(
		    sizePolicy=qtw.
		    QSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Fixed)
		)
		#TODO settings
		items = ["Off"]
		items.extend([f"{i} min" for i in range(1, 61)])
		self.notification_choice.addItems(items)

		self.time_edit = qtw.QDateTimeEdit(
		    dateTime=qtc.QDateTime.currentDateTime().addSecs(60 * 60),
		    sizePolicy=qtw.QSizePolicy(
		        qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Fixed
		    )
		)

		#TODO settings
		notification_label_info = qtw.QLabel(
		    "Notification",
		    sizePolicy=qtw.QSizePolicy(
		        qtw.QSizePolicy.MinimumExpanding, qtw.QSizePolicy.Fixed
		    ),
		    alignment=qtc.Qt.AlignRight | qtc.Qt.AlignTrailing | qtc.Qt.AlignVCenter
		)

		second_layout = qtw.QHBoxLayout()
		second_layout.addWidget(self.time_edit)
		second_layout.addWidget(notification_label_info)
		second_layout.addWidget(self.notification_choice)

		button_layout = qtw.QHBoxLayout()
		button_layout.addWidget(self.cancel_button)
		button_layout.addWidget(self.confirm_button)

		main_layout.addLayout(text_layout)
		main_layout.addLayout(second_layout)
		main_layout.addLayout(button_layout)

	def retranslate(self, settings: Settings):
		self.summary_line_edit.setPlaceholderText(settings.SUMMARY_TEXT)
		self.description_text_edit.setPlaceholderText(settings.DESCRIPTION_TEXT)
		self.cancel_button.setText(settings.CANCEL_BUTTON_TEXT)
		self.confirm_button.setText(settings.CONFIRM_BUTTON_TEXT)
		#TODO retranslate notification

	def _enforce_summary_not_empty(self):
		if len(self.summary_line_edit.text()
		       ) > 0 and not self.confirm_button.isEnabled():
			self.confirm_button.setEnabled(True)
		elif len(self.summary_line_edit.text()) == 0:
			self.confirm_button.setEnabled(False)

	def _enforce_text_edit_length(self, max_length: int):
		text = self.description_text_edit.toPlainText()
		if len(text) > max_length:
			self.description_text_edit.setPlainText(text[:max_length])
			#When changing text, cursor is moved to the beginning,
			#this moves it to the end
			cursor = self.description_text_edit.textCursor()
			cursor.setPosition(max_length)
			self.description_text_edit.setTextCursor(cursor)