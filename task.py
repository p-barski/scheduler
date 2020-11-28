from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
BaseClass = declarative_base()


class Task(BaseClass):
	"""Model of a task saved in database."""
	__tablename__ = "task"
	id = Column(Integer, primary_key=True)

	summary = Column(String)
	description = Column(String)
	scheduled_date = Column(DateTime)
	notification = Column(Integer)

	def __init__(
	    self, summary: str, description: str, _datetime: datetime,
	    notification: int
	):
		self.summary = summary
		self.description = description
		self.scheduled_date = _datetime
		self.notification = notification

	def __str__(self):
		string = f"{self.summary} scheduled at {self.scheduled_date}"
		if self.notification != 0:
			return f"{string}, with notification at {self.notification}"
		return string

	def __repr__(self):
		return f"Task({self.summary}, {self.description}, {self.scheduled_date}, {self.notification})"
