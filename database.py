from datetime import date
from typing import Tuple
from task import Task


class DB:
	"""Access to database."""
	def __init__(self):
		#TODO
		print(DB.__name__)
		self.tasks = []

	def get_tasks(self, date_filter: date) -> Tuple[Task, ...]:
		"""Returns tuple of tasks from given day."""
		#TODO
		print(f"{DB.__name__}:{self.get_tasks.__name__}:{date_filter}")
		return tuple(
		    sorted(
		        tuple(
		            task for task in self.tasks
		            if task.datetime.date() == date_filter
		        ),
		        key=lambda task: task.datetime
		    )
		)

	def save_task(self, task: Task):
		"""Saves task in database."""
		#TODO
		if task not in self.tasks:
			self.tasks.append(task)
		print(f"{DB.__name__}:{self.save_task.__name__}:{task}")

	def delete_task(self, task: Task):
		"""Deletes task from database."""
		#TODO
		self.tasks.remove(task)
		print(f"{DB.__name__}:{self.delete_task.__name__}:{task}")