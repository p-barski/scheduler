from typing import Final


class Task:
	"""Model of a task saved in database."""
	def __init__(self, summary: str, description: str):
		#TODO ORM
		#TODO dates
		self.summary: Final[str] = summary
		self.description: Final[str] = description
