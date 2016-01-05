# EMF 		From...Import
# EMF 		Import...As
# System 	Import...As
import pandas as pd
# System 	From...Import

class EMF_Results_Handle():
	def __init__(self):
		self.dates = None
		self.models = None
		self.predictionArray = None # Array of size (dates)x(models)

	def add_predictions(self, model):
		dates = model.get_dates()
		values = model.predictions
		model_id = model.get_identifier()
		newValues = pd.DataFrame(values, column=[model_id], index=dates)
		if self.predictionArray is None:
			self.predictionArray = newValues
		else:
			pd.concatenate([self.predictionArray, newValues], axis=1)


	def 

	def add_model(self, model):
		raise NotImplementedError