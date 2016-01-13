# TODO:
#	Figure out why columns are writing wrong
# 	put categories in some DB for use.

# EMF 		From...Import
from lib_EMF import HomeDirectory

######################### CSV CODE

CSVRepository = HomeDirectory + 'csv/'
TempQuandlCSV = CSVRepository + 'KansasCityFed.csv'
TestQuandlCSV = CSVRepository + 'dataset1.csv'
QAQuandlCSV = CSVRepository + 'QuandlDataSeries.csv'
ProdQuandlCSV = CSVRepository + 'QuandlDataSeries.csv'

QuandlCSVColumns = [
	'category1',
	'category2',
	'category3',
	'source',
	'db_name',
	'db_ticker',
	'Q_DATABASE_CODE',
	'Q_DATASET_CODE',
	'Q_COLUMN_NUM',
	'Q_COLUMN_NAME',
	'Q_COLLAPSE_INSTR',
	'Q_TRANSFORM_INSTR',
	'Q_REFRESHED_AT',
	'Q_EARLIEST_DATE',
	'Q_LATEST_DATE',
	'Q_PERIODICITY',
	'UNIT_TYPE',
	'SEASONALLY_ADJUSTED',
	'IS_CATEGORICAL'
	'EMF_periodicity',
	'EMF_DataType',
	'EMF_DataSector',
	'Q_DESCRIPTION',
	'Q_NAME',
	'NUM_COLUMNS',
	'NUM_POINTS',
	'ERROR'
]
QuandlCSVColumns = dict(zip(QuandlCSVColumns, xrange(len(QuandlCSVColumns))))

QuandlEditableColumns = [
	'Q_REFRESHED_AT',
	'Q_EARLIEST_DATE',
	'Q_LATEST_DATE',
	'Q_PERIODICITY',
	'Q_DESCRIPTION',
	'Q_NAME',
	'NUM_POINTS',
	'NUM_COLUMNS',
	'ERROR'
]

######################### API CODE
QuandlAPIKey = 'pmM4BUFqzx1FetXxbj1x'

# dataURL = 'https://www.quandl.com/api/v3/datasets/{db}/{ds}/data.json?api_key={api}'
# metaDataURL = 'https://www.quandl.com/api/v3/datasets/{db}/{ds}/metadata.json?api_key={api}'
QuandlURL = 'https://www.quandl.com/api/v3/datasets/{db}/{ds}.json?api_key={api}'

URLParameterFormats = {
	'order' : 'order={order}', # order=asc|desc
	'start_date': 'start_date={start_date}', #yyyy-mm-dd
	'end_date': 'end_date={end_date}', #yyyy-mm-dd
	'column_index': 'column_index={column_index}', #integer
	'collapse': 'collapse={collapse}', # collapse=none|daily|weekly|monthly|quarterly|annual
	'transform': 'transform={transform}', # transform=none|diff|rdiff|cumul|normalize
	'rows': 'rows={rows}',
	'limit': 'limit={limit}',
	# 'exclude_column_names': 'exclude_column_names={exclude_column_names}', # CSV 
}

URLParameterDefaults = {
	'order': 'asc',
	'collapse': 'monthly',
}

START_DATE = '1960-01-01'
