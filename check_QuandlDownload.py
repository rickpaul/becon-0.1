# EMF 		From...Import
from 	lib_DataSeries		import DATE_COL
from 	lib_DBInstructions	import retrieve_DataSeries_All, TICKER
from 	lib_EMF		 		import TEST_MODE
from 	util_EMF			import dt_date_range_generator, dt_epoch_to_str_Y_M_D, dt_epoch_to_str_Y_M_D_Time
from 	util_EMF 			import YEARS, QUARTERS, MONTHS, WEEKS, DAYS
from 	util_DB				import get_DB_Handle
from 	handle_DataSeries	import EMF_DataSeries_Handle
# System 	Import...As
import 	numpy 				as 	np


def check_Quandl_Download():
	hndl_DB = get_DB_Handle(TEST_MODE)
	allTickers = retrieve_DataSeries_All(hndl_DB.cursor, column=TICKER)
	print 'Retrieved {0} Tickers:'.format(len(allTickers))
	allTickers = ['NAHB_Housing_ProspectiveBuyers']
	for t in allTickers:
		hndl_Data = EMF_DataSeries_Handle(hndl_DB, ticker=t)
		print '({0} : {1})'.format(t, hndl_Data.seriesID)
		generator = dt_date_range_generator(hndl_Data.get_earliest_date(), 
											hndl_Data.get_latest_date(), 
											periodicity=hndl_Data.get_periodicity())
		genDates = np.array([dt_epoch_to_str_Y_M_D_Time(dt) for dt in generator])
		QndDates = np.array([dt_epoch_to_str_Y_M_D_Time(dt) for dt in hndl_Data.get_series_dates()])
		try:
			# print np.vstack((genDates, QndDates)).T
			genLen = len(genDates)
			QndLen = len(QndDates)
			if genLen != QndLen:
				for i in xrange(max(genLen,QndLen)):
					if genDates[i] != QndDates[i]:
						print genDates
						print QndDates
						break

			assert (QndLen == genLen) and np.all(genDates == QndDates)
		except:
			print t + '\t\tFAILED!'


def check_dates(dates, minDate, maxDate, periodicity=MONTHS):
	generator = dt_date_range_generator(minDate, maxDate, periodicity=periodicity)
	genDates = np.array([dt for dt in generator])
	try:
		# print np.vstack((genDates, QndDates)).T
		genLen = len(genDates)
		datLen = len(dates)
		if genLen != datLen:
			for i in xrange(max(genLen,datLen)):
				print genDates[i], 
				print dates[i]
				if genDates[i] != dates[i]:
					print dt_epoch_to_str_Y_M_D_Time(genDates[i]), 
					print dt_epoch_to_str_Y_M_D_Time(dates[i]), 
					break
		assert (datLen == genLen) and np.all(genDates == dates)
	except Exception, e:
		print e
		print 'FAILED!'

def main():
	check_Quandl_Download()

if __name__ == '__main__':
	main()


