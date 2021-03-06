# TODO:
#	Figure out why columns are writing wrong
# 	put categories in some DB for use.

# EMF 		From...Import
from lib_EMF import HomeDirectory

######################### CSV CODE

CSVRepository = HomeDirectory + 'csv/'
TempQuandlCSV = CSVRepository + '_test_dataset_1.csv'
TestQuandlCSV = CSVRepository + 'dataset1.csv'
QAQuandlCSV = CSVRepository + 'QuandlDataSeries.csv'
ProdQuandlCSV = CSVRepository + 'QuandlDataSeries.csv'

QuandlCSVColumns = [
	'geography',
	'geography_size',
	'category_1',
	'sub_category_1',
	'category_1_meaning',
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
	'IS_CATEGORICAL',
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

# CSV Download Instruction Columns
QuandlDnldCols = [	'Q_DATABASE_CODE',
					'Q_DATASET_CODE', 
					'Q_COLUMN_NUM', 
					'Q_COLLAPSE_INSTR', 
					'Q_TRANSFORM_INSTR']
# CSV Download Instruction Column Indexes
QuandlDnldColIdxs = [QuandlCSVColumns[x] for x in QuandlDnldCols]

######################### API CODE

QuandlAPIKey = 'pmM4BUFqzx1FetXxbj1x'

QuandlDataURL = 'https://www.quandl.com/api/v3/datasets/{db}/{ds}/data.json?api_key={api}'
QuandlMetadataURL = 'https://www.quandl.com/api/v3/datasets/{db}/{ds}/metadata.json?api_key={api}'
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
	'start_date': '1960-01-01'
}

USE_DEFAULT = u'' # Note this is what would come in from an un-filled CSV Column
