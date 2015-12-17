# System 	Import...As
import 	sqlite3		as sq
import 	logging 	as log
# System 	From...Import
from 	os 			import remove

class EMF_Database_Handle:
	def __init__(self, dbLocation, deleteDB=False):
		'''
		CONSIDER:
					__conn and __cursor aren't passed by copy. Are they actually protected?
		'''
		self.__dbLocation = dbLocation
		self.__conn = sq.connect(dbLocation)
		self.__cursor = self.__conn.cursor()
		self.__deleteDB = deleteDB
		log.info('Database %s opened.', self.__dbLocation)

	def __del__(self):
		self.__conn.close()
		log.info('Database %s closed.', self.__dbLocation)
		if self.__deleteDB:
			remove(self.__dbLocation)
			log.warning('Database %s deleted.', self.__dbLocation)


	def conn_(self):
		return self.__conn 

	def cursor_(self):
		return self.__cursor

	def dbLoc_(self):
		return self.__dbLocation