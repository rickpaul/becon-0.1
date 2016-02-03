# EMF 		From...Import
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_Logging 			import EMF_Logging_Handle
from 	handle_Interpolator 	import EMF_Interpolator_Handle
from 	handle_TimeSet			import EMF_TimeSet_Handle
from 	handle_WordSelector2 	import EMF_WordSelector_Handle2
from 	lib_DBInstructions		import retrieve_DataSeries_All, TICKER
from 	lib_Runner_Model 		import PredictorTransformationKeys, ResponseTransformationKeys # should come from lib_runner_pca?
from 	lib_Runner_PCA 			import LINEAR, LAST_VALUE, NEAREST, IS_INTERPOLATED
from 	lib_TimeSet 			import DAYS, WEEKS, MONTHS, QUARTERS, YEARS, SECONDS
from 	util_DB					import connect_to_DB
# EMF 		Import...As
import 	lib_EMF
import 	lib_Runner_PCA
# System 	Import...As
import 	numpy 					as np

class EMF_Interpolation_Runner(object):
	def __init__(self, hndl_DB):
		self._hndl_DB = hndl_DB
		self._hndl_WrdSlct = EMF_WordSelector_Handle2(self._hndl_DB)
		self._hndl_Intrp = EMF_Interpolator_Handle(self._hndl_DB)

	def interpolate_missing_db_values(self, periodicity=MONTHS, method=LINEAR):
		allTickers = retrieve_DataSeries_All(hndl_DB.cursor, column=TICKER)
		print 'Retrieved {0} Tickers:'.format(len(allTickers))
		for t in allTickers:
			hndl_Data = EMF_DataSeries_Handle(hndl_DB, ticker=t)
			self._hndl_Intrp.target_data_series = hndl_Data
			if periodicity is not None:
				self._hndl_Intrp.periodicity = periodicity
			if method==LINEAR:
				results = self._hndl_Intrp.simple_interpolation(method=method)
				if results is not None:
					# Save New Interpolated Dates
					results = results[results[IS_INTERPOLATED]]
					dates = np.array(results.index).ravel()
					values = np.array(results[t]).ravel()
					interpolated = np.ones(len(values))
					hndl_Data.save_series_db(dates, values, isInterpolated=interpolated)
					# Adjust Periodicity
					hndl_Data.original_periodicity=hndl_Data.periodicity
					hndl_Data.periodicity=periodicity
			del self._hndl_Intrp.target_data_series
			del self._hndl_Intrp.word_array

	# def add_auxiliary_data(self):
	# 	self._hndl_WrdSlct.select_pred_words_all_tickers()

	# def add_target_data(self, data):
	# 	self._hndl_WrdSlct.select_pred_words_all_tickers()

CURRENT_MODE = lib_EMF.TEST_MODE
CURRENT_DATA_SERIES = ''

def main(hndl_DB):
	runner_Intrp = EMF_Interpolation_Runner(hndl_DB)
	# runner_Intrp.set_model_from_template(CURRENT_TEMPLATE)
	# runner_Intrp.add_data()
	runner_Intrp.interpolate_missing_db_values()

if __name__ == '__main__':
	hndl_Log = EMF_Logging_Handle(mode=CURRENT_MODE)
	hndl_DB = connect_to_DB(mode=CURRENT_MODE)
	main(hndl_DB)