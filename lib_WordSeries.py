# TODO:
	# Check if TRANSFORMED, BASIS are deprecated

DATE_COL = 'dates'
VALUE_COL = 'values'

DATE_COL_dtype = (DATE_COL, 'int')
VALUE_COL_dtype = (VALUE_COL, 'float64')

WORD_HISTORY_DTYPE = [DATE_COL_dtype, VALUE_COL_dtype]

WordTypes = [
	'continuous',
	'categorical_unbounded',	# used for, e.g. rounding of normals, where values can be any
	'categorical_bounded'		# used for, e.g. stratification, where values can be any of a range
]