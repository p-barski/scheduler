from unittest import TestCase
from unittest.main import main
from datetime import datetime, timedelta
from collections import namedtuple
from random import randint
from notifier import TaskFilter

Task = namedtuple("Task", ("datetime", "notification"))


class TaskFilterTests(TestCase):
	def test_no_notification_1(self):
		for _ in range(5000):
			sleep_time = randint(3, 59)
			notification_time = 0
			filter_obj = TaskFilter(sleep_time)
			offset = (60 * -notification_time) + sleep_time

			task = Task(datetime.now() + timedelta(seconds=offset), notification_time)
			self.assertFalse(filter_obj(task))

	def test_no_notification_2(self):
		for _ in range(5000):
			sleep_time = randint(3, 59)
			notification_time = 0
			filter_obj = TaskFilter(sleep_time)
			offset = randint(
			    (60 * notification_time), (60 * notification_time) * 2000
			)

			task = Task(datetime.now() + timedelta(seconds=offset), notification_time)
			self.assertFalse(filter_obj(task))

	def test_notification_1(self):
		for _ in range(5000):
			sleep_time = randint(3, 59)
			notification_time = randint(1, 120)
			filter_obj = TaskFilter(sleep_time)
			offset = (60 * notification_time) - (sleep_time / 2)

			task = Task(datetime.now() + timedelta(seconds=offset), notification_time)
			self.assertTrue(filter_obj(task))

	def test_notification_2(self):
		for _ in range(5000):
			sleep_time = randint(3, 59)
			notification_time = randint(1, 120)
			filter_obj = TaskFilter(sleep_time)
			offset = -(60 * notification_time) + (sleep_time / 2)

			task = Task(datetime.now() + timedelta(seconds=offset), notification_time)
			self.assertFalse(filter_obj(task))

	def test_notification_3(self):
		for _ in range(5000):
			sleep_time = randint(3, 59)
			notification_time = randint(1, 120)
			filter_obj = TaskFilter(sleep_time)
			offset = -randint(0, 2000)

			task = Task(datetime.now() + timedelta(seconds=offset), notification_time)
			self.assertFalse(filter_obj(task))

	def test_notification_4(self):
		for _ in range(5000):
			sleep_time = randint(3, 59)
			notification_time = randint(1, 120)
			filter_obj = TaskFilter(sleep_time)
			offset = randint(
			    (60 * notification_time), (60 * notification_time) * 2000
			)

			task = Task(datetime.now() + timedelta(seconds=offset), notification_time)
			self.assertFalse(filter_obj(task))


if __name__ == "__main__":
	main()