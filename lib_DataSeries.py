
# NUMPY VALUES
DATE_COL = 'dates'
VALUE_COL = 'values'
DATE_COL_dtype = (DATE_COL, 'int')
VALUE_COL_dtype = (VALUE_COL, 'float64')
DATA_HISTORY_DTYPE = [DATE_COL_dtype, VALUE_COL_dtype]

Periodicity = {
	'daily' 	: 	365,
	'weekly'	:	52,
	'monthly'	:	12,
	'quarterly'	:	4,
	'annually'	:	1,
}

