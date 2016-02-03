
# EMF 		From...Import
from 	handle_WordSet 			import EMF_WordSet_Handle
from 	handle_TimeSet 			import EMF_TimeSet_Handle
from 	lib_Runner_PCA 			import LINEAR, LAST_VALUE, NEAREST, IS_INTERPOLATED
from 	lib_TimeSet 			import DATESTRING_TYPE, DATETIME_TYPE, EPOCH_TYPE
# System 	Import...As
import 	pandas 					as pd
import 	numpy 					as np
import 	logging 				as log


class EMF_Interpolator_Handle(object):
	def __init__(self, hndl_DB):
		self._hndl_DB = hndl_DB
		self._hndl_WordSet = EMF_WordSet_Handle(self._hndl_DB)
		self._hndl_TimeSet = None
		self._word_array = None
		self._target_filter = None

	def word_array():
		doc = "The Response Word."
		def fget(self):
			if self._word_array is None:
				self._word_array = pd.DataFrame()
			return self._word_array
		def fset(self, value):
			self._word_array = value
		def fdel(self):
			self._word_array = None
		return locals()
	word_array = property(**word_array())

	def hndl_TimeSet():
		doc = "The Response Word."
		def fget(self):
			if self._hndl_TimeSet is None:
				self._hndl_TimeSet = EMF_TimeSet_Handle()
			return self._hndl_TimeSet
		def fdel(self):
			self._hndl_TimeSet = None
		return locals()
	hndl_TimeSet = property(**hndl_TimeSet())

	def periodicity():
		doc = "Desired periodicity."
		def fget(self):
			return self.hndl_TimeSet.periodicity
		def fset(self, value):
			self.hndl_TimeSet.periodicity = value
		return locals()
	periodicity = property(**periodicity())

	def min_date():
		doc = "min_date."
		def fget(self):
			return self.hndl_TimeSet.startEpoch
		def fset(self, value):
			self.hndl_TimeSet.startEpoch = value
		return locals()
	min_date = property(**min_date())

	def max_date():
		doc = "max_date."
		def fget(self):
			return self.hndl_TimeSet.endEpoch
		def fset(self, value):
			self.hndl_TimeSet.endEpoch = value
		return locals()
	max_date = property(**max_date())

	def target_data_series():
		doc = "The Data Series to be interpolated."
		def fset(self, hndl_Data):
			self._target_key = hndl_Data.ticker
			self.periodicity = hndl_Data.periodicity
			self.min_date = hndl_Data.min_date
			self.max_date = hndl_Data.max_date
			dates = hndl_Data.dates
			values = hndl_Data.values
			self.__add_word(self._target_key, dates, values, force=True)
		def fget(self):
			return self.word_array[self.target_key][self.target_filter]
		def fdel(self):
			self._target_key = None
			del self.target_filter
			del self.hndl_TimeSet
		return locals()
	target_data_series = property(**target_data_series())

	def target_key():
		def fget(self):
			return self._target_key
		def fdel(self):
			self._target_key = None
		return locals()
	target_key = property(**target_key())

	def target_dates():
		doc = "target Dates"
		def fget(self):
			return self.word_array[self.target_key][self.target_filter].index
		return locals()
	target_dates = property(**target_dates())

	def target_values():
		doc = "target Values"
		def fget(self):
			return self.word_array[self.target_key][self.target_filter]
		return locals()
	target_values = property(**target_values())

	def target_filter():
		def fget(self):
			if self._target_filter is None:
				self._target_filter = ~self.word_array[self.target_key].isnull()
			return self._target_filter
		def fdel(self):
			self._target_filter = None
		return locals()
	target_filter = property(**target_filter())

	def PCA_interpolation(self):
		raise NotImplementedError

	def bootstrapped_PCA_interpolation(self):
		raise NotImplementedError

	def polynomial_interpolation(self):
		from sklearn.linear_model import Ridge
		from sklearn.preprocessing import PolynomialFeatures
		from sklearn.pipeline import make_pipeline
		model = make_pipeline(PolynomialFeatures(4), Ridge())
		dt = np.array(target_dates).reshape(-1,1)
		vl = np.array(target_values).reshape(-1,1)
		model.fit(dt, vl)
		genDates = self.hndl_TimeSet.get_dates(outputType=EPOCH_TYPE)
		return model.predict(genDates)

	def simple_interpolation(self, method=LINEAR):
		genDates = self.hndl_TimeSet.get_dates(outputType=EPOCH_TYPE)
		interpolatable = self.word_array[self.target_key].ix[genDates].isnull()
		if sum(interpolatable):
			log.info('INTERPOLATOR: Interpolating {0} points for {1}'.format(sum(interpolatable), self.target_key))
			log.info('INTERPOLATOR: TimeSet to match: {0}'.format(self.hndl_TimeSet))
			tempArray = pd.concat([pd.DataFrame(index=genDates), self.word_array[self.target_key]], axis=1, ignore_index=False)
			if genDates[0] < self.target_dates[0]:
				tempArray[self.target_key][genDates[0]] = self.target_values[0]
			if genDates[-1] > self.target_dates[-1]:
				tempArray[self.target_key][genDates[-1]] = self.target_values[-1]				
			tempArray = tempArray[self.target_key].interpolate(method=method)
			tempArray = pd.concat([pd.DataFrame({IS_INTERPOLATED: interpolatable}, index=genDates), tempArray], axis=1, ignore_index=False)
			return tempArray.ix[genDates]
		else:
			log.info('INTERPOLATOR: Nothing to interpolate for {0}'.format(self.target_key))
			log.info('INTERPOLATOR: TimeSet to match: {0}'.format(self.hndl_TimeSet))
			return None
		
	def __add_word(self, key, dates, values, force=False):
		'''
		Duplicate from handle_WordSet
		'''
		if key in self.word_array:
			log.info('INTERPOLATOR: {0} already in Word Array.'.format(key))
			if not force:
				return
			else:
				newDF = pd.DataFrame({key:values.ravel()}, index=dates.ravel())
				self.word_array = pd.concat([self.word_array, newDF], axis=1, ignore_index=True)
				log.debug('INTERPOLATOR: Added {0} points overwriting {1} in Word Array.'.format(len(self.word_array), key))
		else:
				newDF = pd.DataFrame({key:values.ravel()}, index=dates.ravel())
				self.word_array = pd.concat([self.word_array, newDF], axis=1, ignore_index=False)
				log.debug('INTERPOLATOR: Added {0} points for {1} to Word Array.'.format(len(self.word_array), key))
				# self._hndl_Time = max_time_handle_merge(hndl_Word.hndl_Time, self._hndl_Time) # WARNING! Doesn't work if we truncate an end. Forcing messes w it.
