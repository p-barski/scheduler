from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
BaseClass = declarative_base()


class Preferences(BaseClass):
	"""User's preferences stored in database."""
	__tablename__ = "preferences"
	id = Column(Integer, primary_key=True)

	language = Column(String)
	width = Column(Integer)
	height = Column(Integer)
	x_offset = Column(Integer)
	y_offset = Column(Integer)
	maximised = Column(Boolean)
	default_preferences = Column(Boolean)

	def __init__(self):
		#Default values
		self.language = "ENG"
		self.width = 1280
		self.height = 720
		self.x_offset = 0
		self.y_offset = 0
		self.maximised = False
		self.default_preferences = True