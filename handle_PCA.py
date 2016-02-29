# EMF 		From...Import
from 	handle_ColumnArray 		import EMF_ColumnArray_Handle
from 	lib_PCA 				import PREDICTOR, RESPONSE, INDEX
from 	lib_PCA 				import WORD_TYPE
# System 	Import...As
import 	logging 				as log
import 	pandas	 				as pd
# System 	From...Import
from 	sklearn.decomposition 	import PCA

class EMF_PCA_Handle(EMF_ColumnArray_Handle):
	def __init__(self):
		#
		self._file_name = None
		self._array_file_path = None
		self._metadata_file_path = None
		#
		self._log_prefix = 'PCA MODEL'
		super(EMF_Results_Handle, self).__init__(save_to_file=True)
		self.max_size = 100

	def is_centered():
		doc = "The is_centered property."
		def fget(self):
			return self._is_centered
		def fset(self, value):
			self._is_centered = value
		return locals()
	is_centered = property(**is_centered())

	def normalize_col_array(self):
		raise NotImplementedError # This isn't working, because we need to normalize the data to a range or std
		# Also can't always use negative values
		self._center_stats_dates = self._col_array.mean(axis=1)
		self._center_stats_words = self._col_array.mean(axis=0)
		self._col_array = self._col_array.subtract(self._center_stats_dates, axis=0)
		self._col_array = self._col_array.subtract(self._center_stats_words, axis=1)
		self.is_centered = True

	def denormalize_col_array(self):
		self._col_array = self._col_array.multiply(self._center_stats_dates, axis=0)
		self._col_array = self._col_array.subtract(self._center_stats_dates, axis=0)
		self.
		self._center_stats_dates = self._col_array.mean(axis=1)
		self._center_stats_words = self._col_array.mean(axis=0)

	def add_column(self, dates, values, key=None, force=False):
		if self.is_centered:
			raise Exception('Cannot add column to already-normalized array')
		super(EMF_Results_Handle, self).add_column(dates, values, key=key, force=force)

	def run_PCA(self):
		self.__normalize_col_array()
		copy_col_array = self._col_array.copy()
		# Zero Out Response
		for col_name in copy_col_array:
			if self._model_info[col_name][WORD_TYPE] == RESPONSE:
				copy_col_array[col_name] = 0
				# raise NotImplementedError # How are we dealing with NaNs?
			elif self._model_info[col_name][WORD_TYPE] == PREDICTOR:
				pass
			else:
				raise NameError
		model = PCA(n_components='mle', whiten=True)
		model.fit_transform(self._col_array)
		self._results = model.inverse_transform(copy_col_array)

	def add_word(self, hndl_Word, word_type=PREDICTOR):
		self.__add_word_metadata(hndl_Word)
		self.__add_word_history(hndl_Word)

	def __add_word_metadata(self, hndl_Word):
		pass

	def __add_word_history(self, hndl_Word):
		col_name = self.__column_name(hndl_Word)
		values = hndl_Word.values
		dates = hndl_Word.dates
		newValues = pd.DataFrame({col_name: values.ravel()}, index=dates.ravel())
		self._col_array = pd.concat([self._col_array, newValues], axis=1, ignore_index=False)

	def __column_name(self, hndl_Word):
		dict_ = {
			'category' : hndl_Word.category,
			'subcategory' : hndl_Word.subcategory,
			'category_meaning' : hndl_Word.category_meaning,
			'data_ticker' : hndl_Word.data_ticker,
			'transformation' : hndl_Word.trns_code
		}
		str_ = '{category}:{subcategory}:{category_meaning}|{data_ticker}|{transformation}'
		return str_.format(**dict_)

	def create_index(self):
		pass

	def plot_words(self):
		pass
