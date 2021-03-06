# EMF 		From...Import
from 	lib_JSON		import DATA_SERIES_TO_JSON
from 	lib_JSON		import JSON_DATE_KEY, JSON_VALUE_KEY, JSON_MODEL_ID, JSON_MODEL_CATS
from 	util_TimeSet	import dt_epoch_to_str_Y_M_D
from 	util_JSON		import save_to_JSON
from 	util_JSON		import get_json_history_path, get_json_predictions_path, get_json_model_path
# System 	Import...As
import 	logging 	as log

class EMF_JSON_Handle():
	def __init__(self):	
		pass

	def generate_d3_JSON_2D_Map(self, word1, word2):
		pass

	def generate_d3_JSON_ParallelCoords(self, hndl_Res):
		# Historical Line Graph
		# Historical Line Graph / Get History Line
		(history_dates, history_values) = hndl_Res.get_resp_word_raw_values()
		json_history = [DATA_SERIES_TO_JSON(d,v) for (d,v) in zip(history_dates, history_values)]
		# Historical Line Graph / Write History Line
		filePath = get_json_history_path(hndl_Res.file_name)
		save_to_JSON(filePath, json_history)
		# Parallel Coordinates
		# Parallel Coordinates / Get Parallel Coords Points
		models = {}
		preds = []
		for dt in hndl_Res.get_prediction_dates():
			(model_idxs, pred_values) = hndl_Res.get_values_by_row(dt)
			models.update(dict.fromkeys(model_idxs))
			for (md, vl) in zip(model_idxs, pred_values):
				preds.append({
					JSON_MODEL_ID: md,
					JSON_DATE_KEY: dt_epoch_to_str_Y_M_D(dt),
					JSON_VALUE_KEY: vl
				})
		# Parallel Coordinates / Write Parallel Coords Points
		filePath = get_json_predictions_path(hndl_Res.file_name)
		save_to_JSON(filePath, preds)
		# Metadata
		# Metadata / Get Model Metadata
		for md in models.keys():
			models[md] = hndl_Res.get_model_metadata(md)
		# Metadata / Write Model Metadata
		filePath = get_json_model_path(hndl_Res.file_name)
		save_to_JSON(filePath, models)
		