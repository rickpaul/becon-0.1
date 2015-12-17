from lib_EMF import HomeDirectory

######################### CSV CODE

CSVRepository = HomeDirectory + 'csv/'
TempQuandlCSV = CSVRepository + 'single_line_QuandlDataSeries.csv'
TestQuandlCSV = CSVRepository + 'QuandlDataSeries.csv'
QAQuandlCSV = CSVRepository + 'QuandlDataSeries.csv'
ProdQuandlCSV = CSVRepository + 'QuandlDataSeries.csv'

QuandlCSVColumns = [
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
	'EMF_periodicity',
	'EMF_DataType',
	'EMF_DataSector	',
]
QuandlCSVColumns = dict(zip(QuandlCSVColumns, xrange(len(QuandlCSVColumns))))

QuandlEditableColumns = [
	QuandlCSVColumns['Q_REFRESHED_AT'],
	QuandlCSVColumns['Q_EARLIEST_DATE'],
	QuandlCSVColumns['Q_LATEST_DATE'],
	QuandlCSVColumns['Q_PERIODICITY'],
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
