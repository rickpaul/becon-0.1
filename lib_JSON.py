# EMF 		From...Import
from	util_EMF		import 	dt_epoch_to_str_Y_M_D
from 	lib_EMF 		import HomeDirectory

JSONRepository = HomeDirectory + 'json/'

# JSON 
DATA_SERIES_TO_JSON = lambda (dt, vl): {'date': dt_epoch_to_str_Y_M_D(dt), 'value': float(vl)}
WORD_SERIES_TO_JSON = lambda (dt, data_vl, word_vl): {'date': dt_epoch_to_str_Y_M_D(dt), 'raw_val': float(data_vl), proc_val: float(word_vl)}