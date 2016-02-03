# DELETE THIS
# 	Only useful in specific circumstances

# EMF 		From...Import
from 	lib_EMF			import TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE
from 	util_CreateDB 	import create_or_connect_to_DB
# EMF 		Import...As
# System 	From...Import
from 	sys 		import argv

if __name__ == '__main__':
	# Read Arguments
	args = argv[1:]
	kwargs = {}
	if len(args):
		if ('-mode-TEMP' in args): kwargs['mode'] = TEMP_MODE
		if ('-mode-TEST' in args): kwargs['mode'] = TEST_MODE
		if ('-mode-QA' in args):   kwargs['mode'] = QA_MODE
		if ('-mode-PROD' in args): kwargs['mode'] = PROD_MODE
		if ('-manual' in args):    kwargs['manualOverride'] = True
	create_or_connect_to_DB(**kwargs)
