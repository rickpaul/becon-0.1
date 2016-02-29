

# NUMPY DTYPE VALUES
DATE_COL = 'dates'
VALUE_COL = 'values'
DATE_COL_dtype = (DATE_COL, 'int')
VALUE_COL_dtype = (VALUE_COL, 'float64')
DATA_HISTORY_DTYPE = [DATE_COL_dtype, VALUE_COL_dtype]

# DIRECTIONALITY MEANINGS (AND OPPOSITES)
DATA_DIRECTIONALITY_MEANINGS = {
	'weakness'		: 'strength',
	'strength'		: 'weakness',
	'pessimism'		: 'optimism',
	'optimism'		: 'pessimism',
	'stress'		: 'low stress',
	'cost'			: 'cheap',
}

DATA_CATEGORY_NICE = {
	'fixed_income' 	: 'interest rates',
	'production' 	: 'company production',
	'economy' 		: 'overall economy',
	'equity' 		: 'stock market',
	'labor' 		: 'labor market',
	'housing' 		: 'housing market',
}