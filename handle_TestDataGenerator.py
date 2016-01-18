# EMF 		From...Import
from 	lib_JSON			import DATA_SERIES_TO_JSON
from 	lib_JSON			import JSON_DATE_KEY, JSON_VALUE_KEY, JSON_MODEL_ID
from 	lib_JSON			import JSON_MODEL_DESC, JSON_MODEL_CONFIDENCE
from 	util_EMF 			import dt_str_YYYY_MM_DD_to_epoch, dt_epoch_to_str_Y_M_D
from 	util_Transformation import transform_FOD_BackwardLooking
from 	util_JSON			import get_json_history_path, get_json_predictions_path, get_json_model_path
from 	util_JSON			import save_to_JSON

# EMF 		Import...As
import 	util_Testing 		as util_Tst
# System 	Import...As
# System 	From...Import
from 	math 				import sqrt
from 	numpy 				import std as np_std
from 	numpy.random 		import normal
from 	numpy.random 		import random

class EMF_TestDataGenerator:
	def __init__(self):
		pass


	def generate_d3_JSON_ParallelCoords(self):
		# Generate 'History'
		n = 120 # 10 years
		n_fd = 12
		series = util_Tst.create_test_data_correlated_returns(n=n, numDims=1, includeResponse=False)
		dt = util_Tst.create_monthly_date_range(n=n)
		vals = series['data']
		json_history = [DATA_SERIES_TO_JSON(d,v) for (d,v) in zip(dt, vals)]
		# Generate Predictions
		std = np_std(transform_FOD_BackwardLooking(vals,{'PeriodDiff':1}))
		end_val = vals[-1,0]
		def get_random_prediction_values(per_fd):
			numPreds = 40
			preds = []
			for i in xrange(numPreds):
				preds.append(end_val + normal()*std*sqrt(per_fd))
			return (range(numPreds), preds)
		def get_model_metadata(model_idx):
			return {
				JSON_MODEL_ID :			model_idx, 
				JSON_MODEL_CONFIDENCE :	random(), 
				JSON_MODEL_DESC :		'junkdesc ' + str(model_idx)	
			}
		end_dt = dt[-1]
		prd_dt = util_Tst.create_monthly_date_range(n=n_fd+1, startEpoch=end_dt+10000) #hacky, but end of next month
		models = {}
		preds = []
		for (i, dt) in enumerate(prd_dt):
			(model_idxs, pred_values) = get_random_prediction_values(i)
			models.update(dict.fromkeys(model_idxs))
			for (md, vl) in zip(model_idxs, pred_values):
				preds.append({
					JSON_MODEL_ID: md,
					JSON_DATE_KEY: dt_epoch_to_str_Y_M_D(dt),
					JSON_VALUE_KEY: vl
				})
		for md in models.keys():
			models[md] = get_model_metadata(md)
		# Save data
		dataName = 'test1'
		filePath = get_json_history_path(dataName)
		save_to_JSON(filePath, json_history)
		filePath = get_json_predictions_path(dataName)
		save_to_JSON(filePath, preds)
		filePath = get_json_model_path(dataName)
		save_to_JSON(filePath, models)


# if __name__ == '__main__':
# 	generator = EMF_TestDataGenerator()
# 	generator.generate_d3_JSON_ParallelCoords()