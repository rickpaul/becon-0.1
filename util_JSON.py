from 	lib_JSON		import JSON_MODEL_PREDICTIONS_SUFFIX, JSON_MODEL_METADATA_SUFFIX, JSON_MODEL_HISTORY_SUFFIX
from 	lib_JSON		import JSONSuffix
from 	lib_Website 	import WebRepository
# System 	From...Import
from 	json 			import dump, loads


def get_json_history_path(dataName):
	return '{0}{1}{2}{3}'.format(	WebRepository, 
									dataName,
									JSON_MODEL_HISTORY_SUFFIX,
									JSONSuffix)
def get_json_predictions_path(dataName):
	return '{0}{1}{2}{3}'.format(	WebRepository, 
									dataName,
									JSON_MODEL_PREDICTIONS_SUFFIX,
									JSONSuffix)
def get_json_model_path(dataName):
	return '{0}{1}{2}{3}'.format(	WebRepository, 
									dataName,
									JSON_MODEL_METADATA_SUFFIX,
									JSONSuffix)


def save_to_JSON(filePath, json_data, overwrite=True):
	if overwrite:
		flag = 'wb'
	else:
		raise NotImplementedError
	with open(filePath, flag) as writer:
		dump(json_data, writer)

def load_from_JSON(filePath):
	return load(filePath)