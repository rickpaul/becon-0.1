# TODO:
#	remove main()
#	Implement Error Handling (e.g. what to do when get 404)
#	Add Logging
#	Implement Parameter Checking (e.g. dates in correct format, order =asc or desc)
#	How do you know if data is interpolated or forecast?

from	util_EMF 	import dtConvert_YYYY_MM_DDtoEpoch

import 	lib_QuandlAPI as lib_quandl
import 	urllib2
import 	json
import	logging as 	log
import	numpy	as 	np

class EMF_QuandlAPI_Handle:
	'''
	CONSIDER:
				Use Quandl package (NO)
				Use Requests package instead of urllib2 (NO)
	TODOS:
				Save off metadata
	'''
	def __init__(self, Q_Database, Q_Dataset):
		self.parameters = {
			'db': Q_Database, 
			'ds': Q_Dataset,
			'api': lib_quandl.QuandlAPIKey
		}
		self.extraParameters = lib_quandl.URLParameterDefaults

	def set_extra_parameter(self, parameter_name, parameter_value):
		'''
		PARAMETERS:
					<string>	parameter_name
					<string>	parameter_value
		RETURNS: 	
					<NONE>
		TODOS:
					--Implement Parameter Checking (e.g. dates in correct format, order =asc or desc)
		'''
		assert parameter_name in lib_quandl.URLParameterFormats
		self.extraParameters[parameter_name] = parameter_value

	def get_data_history(self, columnName=None, saveHistoryLocal=False):
		'''
		RETURNS:
					<NONE>
		TODO:
					+How do you know if data is interpolated or forecast?
					-Add Logging
		-'''
		url = self.__get_parameterized_URL()
		queryJSON = self.__retrieve_data(url)
		(dates, values) = self.__parse_JSON_data(queryJSON, columnName=columnName)
		if saveHistoryLocal:
			(self.dates, self.values) = (dates, values)
		return (dates, values)

	def __get_parameterized_URL(self, url=lib_quandl.QuandlURL):
		tempDict = {}
		for key in self.extraParameters:
			url += '&' + lib_quandl.URLParameterFormats[key]
		tempDict.update(self.parameters)
		tempDict.update(self.extraParameters)
		return url.format(**tempDict)

	def __retrieve_data(self, url):
		'''
		CONSIDER:
					Could use Requests package
		TODOS:
					+Implement Error Handling (e.g. what to do when get 404)
					-Add Logging
		'''
		try:
			response = urllib2.urlopen(url)
			rawData = response.read()
			responseCode = response.getcode()
		except urllib2.HTTPError as e:
			raise NotImplementedError #Handle Exception
		return json.loads(rawData)

	def __parse_JSON_data(self, queryJSON, columnName=None):
		'''
		TODOS:
					++Save to broken download database!
					++What to do with None Values in matrix
					+Implement Error Handling (e.g. what to do when JSON read fails)
					-Move queryJSON keys to lib_QuandlAPI
					-Add Logging
		'''
		# Unwrap Data History
		dataset = queryJSON['dataset']['data']
		# Unwrap Columns and Assign Column Index
		columns = queryJSON['dataset']['column_names']
		numCols = len(columns)
		assert numCols > 0
		if numCols != 2:
			if (columnName is None) or (columnName not in columns):
				log.warning('More than one column detected for data download. Using First Column')
				columnIndex = 1
				raise NotImplementedError # SAVE TO BROKEN DOWNLOADS DB
			else:
				columnIndex = columns.index(columnName)
		else:
			columnIndex = 1
		# Fill Dates and Value Arrays
		# originalDates = []
		dates = []
		values = []
		numRows = len(dataset)
		for row in dataset:
			# originalDates.append(dtConvert_YYYY_MM_DDtoEpoch(row[0]))
			dates.append(dtConvert_YYYY_MM_DDtoEpoch(row[0], endOfMonth=True))
			values.append(row[columnIndex])
		# originalDates = np.asarray(originalDates)
		dates = np.asarray(dates)
		values = np.asarray(values)
		# Return
		return (dates, values)

def main():
	handle = EMF_QuandlAPI_Handle('WIKI','FB')
	(dates, values) = handle.get_data_history(columnName='Open')
	handle.set_extra_parameter('column_index', 1)
	(dates2, values2) = handle.get_data_history()
	assert np.all(dates==dates2)
	assert np.all(values==values2)
	print np.vstack((dates, values))

if __name__ == '__main__':
	main()