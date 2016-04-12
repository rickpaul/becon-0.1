# System 	Import...As
import 	sqlite3		as sq
import 	logging 	as log
# System 	From...Import
from 	os 			import remove

class EMF_Database_Handle(object):
	def __init__(self, dbLoc, deleteDB=False):
		'''
		CONSIDER:
					__conn and _cursor aren't passed by copy. Are they actually protected?
		'''
		raise Exception('This is not a usable handle. Connect using the MySQL or SQLite Handles.')

	def conn():
		doc = "The conn property."
		def fget(self):
			return self._conn
		return locals()
	conn = property(**conn())

	def cursor():
		doc = "The cursor property."
		def fget(self):
			return self._cursor
		return locals()
	cursor = property(**cursor())
