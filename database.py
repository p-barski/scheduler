from datetime import date, timedelta
from typing import Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from task import Task


class DB:
	"""Access to database."""
	def __init__(self):
		self._db_name = "tasks.db"
		self._db_path = f"sqlite:///{self._db_name}"
		self._engine = create_engine(
		    self._db_path, echo=False, connect_args={'check_same_thread': False}
		)
		self._session = sessionmaker(bind=self._engine)()
		Task.__table__.create(bind=self._engine, checkfirst=True)

	def get_tasks(self, date_filter: date) -> Tuple[Task, ...]:
		"""Returns tuple of tasks from given day."""
		query = self._session.query(Task).filter(
		    Task.scheduled_date >= date_filter
		).filter(Task.scheduled_date <= date_filter + timedelta(days=1))
		return query.all()

	def save_task(self, task: Task):
		"""Saves task in database."""
		self._session.add(task)
		self._session.commit()

	def delete_task(self, task: Task):
		"""Deletes task from database."""
		self._session.delete(task)
		self._session.commit()