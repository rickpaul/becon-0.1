
class EMF_Word:
'''
A Word is a combination of a transformation and a predictor variable.

'''
	def __init__(self, db_conn, db_cursor):
		self.db_cursor = db_cursor
		self.db_conn = db_conn
		# Definitional Variables
		self.timeDelay = None
		self.transformationCode = None
		self.dataTicker = None
		self.dataID = None # ID of data undergoing transformation
		self.wordID = None # ID of word produced transformation
		# Meta Variables
		self.isStoredWord = None #TODO: Change to call.
		self.hasStats = None #TODO: Change to call.
		self.time_firstPredictorData = None
		self.time_finalPredictorData = None
		self.time_firstWord = None
		self.time_finalWord = None


	def __checkDB_HasStats(self):
		statement = 'select count(*)'


class EMF_WordSet:



class EMF_Framework:



	def set
