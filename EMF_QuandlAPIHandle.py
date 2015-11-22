# TODO:
#	CONSIDER: Use Quandl Python Library? I think no.
#	Needs to be handle? Could be lib

import 	EMF_Quandl_lib as quandlLib
import 	urllib2
import 	json

class EMF_QuandlAPI_Handle:

	def __init__(self):
		raise NotImplementedError

	def setDataset(self, Q_Database, Q_Dataset):
		self.Q_Database = Q_Database
		self.Q_Dataset = Q_Dataset


	def retrieveJSONData(self, url):
		'''
		TODO:
		Implement Error Handling (e.g. what to do when get 404)
		'''
		rawData = urllib2.urlopen(url).read()
		queryResult = json.loads(rawData)
		dates = 
		raise NotImplementedError

	def __getURL_QuandlData(self):
		url.format(**{'db': self.Q_Database, 'ds': self.Q_Dataset})
		return url

	def __getURL_QuandlMetaData(self):
		raise NotImplementedError

	def __getURL_QuandlDataAndMetaData(self):
		raise NotImplementedError

# date column is always 0
#"https://www.quandl.com/api/v3/datasets/WIKI/AAPL.json?order=asc&exclude_column_names=true&start_date=2012-11-01&end_date=2012-11-30&column_index=4&collapse=weekly&transformation=rdiff"
#limit=1 === latest only
#rows=1 === latest only