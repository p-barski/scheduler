from threading import Thread, Event
from datetime import datetime, timedelta
from typing import Final
from notifypy import Notify
from database import DB


class TaskFilter:
	"""Filters tasks for notification."""
	def __init__(self, sleep_time: int):
		self.sleep_time: Final[int] = sleep_time

	def __call__(self, task) -> bool:
		if task.notification == 0:
			return False
		time_diff = task.datetime - datetime.now()
		upper_bound = timedelta(seconds=60 * task.notification)
		lower_bound = timedelta(
		    seconds=60 * task.notification - self.sleep_time * 1.5
		)
		return upper_bound >= time_diff >= lower_bound


class Notifier:
	"""Checks tasks in database and sends notification when needed."""
	SLEEP_TIME: Final[int] = 20

	def __init__(self, db: DB, notification_title: str):
		self._db = db
		self._cancel_event = Event()
		self._thread = Thread(target=self._notification_loop)
		self._filter = TaskFilter(self.SLEEP_TIME)
		self._notification = Notify()
		self._notification.title = notification_title

	def __del__(self):
		self.stop()

	def start(self):
		"""Starts notifying thread."""
		self._thread.start()

	def stop(self):
		"""Stops notifying thread."""
		self._cancel_event.set()
		self._thread.join()

	def retranslate(self, notification_title: str):
		"""Changes notification title."""
		self._notification.title = notification_title

	def _notification_loop(self):
		while not self._cancel_event.is_set():
			tasks = self._db.get_tasks(datetime.now().date())
			tasks = (task for task in tasks if self._filter(task))
			for task in tasks:
				self._notification.message = task.summary
				self._notification.send()
			self._cancel_event.wait(self.SLEEP_TIME)