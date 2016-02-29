
# EMF 		From...Import
from 	handle_ColumnArray 		import EMF_ColumnArray_Handle
from 	util_Results			import get_prediction_array_path, get_results_metadata_path

# System 	Import...As
import 	pandas	 				as pd


class EMF_Results_Peeker(object):

def __columnArrayPeeker(self, fileName):
	column_array = pickle.load(open(self.file_name,'rb'))
	columns = column_array.columns
	num_columns = len(columns)