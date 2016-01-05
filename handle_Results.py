# EMF 		From...Import
# EMF 		Import...As
# System 	Import...As
import pandas as pd
# System 	From...Import

class EMF_Results_Handle():
	def __init__(self):
		self.dates = None
		self.models = None
		self.predictionArray = None # Panda Array of size (dates)x(models)

	def __add_predictions(self, model):
		dates = model.get_series_dates()
		values = model.get_series_values()
		model_id = str(model)
		newValues = pd.DataFrame(values, columns=[model_id], index=dates)
		if self.predictionArray is None:
			self.predictionArray = newValues
		else:
			self.predictionArray = pd.concat([self.predictionArray, newValues], axis=1, join='outer')


	def __add_features(self, model):
		raise NotImplementedError

	# def __add_feature()

	def add_model(self, model):
		self.__add_predictions(model)
		#self.__add_features(model)