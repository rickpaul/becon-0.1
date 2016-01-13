# EMF 		From...Import
# EMF 		Import...As
# System 	Import...As
import pandas as pd
# System 	From...Import

class EMF_Results_Handle():
	def __init__(self):
		self.dates = None
		self.models = {}
		self.predictionFeatures = {}
		self.respWord = None
		self.modelIdx = 1
		self.predictionArray = None # Panda Array of size (dates)x(models)

	def __add_predictions(self, hndl_Model):
		dates = hndl_Model.get_series_dates()
		values = hndl_Model.get_series_values()
		model_name = str(hndl_Model)
		newValues = pd.DataFrame({self.modelIdx: values.ravel()}, index=dates.ravel())
		if self.predictionArray is None:
			self.predictionArray = newValues
		else:
			self.predictionArray = pd.concat([self.predictionArray, newValues], axis=1, ignore_index=False)
		self.models[self.modelIdx] = model_name
		self.modelIdx += 1

	# def __add_features(self, hndl_Model):


	def add_model(self, hndl_Model):
		if self.respWord is None:
			self.respWord = hndl_Model.hndl_WordSet.respWord
		self.__add_predictions(hndl_Model)
		# self.__add_features(hndl_Model)