# TODOS:
# 	This should probably be a pandas dataframe

# EMF 		From...Import
from 	lib_WordSeries	 		import DATE_COL, VALUE_COL, WORD_HISTORY_DTYPE
# from 	template_SerialHandle 	import EMF_Serial_Handle
from 	util_DB					import typify
from 	util_TimeSet			import dt_now_as_epoch
from 	util_WordSeries			import generate_Word_Series_name, generate_Word_Series_generic_desc
from 	util_WordSeries			import generate_Word_Series_categorical_desc
# EMF 		Import...As
import 	lib_DBInstructions 		as lib_DBInst
# System 	Import...As
import 	logging 				as log
import 	numpy 					as np
# System 	From...Import
from 	copy 					import deepcopy 

class EMF_WordSeries_Handle(object):
	def __init__(self, dbHandle, dataHandle, transformationHandle):
		self.hndl_DB = dbHandle
		self.hndl_Data = dataHandle
		self.hndl_Trns = transformationHandle
		self._hndl_Time = None
		self._wordSeriesID = lib_DBInst.retrieve_WordSeriesID(	self.hndl_DB.conn, 
																self.hndl_DB.cursor, 
																str(self),
																insertIfNot=True)
		self.__save_metadata('int_data_series_ID', self.hndl_Data.seriesID)
		self.__save_metadata('int_transformation_hash', self.hndl_Trns.code)
		self.stored_values = None
		self.stored_dates = None


	def __load_metadata(self, column):
		return lib_DBInst.retrieve_WordSeriesMetaData(self.hndl_DB.cursor, column, self.wordSeriesID)

	def __save_metadata(self, column, value):
		return lib_DBInst.update_WordSeriesMetaData(self.hndl_DB.conn, self.hndl_DB.cursor, column, value, self.wordSeriesID)

	def __str__(self):
		return generate_Word_Series_name(self.hndl_Data, self.hndl_Trns)
		
	__repr__ = __str__

	def wordSeriesID():
		doc = "The wordSeriesID property."
		def fget(self):
			return self._wordSeriesID
		return locals()
	wordSeriesID = property(**wordSeriesID())

	def dataSeriesID():
		doc = "The dataSeriesID property."
		def fget(self):
			return self.hndl_Data.seriesID
		return locals()
	dataSeriesID = property(**dataSeriesID())

	def trns_name():
		doc = "The trns_name property."
		def fget(self):
			return self.hndl_Trns.name
		return locals()
	trns_name = property(**trns_name())

	def trns_code():
		doc = "The trns_code property."
		def fget(self):
			return self.hndl_Trns.code
		return locals()
	trns_code = property(**trns_code())

	def data_name():
		doc = "The data_name property."
		def fget(self):
			return self.hndl_Data.name
		return locals()
	data_name = property(**data_name())

	def data_ticker():
		doc = "The data_ticker property."
		def fget(self):
			return self.hndl_Data.ticker
		return locals()
	data_ticker = property(**data_ticker())

	def desc():
		def fget(self):
			return generate_Word_Series_generic_desc(self.hndl_Data, self.hndl_Trns)
		return locals()
	desc = property(**desc())

	def cat_desc():
		def fget(self):
			return generate_Word_Series_categorical_desc(self.hndl_Data, self.hndl_Trns)
		return locals()
	cat_desc = property(**cat_desc())

	def min_date():
		doc = "Minimum date post-transformation"
		def fget(self):
			return self.hndl_Time.startEpoch
		return locals()
	min_date = property(**min_date())

	def max_date():
		doc = "Maximum date post-transformation"
		def fget(self):
			return self.hndl_Time.endEpoch
		return locals()
	max_date = property(**max_date())

	def dates():
		doc = "The dates property."
		def fget(self):
			return self.get_series_dates()
		return locals()
	dates = property(**dates())

	def values():
		doc = "The values property."
		def fget(self):
			return self.get_series_values()
		return locals()
	values = property(**values())

	# Is this sloppy? Yes.
	def hndl_Time():
		doc = "Time Handle"
		def fget(self):
			if self._hndl_Time is None:
				self._hndl_Time = deepcopy(self.hndl_Data.hndl_Time)
				self.hndl_Trns.transform_time(self._hndl_Time)
			return self._hndl_Time
		return locals()
	hndl_Time = property(**hndl_Time())

	# Is this sloppy? Yes.
	def hndl_Time_Raw():
		doc = "Time Handle"
		def fget(self):
			return self.hndl_Data.hndl_Time
		return locals()
	hndl_Time_Raw = property(**hndl_Time_Raw())

	def category(): #Necessary?
		doc = "The category property."
		def fget(self):
			return self.hndl_Data.category
		return locals()
	category = property(**category())

	def subcategory(): #Necessary?
		doc = "The subcategory property."
		def fget(self):
			return self.hndl_Data.subcategory
		return locals()
	subcategory = property(**subcategory())

	def category_meaning(): #Necessary?
		doc = "The category_meaning property."
		def fget(self):
			return self.hndl_Data.category_meaning
		return locals()
	category_meaning = property(**category_meaning())

	def prediction_requires_raw_data(self):
		return self.hndl_Trns.prediction_is_value_dependent()

	def get_raw_values(self):
		return self.hndl_Data.get_series_values()

	def get_raw_dates(self):
		return np.array(self.hndl_Data.hndl_Time.get_dates())

	def __generate_transformed_series(self):
		values = self.hndl_Trns.transform_data(self.hndl_Data.get_series_values()).reshape(-1,1)
		dates = self.hndl_Time.get_dates().reshape(-1,1)
		return (values, dates)

	# Pretty sloppy. Should just break it up.
	def __get_transformed_series(self, regenerate=False):
		# If stored locally, Retrieve
		if (not regenerate) and self.__is_stored_local():
			return (self.stored_values, self.stored_dates)
		# If stored in DB, Retrieve Words from DB
		elif (not regenerate) and self.__is_stored_db():
			return self.__get_series_db()
		# If not stored, Generate Words
		else:
			return self.__generate_transformed_series()

	def get_series_values(self):
		'''
		IMPLEMENTATION OF MODEL TEMPLATE
		'''
		return self.__get_transformed_series()[0]

	def get_series_dates(self):
		'''
		IMPLEMENTATION OF MODEL TEMPLATE
		'''
		return self.__get_transformed_series()[1]
		
	def save_series_local(self, regenerate=True):
		(self.stored_values, self.stored_dates) = self.__get_transformed_series(regenerate=regenerate)

	def __is_stored_local(self):
		return (self.stored_values is not None and self.stored_dates is not None) 

	def __set_last_accessed(self):
		self.__save_metadata('dt_history_last_accessed', dt_now_as_epoch())

	def __set_word_is_stored(self, isStored):
		self.__save_metadata('bool_word_is_stored', int(isStored))

	def __is_stored_db(self):
		typify(bool, self.__load_metadata('bool_word_is_stored'))

	def get_model_categorization(self):
		if self.hndl_Data.is_categorical:
			if self.hndl_Trns.is_bounded:
				return 'categorical_bounded'
			else:
				return 'categorical_unbounded'
		else:
			return 'continuous'

	# def __get_series_db(self):
	# 	'''
	# 	CONSIDER:
	# 				We should check for transformation complexity. 
	# 					It may be quicker to not access the db and just regenerate.
	# 	'''	
	# 	series = lib_DBInst.getCompleteWordHistory_WordHistoryTable(self.hndl_DB.cursor, 
	# 																self.wordSeriesID)
	# 	series = np.asarray(dtype=WORD_HISTORY_DTYPE)
	# 	values = series[VALUE_COL].reshape(-1,1)
	# 	dates = series[DATE_COL].reshape(-1,1)
	# 	return (values, dates)

	# def __save_value_db(self, date, value):
	# 	'''
	# 	TODOS: 
	# 				- Make a version that takes more than one value (i.e. don't have to call this repeatedly.)
	# 	'''
	# 	return lib_DBInst.insertWordPoint_WordHistoryTable( self.hndl_DB.conn, 
	# 														self.hndl_DB.cursor, 
	# 														self.wordSeriesID, 
	# 														date, 
	# 														value)

	# def save_series_db(self):
	# 	'''

	# 	TODOS: 
	# 				++ Deal with None values
	# 				++ Make roll back non-automatic 
	# 				+ Store Data on successful inserts, maxDateEncountered, etc.
	# 	'''
	# 	(values, dates) = self.__get_transformed_series(regenerate=True)
	# 	successfulInserts = 0
	# 	unsuccessfulInserts = 0
	# 	for i in xrange(dataLen):
	# 		success = self.__save_value_db(dates[i], values[i])
	# 		if not success:
	# 			log.warning('Failed to Write Historical Word Point at %s for %s [value = %f]', self.wordSeriesTicker, dates[i], values[i])
	# 			unsuccessfulInserts += 1
	# 			break
	# 		else:
	# 			successfulInserts +=1
	# 	# Roll Back Insert If Necessary
	# 	if unsuccessfulInserts == 0:
	# 		self.__set_word_is_stored(True)
	# 	else:
	# 		self.delete_word_history()
	# 	log.info('Successfully/Unsuccessfully wrote %d/%d Historical Word Points for %s', successfulInserts, unsuccessfulInserts, self.wordSeriesTicker)
	# 	return (successfulInserts, unsuccessfulInserts)

	# def delete_series_db(self):
	# 	'''
	# 	deletes word history from Database
	# 	'''
	# 	raise NotImplementedError
	# 	self.__save_metadata(self, 'bool_word_is_stored', 0)
	# 	log.info('Deleting Word History for %s', self.wordSeriesTicker)
