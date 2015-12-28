# TODO:
#	Implement Error Handling (e.g. what to do when get 404)
#	Add Logging
#	Implement Parameter Checking (e.g. dates in correct format, order =asc or desc)
#	How do you know if data is interpolated or forecast?
# EMF 		From...Import
from	util_EMF 		import dt_str_YYYY_MM_DD_to_epoch as YMD_to_epoch
# EMF 		Import...As
import 	lib_QuandlAPI 	as lib_quandl
# System 	Import...As
import 	urllib2
import 	json
import	logging 		as 	log
import	numpy			as 	np

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
		self.error = None

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

	def get_data(self, columnName=None, saveHistoryLocal=False):
		'''
		RETURNS:
					<NONE>
		TODO:
					+How do you know if data is interpolated or forecast?
					-Add Logging
		-'''
		try:
			# Get Data
			url = self.__get_parameterized_URL()
			queryJSON = self.__retrieve_data(url)
			# Parse Data
			metadata = self.__parse_JSON_metadata(queryJSON)
			(dates, values) = self.__parse_JSON_data_history(queryJSON, columnName=columnName)
			# Save Local
			if saveHistoryLocal:
				(self.dates, self.values, self.metadata) = (dates, values, metadata)
			# Return
			metadata['ERROR'] = self.error
			return (dates, values, metadata)
		except:
			return ([],[], {'ERROR':'UNCAUGHT ERROR'})

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
			responseCode = response.getcode()
			self.error = 'HTTP Error: ' + responseCode
		return json.loads(rawData)['dataset']

	def __parse_JSON_data_history(self, queryJSON, columnName=None):
		'''
		TODOS:
					++Save to broken download database!
					++What to do with None Values in matrix
					+Implement Error Handling (e.g. what to do when JSON read fails)
					-Move queryJSON keys to lib_QuandlAPI
					-Add Logging
		'''
		# Unwrap Data History
		dataset = queryJSON['data']
		# Unwrap Columns and Assign Column Index
		columns = queryJSON['column_names']
		numCols = len(columns)
		assert numCols > 0
		if numCols != 2:
			if (columnName is None) or (columnName not in columns):
				log.warning('More than one column detected for data download. Using First Column')
				columnIndex = 1
				self.error = 'Multiple Column Error'
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
			# originalDates.append(YMD_to_epoch(row[0]))
			dates.append(YMD_to_epoch(row[0], endOfMonth=True))
			values.append(row[columnIndex])
		# originalDates = np.asarray(originalDates)
		dates = np.asarray(dates)
		values = np.asarray(values)
		# Return
		return (dates, values)

	def __parse_JSON_metadata(self, queryJSON):
		'''
		TODOS:
					+Difference between oldest_available_date and start_date?
					-Move queryJSON keys to lib_QuandlAPI
					-Add Logging
		'''
		metadata = {}
		# Unwrap MetaData History
		metadata['Q_EARLIEST_DATE'] = queryJSON['oldest_available_date']
		metadata['Q_LATEST_DATE'] = queryJSON['newest_available_date']
		# metadata['Q_EARLIEST_DATE'] = queryJSON['start_date']
		# metadata['Q_LATEST_DATE'] = queryJSON['end_date']
		metadata['Q_REFRESHED_AT'] = queryJSON['refreshed_at']
		metadata['Q_PERIODICITY'] = queryJSON['frequency']
		metadata['Q_NAME'] = queryJSON['name']
		metadata['Q_DESCRIPTION'] = queryJSON['description']
		metadata['NUM_COLUMNS'] = len(queryJSON['column_names'])
		metadata['NUM_POINTS'] = len(queryJSON['data'])
		return metadata

