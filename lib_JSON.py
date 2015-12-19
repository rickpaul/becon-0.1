# EMF 		From...Import
from	util_EMF		import 	dtConvert_EpochtoY_M_D
from 	lib_EMF 		import HomeDirectory

JSONRepository = HomeDirectory + 'json/'

# JSON 
DATA_SERIES_TO_JSON = lambda (dt, vl): {'date': dtConvert_EpochtoY_M_D(dt), 'value': float(vl)}
WORD_SERIES_TO_JSON = lambda (dt, data_vl, word_vl): {'date': dtConvert_EpochtoY_M_D(dt), 'raw_val': float(data_vl), proc_val: float(word_vl)}