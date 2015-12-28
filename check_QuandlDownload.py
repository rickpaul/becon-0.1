# EMF 		From...Import
from 	lib_DataSeries		import DATE_COL
from 	lib_DBInstructions	import retrieve_DataSeries_All, TICKER, ID
from 	lib_EMF		 		import TEST_MODE
from 	util_EMF			import dt_date_range_generator, dt_epoch_to_str_Y_M_D, dt_epoch_to_str_Y_M_D_Time
from 	util_DB				import get_DB_Handle
from 	handle_DataSeries	import EMF_DataSeries_Handle
# System 	Import...As
import 	numpy 				as 	np


def check_Quandl_Download():
	hndl_DB = get_DB_Handle(TEST_MODE)
	hndl_Data = EMF_DataSeries_Handle(hndl_DB)
	allIDs = retrieve_DataSeries_All(hndl_DB.cursor_(), column=ID)
	allTickers = retrieve_DataSeries_All(hndl_DB.cursor_(), column=TICKER)
	print 'Retrieved {0} IDs:'.format(len(allIDs))
	for (t, i) in zip(allTickers, allIDs):
		print '({0} : {1})'.format(i,t)
	for t in allTickers:
		hndl_Data.set_data_series(ticker=t)
		generator = dt_date_range_generator(hndl_Data.get_earliest_date(), hndl_Data.get_latest_date(), periodicity=12)
		genDates = np.array([dt_epoch_to_str_Y_M_D_Time(dt) for dt in generator])
		QndDates = np.array([dt_epoch_to_str_Y_M_D_Time(dt) for dt in hndl_Data.get_data_history()[DATE_COL]])
		try:
			# print np.vstack((genDates, QndDates)).T
			genLen = len(genDates)
			QndLen = len(QndDates)
			assert (QndLen == genLen)
			assert np.all(genDates == QndDates)
		except:
			print t + ' failed.' + hndl_Data.
		hndl_Data.unset_data_series()


def main():
	check_Quandl_Download()

if __name__ == '__main__':
	main()