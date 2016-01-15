# EMF 		From...Import
from 	lib_Pickle 		import PickleRepository, PickleSuffix
from 	lib_JSON		import JSONRepository, JSONSuffix


def get_prediction_array_path(dataName):
	return '{0}{1}{2}'.format(	PickleRepository, 
								dataName, 
								PickleSuffix)


def get_results_metadata_path(dataName):
	return '{0}{1}{2}'.format(	JSONRepository, 
								dataName, 
								JSONSuffix)
