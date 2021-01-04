from datetime import date, timedelta
from time import sleep
from typing import Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from preferences import Preferences
from task import Task


#pylint: disable=no-member
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
		Preferences.__table__.create(bind=self._engine, checkfirst=True)

	def get_tasks(self, date_filter: date) -> Tuple[Task, ...]:
		"""Returns tuple of tasks from given day."""
		query = self._session.query(Task).filter(
		    Task.scheduled_date >= date_filter
		).filter(Task.scheduled_date <= date_filter + timedelta(days=1))
		while True:
			#This fixes exception when db is commiting changes
			#and another thread tries to access it
			try:
				return query.all()
			except InvalidRequestError:
				sleep(0.1)

	def save_task(self, task: Task):
		"""Saves task in database."""
		self._session.add(task)
		self._session.commit()

	def delete_task(self, task: Task):
		"""Deletes task from database."""
		self._session.delete(task)
		self._session.commit()

	def get_preferences(self) -> Preferences:
		"""Returns user's preferences saved in database or,
		if there is none, default preferences."""
		query = self._session.query(Preferences)
		try:
			return query.all()[0]
		except IndexError:
			return Preferences()

	def save_preferences(self, preferences: Preferences):
		preferences.default_preferences = False
		self._session.add(preferences)
		self._session.commit()