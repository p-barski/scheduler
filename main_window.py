from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from task import Task
from task_widget import TaskWidgetFactory
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
		self.settings = Settings("ENG")
		self.db = DB()
		self.notifier = Notifier(self.db, self.settings.NOTIFICATION_TITLE)
		self.notifier.start()
		self.factory = TaskWidgetFactory(
		    self.settings, self._switch_to_task_editing, self._delete_task
		)

		self.setWindowTitle(self.settings.WINDOW_TITLE)
		self.resize(self.settings.WINDOW_WIDTH, self.settings.WINDOW_HEIGHT)

		main_widget = qtw.QWidget()
		main_layout = qtw.QVBoxLayout()
		main_widget.setLayout(main_layout)
		self.setCentralWidget(main_widget)

		self.task_viewing = TaskViewingWidget(
		    self.settings, self.db, self._switch_to_task_creation,
		    self.task_deleted_event, self.factory
		)

		self.task_creation = TaskCreationWidget(
		    self.settings, self.db, self._switch_to_task_viewing
		)

		self.task_edition = TaskEditionWidget(
		    self.settings, self.db, self._switch_to_task_viewing
		)
		self.task_edition.cancel_button.clicked.connect(
		    self._switch_to_task_viewing
		)

		main_layout.addWidget(self.task_viewing)
		main_layout.addWidget(self.task_creation)
		main_layout.addWidget(self.task_edition)

		self._switch_to_task_viewing()

		#Centering window
		qtRectangle = self.frameGeometry()
		centerPoint = qtw.QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())

	def retranslate(self, settings: Settings):
		self.task_edition.retranslate(settings)
		self.task_creation.retranslate(settings)
		self.task_viewing.retranslate(settings)
		self.notifier.retranslate(settings.NOTIFICATION_TITLE)

	def closeEvent(self, event):
		"""Overridden method, called when closing widget."""
		self.notifier.stop()

	def _switch_to_task_creation(self):
		self.task_viewing.hide()
		self.task_edition.hide()
		self.task_creation.show()

	def _switch_to_task_viewing(self):
		self.task_creation.hide()
		self.task_edition.hide()
		self.task_viewing.show()

	def _switch_to_task_editing(self, task: Task):
		self.task_creation.hide()
		self.task_viewing.hide()
		self.task_edition.set_task(task)
		self.task_edition.show()

	def _delete_task(self, task: Task):
		self.db.delete_task(task)
		self.task_deleted_event.emit()


if __name__ == "__main__":
	app = qtw.QApplication([])
	ui = MainWindow()
	ui.show()
	app.exec_()