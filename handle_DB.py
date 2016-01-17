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
		self._dbLoc = dbLoc
		self._conn = sq.connect(dbLoc)
		self._cursor = self._conn.cursor()
		self._deleteDB = deleteDB
		log.info('Database %s opened.', self._dbLoc)

	def __del__(self):
		self._conn.close()
		log.info('Database %s closed.', self._dbLoc)
		if self._deleteDB:
			remove(self._dbLoc)
			log.warning('Database %s deleted.', self._dbLoc)

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

	def dbLoc():
		doc = "The dbLoc property."
		def fget(self):
			return self._dbLoc
		return locals()
	dbLoc = property(**dbLoc())