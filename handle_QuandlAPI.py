# TODO:
#	Implement Error Handling (e.g. what to do when get 404)
#	Add Logging
#	Implement Parameter Checking (e.g. dates in correct format, order =asc or desc)
#	How do you know if data is interpolated or forecast?

# 	Make sure CSV written is utf-8
# 	Get metadata first; only download if necessary

# EMF 		From...Import
from 	lib_QuandlAPI	import USE_DEFAULT
from	util_QuandlAPI	import codify_periodicity, stringify_periodicity
from	util_TimeSet 	import dt_str_Y_M_D_to_epoch as YMD_to_epoch
from	util_TimeSet 	import dt_epoch_to_str_Y_M_D as epoch_to_YMD
from	util_TimeSet 	import str_Y_M_D_is_end_of_month as YMD_is_EoM
# EMF 		Import...As
import 	lib_QuandlAPI 	as lib_quandl
# System 	From...Import
from 	copy 			import copy
# System 	Import...As
import 	urllib2
import 	json
import	logging 		as 	log
import	numpy			as 	np

class EMF_QuandlAPI_Handle(object):
	'''
	We decided to keep this in urllib2. 
	There is a Quandl package we are not using.
	We are also not using requests.
	TODOS:
				Save off metadata
	'''
	def __init__(self, Q_Database, Q_Dataset):
		self._Quandl_Database = Q_Database
		self._Quandl_Dataset = Q_Dataset
		self.parameters = {
			'db': self._Quandl_Database, 
			'ds': self._Quandl_Dataset,
			'api': lib_quandl.QuandlAPIKey
		}
		self._dnld_parameters = lib_quandl.URLParameterDefaults
		self._error = None

	def Instr_Collapse():
		doc = "The Collapse Instruction for Quandl Downloads."
		def fget(self):
			return self.get_download_parameter('collapse')
		def fdel(self):
			self.rmv_download_parameter('collapse')
			log.debug('QUANDL: Removing Periodicity override')
		def fset(self, value):
			if value is None:
				self.rmv_download_parameter('collapse')
				log.debug('QUANDL: Removing Periodicity override')
			elif value is USE_DEFAULT:
				pass
			else:
				self.set_download_parameter('collapse', value)
				log.debug('QUANDL: Periodicity override is now: {0}'.format(value))
		return locals()
	Instr_Collapse = property(**Instr_Collapse())

	def Instr_Transform():
		doc = "The Transformation Instruction for Quandl Downloads."
		def fdel(self):
			self.rmv_download_parameter('transform')
			log.debug('QUANDL: Removing Transformation override')
		def fset(self, value):
			if value is None:
				self.rmv_download_parameter('transform')
				log.debug('QUANDL: Removing Transformation override')
			elif value is USE_DEFAULT:
				pass
			else:
				self.set_download_parameter('transform', value)
				log.debug('QUANDL: Transformation override is now: {0}'.format(value))
		return locals()
	Instr_Transform = property(**Instr_Transform())

	def Instr_Col_Idx():
		doc = "The Column Index Instruction for Quandl Downloads."
		def fdel(self):
			self.rmv_download_parameter('column_index')
			log.debug('QUANDL: Removing Column Index override')
		def fset(self, value):
			if value is None:
				self.rmv_download_parameter('column_index')
				log.debug('QUANDL: Removing Column Index override')
			elif value is USE_DEFAULT:
				pass
			else:
				self.set_download_parameter('column_index', value)
			log.debug('QUANDL: Column Index override is now: {0}'.format(value))
		return locals()
	Instr_Col_Idx = property(**Instr_Col_Idx())

	def Instr_Start_Date():
		doc = "The Start-Date Instruction for Quandl Downloads."
		def fdel(self):
			self.rmv_download_parameter('start_date')
			log.debug('QUANDL: Removing Start Date override')
		def fset(self, value):
			if value is None:
				self.rmv_download_parameter('start_date')
				log.debug('QUANDL: Removing Start Date override')
			elif value is USE_DEFAULT:
				pass
			else:
				value = dt_epoch_to_str_Y_M_D(value)
				self.set_download_parameter('start_date', value)
				log.debug('QUANDL: Start Date override is now: {0}'.format(value))
		return locals()
	Instr_Start_Date = property(**Instr_Start_Date())

	def Quandl_Database():
		doc = "The Quandl_Database."
		def fget(self):
			return self._Quandl_Database
		return locals()
	Quandl_Database = property(**Quandl_Database())

	def Quandl_Dataset():
		doc = "The Quandl_Dataset."
		def fget(self):
			return self._Quandl_Dataset
		return locals()
	Quandl_Dataset = property(**Quandl_Dataset())

	def Quandl_Name():
		doc = "The Quandl_Name."
		def fget(self):
			return self._Quandl_Name
		return locals()
	Quandl_Name = property(**Quandl_Name())

	def Quandl_Description():
		doc = "The Quandl_Description."
		def fget(self):
			return self._Quandl_Description
		return locals()
	Quandl_Description = property(**Quandl_Description())

	def Quandl_Earliest_Date():
		doc = "The Quandl_Earliest_Date."
		def fget(self):
			return self._Quandl_Earliest_Date
		return locals()
	Quandl_Earliest_Date = property(**Quandl_Earliest_Date())

	def Quandl_Latest_Date():
		doc = "The Quandl_Latest_Date."
		def fget(self):
			return self._Quandl_Latest_Date
		return locals()
	Quandl_Latest_Date = property(**Quandl_Latest_Date())

	def Quandl_Latest_Refresh():
		doc = "The Quandl_Latest_Refresh."
		def fget(self):
			return self._Quandl_Latest_Refresh
		return locals()
	Quandl_Latest_Refresh = property(**Quandl_Latest_Refresh())

	def Quandl_Periodicity():
		doc = "The Quandl_Periodicity."
		def fget(self):
			return self._Quandl_Periodicity
		return locals()
	Quandl_Periodicity = property(**Quandl_Periodicity())

	def Data_Num_Columns():
		doc = "The Data_Num_Columns."
		def fget(self):
			return self._Data_Num_Columns
		return locals()
	Data_Num_Columns = property(**Data_Num_Columns())

	def Data_Num_Points():
		doc = "The Data_Num_Points."
		def fget(self):
			return self._Data_Num_Points
		return locals()
	Data_Num_Points = property(**Data_Num_Points())

	def Data_Chosen_Column():
		doc = "The Data_Chosen_Column."
		def fget(self):
			return self._Data_Chosen_Column
		return locals()
	Data_Chosen_Column = property(**Data_Chosen_Column())

	def Data_Periodicity():
		doc = "The Data_Periodicity."
		def fget(self):
			return stringify_periodicity(
				max(	codify_periodicity(self.Instr_Collapse), 
						codify_periodicity(self.Quandl_Periodicity)
					)
				)
		return locals()
	Data_Periodicity = property(**Data_Periodicity())

	def Data_Earliest_Date():
		doc = "The Data_Earliest_Date."
		def fget(self):
			return self._Data_Earliest_Date
		return locals()
	Data_Earliest_Date = property(**Data_Earliest_Date())

	def Data_Latest_Date():
		doc = "The Data_Latest_Date."
		def fget(self):
			return self._Data_Latest_Date
		return locals()
	Data_Latest_Date = property(**Data_Latest_Date())

	def dates():
		doc = "The data dates."
		def fget(self):
			return self._dates
		def fset(self, value):
			self._dates = value
		return locals()
	dates = property(**dates())

	def values():
		doc = "The data values."
		def fget(self):
			return self._values
		def fset(self, value):
			self._values = value
		return locals()
	values = property(**values())

	# def metadata():
	# 	doc = "The data metadata."
	# 	def fget(self):
	# 		return self._metadata
	# 	def fset(self, value):
	# 		self._metadata = value
	# 	return locals()
	# metadata = property(**metadata())

	def error():
		doc = "The data's error."
		def fget(self):
			return self._error
		def fset(self, value):
			self._error = value
		return locals()
	error = property(**error())

	def __get_parameterized_URL(self, url):
		for key in self._dnld_parameters:
			url += '&' + lib_quandl.URLParameterFormats[key]
		tempDict = copy(self.parameters)
		tempDict.update(self._dnld_parameters)
		return url.format(**tempDict)

	def set_download_parameter(self, param_name, param_value):
		'''
		PARAMETERS:
					<string>	param_name
					<string>	param_value
		RETURNS: 	
					<NONE>
		TODOS:
					--Implement Parameter Checking (e.g. dates in correct format, order =asc or desc)
		'''
		assert param_name in lib_quandl.URLParameterFormats
		self._dnld_parameters[param_name] = param_value

	def rmv_download_parameter(self, param_name):
		'''
		PARAMETERS:
					<string>	param_name
		RETURNS: 	
					<NONE>
		TODOS:
					--Implement Parameter Checking (e.g. dates in correct format, order =asc or desc)
		'''
		try:
			del self._dnld_parameters[param_name]
		except KeyError as e:
			pass

	def get_download_parameter(self, param_name):
		'''
		PARAMETERS:
					<string>	param_name
		RETURNS: 	
					<NONE>
		TODOS:
					--Implement Parameter Checking (e.g. dates in correct format, order =asc or desc)
		'''
		try:
			return self._dnld_parameters[param_name]
		except KeyError as e:
			pass

	def get_data(self, columnName=None):
		'''
		RETURNS:
					<TUPLE>(dates, values, metadata) 
		TODO:
					+How do you know if data is interpolated or forecast?
					-Add Logging
		-'''
		try:
			# Get Data
			log.info('QUANDL: Retrieving Quandl API Data')
			url = self.__get_parameterized_URL(lib_quandl.QuandlURL)
			queryJSON = self.__retrieve_raw_json(url)
			# Parse Metadata
			log.info('QUANDL: Parsing Quandl API Metadata')
			self.__parse_JSON_metadata(queryJSON)
			# Parse Data List
			log.info('QUANDL: Parsing Quandl Data History')
			self.__parse_JSON_data_history(queryJSON, columnName=columnName)
		except Exception, e:
			log.error('QUANDL: Uncaught Error')
			log.error('QUANDL: {0}'.format(e))
			self.error = 'Uncaught Error'

	def __retrieve_raw_json(self, url):
		'''
		TODOS:
					+Implement Error Handling (e.g. what to do when get 404)
					-Add Logging
		'''
		try:
			log.debug('QUANDL: Attempting Download from:\n\t\t{0}'.format(url))
			response = urllib2.urlopen(url)
			rawData = response.read()
			log.debug('QUANDL: Download Successful')
		except urllib2.HTTPError as e:
			log.error('QUANDL: Download Failed')
			log.error('QUANDL: {0}'.format(e))
			self.error = 'HTTP Error: ' + response.getcode()
			log.error('QUANDL: ' + self.error)
		except Exception as e:
			log.error('QUANDL: Download Failed')
			log.error('QUANDL: {0}'.format(e))
		# Parse and Return
		return json.loads(rawData)['dataset']

	def __parse_JSON_data_history(self, queryJSON, columnName=None):
		'''
		TODOS:
					++Save to broken download database!
					++WE HAVE NO CHECK FOR PERIODICITY!!!
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
				columnIndex = numCols - 1
				log.warning('QUANDL: More than one column detected for data download. Using Final Column({0})'.format(columns[columnIndex]))
				self.error = 'Multiple Column Error'
			else:
				columnIndex = columns.index(columnName)
		else:
			columnIndex = 1
		self._Data_Chosen_Column = columns[columnIndex]
		log.info('QUANDL: Reading Column ({0})'.format(self.Data_Chosen_Column))
		# Fill Dates and Value Arrays
		dates = []
		values = []
		for row in dataset:
			if not YMD_is_EoM(row[0]):
				log.warning('QUANDL: Date {0} not End of Month.'.format(row[0]))
			dates.append(YMD_to_epoch(row[0]))
			values.append(row[columnIndex])
		# Save Data
		self._Data_Earliest_Date = epoch_to_YMD(min(dates))
		self._Data_Latest_Date = epoch_to_YMD(max(dates))
		# Save Values
		(self.dates, self.values) =  (np.asarray(dates), np.asarray(values))

	def __parse_JSON_metadata(self, queryJSON):
		'''
		TODOS:
					+Difference between oldest_available_date and start_date?
					-Move queryJSON keys to lib_QuandlAPI
					-Add Logging
		'''
		#
		self._Quandl_Name 			= queryJSON['name']
		self._Quandl_Description 	= queryJSON['description']
		self._Quandl_Latest_Refresh = queryJSON['refreshed_at']
		#
		self._Quandl_Earliest_Date 	= queryJSON['oldest_available_date']
		self._Quandl_Latest_Date 	= queryJSON['newest_available_date']
		self._Quandl_Periodicity 	= queryJSON['frequency']
		#
		self._Data_Num_Points 		= len(queryJSON['data'])
		self._Data_Num_Columns 		= len(queryJSON['column_names'])


	# def get_metadata(self, saveHistoryLocal=False):
	# 	'''
	# 	This is unused.

	# 	RETURNS:
	# 				<NONE>
	# 	TODO:
	# 				+How do you know if data is interpolated or forecast?
	# 				-Add Logging
	# 	-'''
	# 	raise NotImplementedError
	# 	try:
	# 		# Get Data
	# 		url = self.__get_parameterized_URL(lib_quandl.QuandlMetadataURL)
	# 		queryJSON = self.__retrieve_raw_json(url)
	# 		# Parse Data
	# 		metadata = self.__parse_JSON_metadata(queryJSON)
	# 		# Save Local
	# 		if saveHistoryLocal:
	# 			self.metadata = metadata
	# 		# Return
	# 		metadata['ERROR'] = self.error
	# 		return metadata
	# 	except Exception, e:
	# 		log.error('QUANDL: {0}'.format(e))
	# 		return ({'ERROR':'UNCAUGHT LOCAL ERROR'})
