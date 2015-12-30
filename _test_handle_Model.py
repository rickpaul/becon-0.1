# TODOS:
#	This isn't actually a test yet.

# EMF 		From...Import
from 	handle_Testing 	import EMF_Testing_Handle
from 	util_Testing 	import save_test_data_blobs
# EMF 		Import...As
import 	lib_Model

def run_model(hndl_Test):
	model = lib_Model.EMF_ClassificationDecisionTree()
	model.add_dependent_variable(hndl_Test.retrieve_test_word('X0','None'))
	model.add_dependent_variable(hndl_Test.retrieve_test_word('X1','None'))
	model.add_independent_variable(hndl_Test.retrieve_test_word('clusterNum','None'))
	model.run_model()

def main():
	hndl_Test = EMF_Testing_Handle()
	save_test_data_blobs(hndl_Test)
	run_model(hndl_Test)

if __name__ == '__main__':
	main()