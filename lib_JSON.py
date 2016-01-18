# EMF 		From...Import
from	util_TimeSet	import dt_epoch_to_str_Y_M_D
from 	lib_EMF 		import HomeDirectory

JSONRepository = HomeDirectory + 'json/'
JSONSuffix = '.json'

JSON_MODEL_METADATA_SUFFIX  = 'metadata'
JSON_MODEL_PREDICTIONS_SUFFIX  = 'predictions'
JSON_MODEL_HISTORY_SUFFIX  = 'history'


JSON_DATE_KEY = 'dt'
JSON_VALUE_KEY = 'vl'

JSON_MODEL_ID = 'model_id'
JSON_MODEL_CONFIDENCE = 'confidence'
JSON_MODEL_DESC = 'model_desc'

# LAMBDAS
DATA_SERIES_TO_JSON = lambda d, v: {JSON_DATE_KEY: dt_epoch_to_str_Y_M_D(d), JSON_VALUE_KEY: float(v)}
# WORD_SERIES_TO_JSON = lambda (dt, data_vl, word_vl): {'dt': dt_epoch_to_str_Y_M_D(dt), 'raw_val': float(data_vl), 'proc_val': float(word_vl)}

