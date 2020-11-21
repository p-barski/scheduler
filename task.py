from datetime import datetime


class Task:
	"""Model of a task saved in database."""
	def __init__(
	    self,
	    summary: str,
	    description: str,
	    _datetime: datetime,
	    notification: bool = False
	):
		#TODO ORM
		self.summary = summary
		self.description = description
		self.datetime = _datetime
		self.notification = notification