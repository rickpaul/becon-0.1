# TODO:
#	Move test into own file
# EMF 		From...Import
from 	handle_DataSeries	import EMF_DataSeries_Handle
from 	handle_Model 		import EMF_Model_Handle
from 	handle_Testing 		import EMF_Testing_Handle
from 	handle_WordSet 		import EMF_WordSet_Handle
# EMF 		Import...As
import lib_Model
# System 	Import...As
import numpy as np
# System 	From...Import
from random import choice, randint



class EMF_Model_Runner():
	# Select Data
	# 	Based on Criteria
	# Create Words 
	# Push words into model
	# Run Model
	# Store Results
	# Assess Models
	MIN_BATCH_SIZE = 20
	MAX_BATCH_SIZE = 20
	def __init__(self, DBHandle):
		self.hndl_DB = DBHandle
		self.models = []
		self.periodicity = None
		self.hndl_WordSet = EMF_WordSet_Handle(self.hndl_DB)


	def register_models(self, modelName):
		if modelName is None:
			self.models = lib_Model.AvailableModels
		else:
			self.models.append(lib_Model.AvailableModels[modelName])

	def register_independent_variable(self, indTicker):
		self.hndl_WordSet

	def set_model_from_template(self, template):


	def run_model_batch(self, wordSet=None):
		# Choose Model at random
		hndl_Model = choice(self.models)()
		# Generate Words
		if wordSet is None:
			pass
		# Run Batches
		batch_size = randint(MIN_BATCH_SIZE, MAX_BATCH_SIZE)
		for i in xrange(batch_size):
			self.__iterate(hndl_Model)

	def __iterate(self, model, wordSet):
		pass

	def __assess_model(self):
		pass
		# if bad model, register dataSeries and transformations as not-helpful

		# if good model, register dataSeries and transformations as helpful 
		# if good model, store feature-importances



# Test Below
def save_test_data(hndl_Test):
	np.random.seed(0)
	from sklearn.datasets import make_blobs
	numDims = 10
	dataLen = 5*numDims
	X, y = make_blobs(n_samples=dataLen, n_features=numDims, centers=2*numDims)
	dt = np.arange(dataLen)
	dataNames = ['X'+str(i) for i in xrange(numDims)]
	hndl_Test.insert_test_data(dt, X, dataNames)
	hndl_Test.insert_test_data(dt, y, ['clusterNum'])


def create_word_set(hndl_Test):
	hndl_WordSet = EMF_WordSet_Handle(hndl_Test.hndl_DB) #
	ind_data = EMF_DataSeries_Handle(hndl_Test.hndl_DB) #
	ind_data.set_data_series('clusterNum') #
	periodicity = ind_data.get_periodicity()
	earliestDate = ind_data.get_earliest_date()
	latestDate = ind_data.get_latest_date()
	hndl_WordSet.set_data_series_criteria(	periodicity=periodicity, 
											atLeastEarly=earliestDate,
											atLeastLate=latestDate,
											ignoreTickers=['clusterNum'])
	hndl_WordSet.set_independent_data_series(ind_data)
	hndl_WordSet.set_independent_transformation('None')
	hndl_Test.hndl_WordSet = hndl_WordSet

def run_model(hndl_Test):
	hndl_WordSet = hndl_Test.hndl_WordSet
	model = lib_Model.EMF_ClassificationDecisionTree()
	model.add_independent_variable(hndl_WordSet.get_independent_word_handle(), 'categorical_bounded')
	depWords = hndl_WordSet.get_dependent_word_handles_random_subset()
	for wordHandle in depWords:
		model.add_dependent_variable(wordHandle, 'continuous')
	model.run_model()

def main():
	hndl_Test = EMF_Testing_Handle()
	save_test_data(hndl_Test)
	create_word_set(hndl_Test)
	run_model(hndl_Test)

if __name__ == '__main__':
	main()