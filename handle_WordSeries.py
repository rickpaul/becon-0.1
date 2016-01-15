# TODOS:

# EMF 		From...Import
from 	lib_WordSeries	 		import DATE_COL, VALUE_COL, WORD_HISTORY_DTYPE
from 	lib_WordSeries	 		import TRANSFORMED, BASIS
from 	template_SerialHandle 	import EMF_Serial_Handle
from 	util_DB					import typify
from 	util_EMF				import dt_now_as_epoch
from 	util_EMF 				import dt_epoch_to_str_Y_M_D # Logging/Testing
from 	util_WordSeries			import generate_Word_Series_name
# EMF 		Import...As
import 	lib_DBInstructions 		as lib_DBInst
# System 	Import...As
import 	logging 				as log
import 	numpy 					as np

class EMF_WordSeries_Handle(EMF_Serial_Handle):
	def __init__(self, dbHandle, dataHandle, transformationHandle):
		self.hndl_DB = dbHandle
		self.hndl_Data = dataHandle
		self.hndl_Trns = transformationHandle
		self.wordSeriesID = lib_DBInst.retrieve_WordSeriesID(	self.hndl_DB.conn_(), 
																self.hndl_DB.cursor_(), 
																str(self),
																insertIfNot=True)
		self.__send_to_DB('int_data_series_ID', self.hndl_Data.seriesID)
		self.__send_to_DB('int_transformation_hash', self.hndl_Trns.trnsCode)
		self.stored_values = None
		self.stored_dates = None

	def __str__(self):
		return generate_Word_Series_name(str(self.hndl_Data), str(self.hndl_Trns))

	def __get_from_DB(self, column):
		return lib_DBInst.retrieve_WordSeriesMetaData(self.hndl_DB.cursor_(), column, self.wordSeriesID)

	def __send_to_DB(self, column, value):
		return lib_DBInst.update_WordSeriesMetaData(self.hndl_DB.conn_(), self.hndl_DB.cursor_(), column, value, self.wordSeriesID)

	def __generate_transformed_series(self):
		values = self.hndl_Trns.transform_data(self.hndl_Data.get_series_values())
		len_ = len(values)
		values = np.reshape(values, (len_, 1))
		dates = self.hndl_Trns.transform_time(self.hndl_Data.get_series_dates())
		dates = np.reshape(dates, (len_, 1))
		return (values, dates)

	def __get_transformed_series(self, regenerate=False):
		# If stored locally, Retrieve
		if self.__is_stored_local() and (not regenerate):
			return (self.stored_values, self.stored_dates)
		# If stored in DB, Retrieve Words from DB
		elif self.__is_stored_db() and (not regenerate):
			return self.__get_series_db()
		# If not stored, Generate Words
		else:
			return self.__generate_transformed_series()

	def get_values_transformed_filtered(self, min_, max_):
		(values, dates) = self.__get_transformed_series()
		filter_ = np.logical_and(dates>=min_, dates<=max_)
		strMin = dt_epoch_to_str_Y_M_D(min_) # Testing/Logging
		strMax = dt_epoch_to_str_Y_M_D(max_) # Testing/Logging
		len_ = sum(filter_) # Testing/Logging
		log.info('{3}\t: Found {0} words from {1} to {2}'.format(len_, strMin, strMax, self))
		strMin = dt_epoch_to_str_Y_M_D(dates[filter_][0]) # TEST: DELETE
		strMax = dt_epoch_to_str_Y_M_D(dates[filter_][-1]) # TEST: DELETE
		log.info('{3}\t: Found {0} words from {1} to {2}'.format(len_, strMin, strMax, self))
		return np.reshape(values[filter_], (len_, 1))

	def get_values_basis_filtered(self, min_, max_):
		'''
		gets untransformed values
		'''		
		return self.hndl_Data.get_series_values_filtered(min_, max_)

	def get_dates_basis_filtered(self, min_, max_):
		'''
		gets untransformed dates
		'''
		return self.hndl_Data.get_series_dates_filtered(min_, max_)

	def get_values_basis(self):
		'''
		gets untransformed values
		TODO: 
					Can fold this into _filtered by making min_, max_ named params
		'''		
		return self.hndl_Data.get_series_values()

	def get_dates_basis(self):
		'''
		gets untransformed dates
		TODO: 
					Can fold this into _filtered by making min_, max_ named params
		'''
		return self.hndl_Data.get_series_dates()

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
		self.__send_to_DB('dt_history_last_accessed', dt_now_as_epoch())

	def __set_word_is_stored(self, isStored):
		self.__send_to_DB('bool_word_is_stored', int(isStored))

	def __is_stored_db(self):
		typify(bool, self.__get_from_DB('bool_word_is_stored'))

	def get_model_categorization(self):
		if self.hndl_Data.get_categorical():
			if self.hndl_Trns.is_bounded:
				return 'categorical_bounded'
			else:
				return 'categorical_unbounded'
		else:
			return 'continuous'

	def get_min_date_transformed(self):
		min_ = self.hndl_Data.get_earliest_date()
		periodicity = self.hndl_Data.get_periodicity()
		return self.hndl_Trns.transform_earliest_time(min_, periodicity)

	def get_max_date_transformed(self):
		max_ = self.hndl_Data.get_latest_date()
		periodicity = self.hndl_Data.get_periodicity()
		return self.hndl_Trns.transform_latest_time(max_, periodicity)

	def get_min_date_basis(self): # Deletable
		return self.hndl_Data.get_earliest_date()

	def get_max_date_basis(self): # Deletable
		return self.hndl_Data.get_latest_date()
		
	def get_date_limits(self, mode=TRANSFORMED):
		if mode == TRANSFORMED:
			return (self.get_min_date_transformed(), self.get_max_date_transformed())
		elif mode == BASIS:
			return (self.get_min_date_basis(), self.get_max_date_basis())
		else:
			raise NameError

	def log_self(self):  # Deletable
		limits = map(dt_epoch_to_str_Y_M_D, self.get_date_limits(mode=TRANSFORMED))
		log.info('WORDSERIES : Transformed word limits: {0} to {1}'.format(*limits))
		limits = map(dt_epoch_to_str_Y_M_D, self.get_date_limits(mode=BASIS))
		log.info('WORDSET : training word limits: {0} to {1}'.format(*limits))


	def __get_series_db(self):
		'''
		CONSIDER:
					We should check for transformation complexity. 
						It may be quicker to not access the db and just regenerate.
		'''	
		series = lib_DBInst.getCompleteWordHistory_WordHistoryTable(self.hndl_DB.cursor_(), 
																	self.wordSeriesID)
		series = np.asarray(dtype=WORD_HISTORY_DTYPE)
		(len_, ) = wordSeries.shape
		values = np.reshape(series[VALUE_COL], (len_, 1))
		dates = np.reshape(series[DATE_COL], (len_, 1))
		return (values, dates)

	def __save_value_db(self, date, value):
		'''
		TODOS: 
					- Make a version that takes more than one value (i.e. don't have to call this repeatedly.)
		'''
		return lib_DBInst.insertWordPoint_WordHistoryTable( self.hndl_DB.conn_(), 
															self.hndl_DB.cursor_(), 
															self.wordSeriesID, 
															date, 
															value)

	def save_series_db(self):
		'''

		TODOS: 
					++ Deal with None values
					++ Make roll back non-automatic 
					+ Store Data on successful inserts, maxDateEncountered, etc.
		'''
		(values, dates) = self.__get_transformed_series(regenerate=True)
		successfulInserts = 0
		unsuccessfulInserts = 0
		for i in xrange(dataLen):
			success = self.__save_value_db(dates[i], values[i])
			if not success:
				log.warning('Failed to Write Historical Word Point at %s for %s [value = %f]', self.wordSeriesTicker, dates[i], values[i])
				unsuccessfulInserts += 1
				break
			else:
				successfulInserts +=1
		# Roll Back Insert If Necessary
		if unsuccessfulInserts == 0:
			self.__set_word_is_stored(True)
		else:
			self.delete_word_history()
		log.info('Successfully/Unsuccessfully wrote %d/%d Historical Word Points for %s', successfulInserts, unsuccessfulInserts, self.wordSeriesTicker)
		return (successfulInserts, unsuccessfulInserts)

	def delete_series_db(self):
		'''
		deletes word history from Database
		'''
		raise NotImplementedError
		self.__send_to_DB(self, 'bool_word_is_stored', 0)
		log.info('Deleting Word History for %s', self.wordSeriesTicker)

	# def get_dates_transformed_filtered(self, min_, max_):
	# 	(values, dates) = self.__get_transformed_series()
	# 	filter_ = np.logical_and(dates>=min_, dates<=max_)
	# 	return np.reshape(dates[filter_], (sum(filter_), 1))

	# def get_series_dates_original(self, min_, max_):
	# 	return self.hndl_Data.get_series_dates_filtered(min_, max_)
