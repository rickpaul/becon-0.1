# TODO:
# 	Add TimeSet Handle to manage/verify time
# 	Create Test
# 	Keys (Column Names) should always be strings

# EMF 		From...Import
from 	template_ColumnArray 	import EMF_ColumnArray_Template
from 	util_JSON 				import save_to_JSON, load_from_JSON
# System 	Import...As
import 	logging 				as log
import 	numpy	 				as np
import 	pandas	 				as pd
import 	pickle


class EMF_ColumnArray_Handle(EMF_ColumnArray_Template):
	def __init__(self, save_to_file=False):
		self._max_size = None
		#
		self._col_index = 1
		self._col_array = None
		self._col_metadata = None
		# self._col_scores = None
		#
		self._save_to_file = save_to_file
	
	def metadata_file_path():
		doc = "UNIMPLEMENTED"
		return locals()
	metadata_file_path = property(**metadata_file_path())

	def array_file_path():
		doc = "UNIMPLEMENTED"
		return locals()
	array_file_path = property(**array_file_path())

	def save_to_file():
		doc = "The save_to_file property."
		def fget(self):
			return self._save_to_file
		def fset(self, value):
			self._save_to_file = value
		return locals()
	save_to_file = property(**save_to_file())

	def max_size():
		doc = "The max_size property."
		def fget(self):
			return self._max_size
		def fset(self, value):
			self._max_size = value
		return locals()
	max_size = property(**max_size())

	def col_index():
		doc = ""
		def fget(self):
			return self._col_index
		def fset(self, value):
			self._col_index = value
		return locals()
	col_index = property(**col_index())
	
	def col_metadata():
		doc = ""
		def fget(self):
			if self._col_metadata is None:
				self._col_metadata = {}
			return self._col_metadata
		def fset(self, value):
			self._col_metadata = value
		def fdel(self):
			self._col_metadata = None
		return locals()
	col_metadata = property(**col_metadata())

	def col_array():
		doc = ""
		def fget(self):
			if self._col_array is None:
				self._col_array = pd.DataFrame()
			return self._col_array
		def fset(self, value):
			self._col_array = value
		def fdel(self):
			self._col_array = None
		return locals()
	col_array = property(**col_array())

	def __del__(self):
		self.save()

	################################ Add Columns
	def add_column(self, dates, values, key=None, force=False):
		'''
		TODO:
					Verify that force is working in pd
		'''
		# Get Key if Necessary
		if key is None:
			key = self.col_index
		# Add Data to Column Array
		if key in self.col_array:
			log.info('{0}: {1} already in Column Array.'.format(self.log_prefix, key))
			# Add Data to Column Array / Return if Exists and Not Force
			if not force:
				return
			# Add Data to Column Array / Overwrite Column if Force
			else:
				newDF = pd.DataFrame({key:values.ravel()}, index=dates.ravel())
				# Look into df1.update(df2) instead of delete/write
				del self.col_array[key]
				self.col_array = pd.concat([self.col_array, newDF], axis=1, ignore_index=False)
				log.debug('{0}: Added {1} points, overwriting {2} in Column Array.'.format(self.log_prefix, len(newDF), key))
		else:
			# Add Data to Column Array / Add Column
			newDF = pd.DataFrame({key:values.ravel()}, index=dates.ravel())
			self.col_array = pd.concat([self.col_array, newDF], axis=1, ignore_index=False)
			log.debug('{0}: Added {1} points for {2} to Column Array.'.format(self.log_prefix, len(newDF), key))
			# self._hndl_Time = max_time_handle_merge(hndl_Word.hndl_Time, self._hndl_Time) # WARNING! Doesn't work if we truncate an end. Forcing messes w it.

	def add_metadata(self, metadata, key=None, force=False):
		# Get Key if Necessary
		if key is None:
			key = str(self.col_index)
		else:
			key = str(key)
		# Add Data to Metadata Dictionary
		if key in self.col_metadata:
			log.info('{0}: {1} already in Column Metadata.'.format(self.log_prefix, key))
			if not force:
				return
			else:
				self.col_metadata[key] = metadata
				log.debug('{0}: Overwriting {2} in Column Metadata.'.format(self.log_prefix, key))
		else:
			self.col_metadata[key] = metadata
			log.info('{0}: Added {1} to Column Metadata.'.format(self.log_prefix, key))

	################################ Delete Columns
	def delete_column(self, col_key, expect_metadata=True):
		try:
			del self.col_array[col_key]
			log.debug('{0}: Deleted {1} from word array'.format(self.log_prefix, col_key))
		except KeyError:
			log.debug('{0}: Unable to delete {1} from word array'.format(self.log_prefix, col_key))
		if expect_metadata:
			try:
				del self.col_metadata[str(col_key)]
				log.debug('{0}: Deleted {1} from metadata'.format(self.log_prefix, col_key))
			except KeyError:
				log.debug('{0}: Unable to delete {1} from metadata'.format(self.log_prefix, col_key))

	################################ Get PD Series
	def get_series_by_col(self, col_key, filter_nulls=True):
		if filter_nulls:
			return self.col_array.loc[self.get_is_not_null_filter(col_key), col_key]
		else:
			return self.col_array[col_key]		

	################################ Get Values
	def get_values_by_row(self, row_index):
		row_ = self.col_array.ix[row_index]
		filter_ = ~row_.isnull()
		row_ = row_[filter_]
		col_indexes = np.array(row_.index)
		values = np.array(row_)
		return (col_indexes, values)

	def get_values_by_col(self, col_key, filter_nulls=True, values_only=False):
		'''
		TODO:
				Test if use of loc fn is correct
				Can this be done more efficiently?
				A little sloppy. What does it return; a tuple or an array?
		'''
		if filter_nulls:
			col_ = self.col_array.loc[self.get_is_not_null_filter(col_key), col_key]
		else:
			col_ = self.col_array[col_key]
		values = np.array(col_)
		if values_only:
			return values
		row_indexes = np.array(col_.index)
		return (row_indexes, values)

	def get_values_by_col_filtered(self, col_key, filter_, values_only=False):
		'''
		TODO:
				Test if use of loc fn is correct
				A little sloppy. What does it return; a tuple or an array?
		'''
		col_ = self.col_array.loc[filter_, col_key]
		values = np.array(col_)
		if values_only:
			return values
		row_indexes = np.array(col_.index)
		return (row_indexes, values)

	def get_is_not_null_filter(self, col_key):
		'''
		TODO:
				Turn this into a cache to keep common filters
		'''
		return ~self.col_array[col_key].isnull()

	################################ File Saving/Loading
	def load(self):
		if self.save_to_file:
			self.load_array()
			self.load_metadata()

	def save(self):
		'''
		TODO:
					Can we make this save atomic? I.e. it rolls back save if not happy/fails for error?
		'''
		if self.save_to_file:
			self.save_array()
			self.save_metadata()

	def load_array(self):
		try:
			log.info('{0}: Loading Prediction Array from {1}'.format(self.log_prefix, self.array_file_path))
			self.col_array = pickle.load( open( self.array_file_path, "rb" ) )
			if self.col_array is not None:
				log.warning('{0}: Loading over an existing Column Array.'.format(self.log_prefix))
		except Exception, e:
			log.warning('{0}: Failed to load Column Array.'.format(self.log_prefix))
			log.warning(e)
			log.warning('{0}: File path was: {1}'.format(self.log_prefix, self.array_file_path))

	def load_metadata(self):
		try:
			log.info('{0}: Loading Column Metadata.'.format(self.log_prefix))
			self.__dict__.update(load_from_JSON(self.metadata_file_path))
		except Exception, e:
			log.warning('{0}: Failed to load Column Metadata.'.format(self.log_prefix))
			log.warning(e)
			log.warning('{0}: File path was: {1}'.format(self.log_prefix, self.array_file_path))

	def save_array(self):
		try:
			log.info('{0}: Saving prediction array pickle to {1}'.format(self.log_prefix, self.array_file_path))
			self.col_array.to_pickle(self.array_file_path)
		except Exception, e:
			log.warning('{0}: Failed to save Column Array.'.format(self.log_prefix))
			log.warning(e)
			log.warning('{0}: File path was: {1}'.format(self.log_prefix, self.array_file_path))
			raise e

	def save_metadata(self):
		try:
			json_ = {
				'_col_index' 	: self.col_index,
				'_col_metadata'	: self.col_metadata,
			}
			log.info('RESULTS: Saving Column Metadata to {0}'.format(self.log_prefix, self.metadata_file_path))
			save_to_JSON(self.metadata_file_path, json_)
		except Exception, e:
			log.warning('{0}: Failed to save Column Metadata.'.format(self.log_prefix))
			log.warning(e)
			log.warning('{0}: File path was: {1}'.format(self.log_prefix, self.metadata_file_path))
			raise e
