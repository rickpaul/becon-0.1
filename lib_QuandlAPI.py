# EMF 		From...Import
from lib_EMF import HomeDirectory

######################### CSV CODE

CSVRepository = HomeDirectory + 'csv/'
TempQuandlCSV = CSVRepository + 'KansasCityFed.csv'
TestQuandlCSV = CSVRepository + 'KansasCityFed.csv'
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

# S&P 500 Stats

# Book Value Per Share
# Dividend
# Dividend Growth
# Dividend Yield
# Earnings
# Earnings Yield
# Earnings Growth
# Real Earnings Growth
# PE Ratio
# Historical Prices
# Inflation Adjusted Prices
# Price to Book Value
# Price to Sales Ratio
# Shiller PE 10 Ratio
# Real Sales Per Share
# Sales Per Share
# Sales Growth
# Real Sales Growth

# Treasury Rates

# 1 Month
# 3 Month
# 6 Month
# 1 Year
# 2 Year
# 3 Year
# 5 Year
# 7 Year
# 10 Year
# 20 Year
# 30 Year


# Real Interest Rates

# 5 Year
# 7 Year
# 10 Year
# 20 Year
# 30 Year


# US CPI
# US Federal Debt Percent
# US Federal Deficit Percent
# US GDP
# US GDP Growth Rate
# US GDP Per Capita
# US Real GDP
# US Real GDP Growth Rate
# US Real GDP Per Capita
# US GDP Deflator
# US Retail Sales
# US Retail Sales Growth
# US Real Retail Sales
# US Real Retail Sales Growth
# US Home Prices
# US Households
# US Married Couples
# US Average Income
# US Average Income Growth
# US Average Real Income
# US Average Real Income Growth
# US Median Income
# US Median Income Growth
# US Median Real Income
# US Median Real Income Growth
# US Income Per Capita
# US Income Per Capita Growth
# US Real Income Per Capita
# US Real Income Per Capita Growth
# US Inflation Rate
# US Population
# US Population Growth Rate
# US Unemployment Rate
# US Long Term Unemployment Rate
# US Employment Population Ratio
# US Labor Force Participation Rate



# Data Sources:
# multpl.com
