import lib_Model
import numpy as np
from handle_Testing import EMF_Testing_Handle

def save_test_data(hndl_Test):
	np.random.seed(0)
	from sklearn.datasets import make_blobs
	dataLen = 200
	X, y = make_blobs(n_samples=dataLen, n_features=2, centers=4)
	dt = np.arange(dataLen)
	hndl_Test.insert_test_data(dt, X, ['X0', 'X1'])
	hndl_Test.insert_test_data(dt, y, ['clusterNum'])
	hndl_Test.create_word_from_data('X0', 'None')
	hndl_Test.create_word_from_data('X1', 'None')
	hndl_Test.create_word_from_data('clusterNum', 'None')

def run_model(hndl_Test):
	model = lib_Model.ClassificationDecisionTree()
	model.add_dependent_variable(hndl_Test.retrieve_word('X0|None'), 'continuous')
	model.add_dependent_variable(hndl_Test.retrieve_word('X1|None'), 'continuous')
	model.add_independent_variable(hndl_Test.retrieve_word('clusterNum|None'), 'categorical_bounded')
	model.run_model()

def main():
	hndl_Test = EMF_Testing_Handle()
	save_test_data(hndl_Test)
	run_model(hndl_Test)

if __name__ == '__main__':
	main()