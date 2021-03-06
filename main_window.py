from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from task import Task
from task_widget import TaskWidgetFactory
from day_widget import DayWidgetFactory
from monthly_view import MonthlyViewWidget
from task_viewing import TaskViewingWidget
from task_creation import TaskCreationWidget
from task_edition import TaskEditionWidget
from ui_settings import Settings
from notifier import Notifier
from database import DB


class MainWindow(qtw.QMainWindow):
	"""Main window of an application."""
	task_deleted_event = qtc.pyqtSignal()

	def __init__(self):
		super().__init__()
		self.db = DB()
		self.preferences = self.db.get_preferences()
		self.settings = Settings(self.preferences.language)

		try:
			self.notifier = Notifier(self.db, self.settings.NOTIFICATION_TITLE)
			self.notifier.start()
		except BaseException as e:
			popup_window = qtw.QMessageBox(
			    windowTitle="Notification error", text=str(e)
			)
			popup_window.exec_()
		self.factory = TaskWidgetFactory(
		    self.settings, self._switch_to_task_editing, self._delete_task
		)
		self.day_factory = DayWidgetFactory(self.db, self._pick_day)

		main_widget = qtw.QWidget()
		main_layout = qtw.QVBoxLayout()
		main_widget.setLayout(main_layout)
		self.setCentralWidget(main_widget)

		self.task_viewing = TaskViewingWidget(
		    self.settings, self.db, self._switch_to_task_creation,
		    self._switch_to_monthly_view, self.task_deleted_event, self.factory
		)
		self.monthly_view = MonthlyViewWidget(self.settings, self.day_factory)

		self.task_creation = TaskCreationWidget(
		    self.settings, self.db, self._switch_to_task_viewing
		)

		self.task_edition = TaskEditionWidget(
		    self.settings, self.db, self._switch_to_task_viewing
		)

		main_layout.addWidget(self.task_viewing)
		main_layout.addWidget(self.monthly_view)
		main_layout.addWidget(self.task_creation)
		main_layout.addWidget(self.task_edition)

		#Menu bar
		self._change_to_pl = qtw.QAction(
		    f"{self.settings.LANGUAGE_TEXT} - PL", self
		)
		self._change_to_pl.triggered.connect(lambda: self.retranslate("PL"))
		self._change_to_eng = qtw.QAction(
		    f"{self.settings.LANGUAGE_TEXT} - ENG", self
		)
		self._change_to_eng.triggered.connect(lambda: self.retranslate("ENG"))

		menu_bar = self.menuBar()
		self._options_menu = menu_bar.addMenu(self.settings.MENU_OPTIONS)
		self._options_menu.addAction(self._change_to_pl)
		self._options_menu.addAction(self._change_to_eng)

		self.setWindowTitle(self.settings.WINDOW_TITLE)

		self.resize(self.preferences.width, self.preferences.height)
		if self.preferences.default_preferences:
			self._center_window()
		elif self.preferences.maximised:
			self.showMaximized()
		else:
			self.move(self.preferences.x_offset, self.preferences.y_offset)

		self._switch_to_task_viewing()

	def retranslate(self, language: str):
		self.settings = Settings(language)
		self.preferences.language = language
		self.task_edition.retranslate(self.settings)
		self.task_creation.retranslate(self.settings)
		self.task_viewing.retranslate(self.settings)
		self.monthly_view.retranslate(self.settings)
		self._options_menu.setTitle(self.settings.MENU_OPTIONS)
		self._change_to_pl.setText(f"{self.settings.LANGUAGE_TEXT} - PL")
		self._change_to_eng.setText(f"{self.settings.LANGUAGE_TEXT} - ENG")
		try:
			self.notifier.retranslate(self.settings.NOTIFICATION_TITLE)
		except AttributeError:
			pass

	def closeEvent(self, event):
		"""Overridden method, called when closing widget."""
		self.db.save_preferences(self.preferences)
		try:
			self.notifier.stop()
		except AttributeError:
			pass

	def resizeEvent(self, event):
		self._update_preferences()

	def moveEvent(self, event):
		self._update_preferences()

	def _switch_to_task_creation(self):
		self.task_viewing.hide()
		self.task_edition.hide()
		self.monthly_view.hide()
		self.task_creation.show()

	def _switch_to_task_viewing(self):
		self.task_creation.hide()
		self.task_edition.hide()
		self.monthly_view.hide()
		self.task_viewing.show()

	def _switch_to_task_editing(self, task: Task):
		self.task_creation.hide()
		self.task_viewing.hide()
		self.monthly_view.hide()
		self.task_edition.set_task(task)
		self.task_edition.show()

	def _switch_to_monthly_view(self):
		self.task_creation.hide()
		self.task_edition.hide()
		self.task_viewing.hide()
		self.monthly_view.show()

	def _pick_day(self, day):
		self.task_viewing.change_day(day)
		self._switch_to_task_viewing()

	def _delete_task(self, task: Task):
		self.db.delete_task(task)
		self.task_deleted_event.emit()

	def _center_window(self):
		qtRectangle = self.frameGeometry()
		centerPoint = qtw.QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())
		self._update_preferences()

	def _update_preferences(self):
		geometry = self.frameGeometry()
		self.preferences.x_offset = geometry.left()
		self.preferences.y_offset = geometry.top()
		self.preferences.width = geometry.width()
		self.preferences.height = geometry.height()
		self.preferences.maximised = self.isMaximized()


if __name__ == "__main__":
	app = qtw.QApplication([])
	ui = MainWindow()
	ui.show()
	app.exec_()