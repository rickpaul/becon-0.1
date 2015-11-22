from EMF_lib import HomeDirectory

######################### CSV CODE

loadCSVRepository = HomeDirectory + 'dataloader/csv/'
QuandlCSVLocation = loadCSVRepository + 'QuandlDataSeries.csv'

QuandlCSVColumns = [
	'source',
	'name'
	'ticker',
	'Q_DATABASE_CODE',
	'Q_DATASET_CODE',
	'Q_COLUMN_NUM',
	'Q_COLLAPSE_INSTR',
	'Q_TRANSFORM_INSTR',
	'Q_REFRESHED_AT',
	'Q_EARLIEST_DATE',
	'Q_LATEST_DATE',
	'periodicity',
]
QuandlCSVColumns = dict(zip(QuandlCSVColumns, xrange(1,len(QuandlCSVColumns)+1)))


######################### API CODE
QuandlAPIKey = 'pmM4BUFqzx1FetXxbj1x'

dataURL = 'https://www.quandl.com/api/v3/datasets/{db}/{ds}/data.json'
metaDataURL = 'https://www.quandl.com/api/v3/datasets/{db}/{ds}/metadata.json'
dataAndMetaDataURL = 'https://www.quandl.com/api/v3/datasets/{db}/{ds}.json'


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
