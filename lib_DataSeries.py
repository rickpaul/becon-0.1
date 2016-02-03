

# NUMPY VALUES
DATE_COL = 'dates'
VALUE_COL = 'values'
DATE_COL_dtype = (DATE_COL, 'int')
VALUE_COL_dtype = (VALUE_COL, 'float64')
DATA_HISTORY_DTYPE = [DATE_COL_dtype, VALUE_COL_dtype]

# MEANINGS (AND OPPOSITES)
DataMeanings = {
	'weakness': 'strength',
	'strength': 'weakness',
	'pessimism': 'optimism',
	'optimism': 'pessimism',
	'stress': 'low stress',
	'cost': 'cheap',
}