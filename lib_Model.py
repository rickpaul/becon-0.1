# TODO:
#	can we make kwargs functions? 
#		(suppose we want to get 2% of data set size for min_samples_split)
#	VERIFY THAT DEC TREE CAN ACCEPT CATEGORICAL VARIABLES!

# EMF 		From...Import
from template_Model 	import EMF_Model_Template
from handle_Model 		import EMF_Model_Handle
# System 	From...Import
from math 				import log

kwargDefaults = {
	'max_depth':			3,
	'min_samples_split':	10,
	'max_leaf_nodes':		20,
	'oob_score':			True,
	'max_features':			None, # n_features for regression, sqrt(n_features) for classification
	'bootstrap':			None, # True for RandomForest, False for ExtraTrees
	'n_jobs':				-1, # Use All Available Cores
}

#Empirical good default values are max_features=n_features for regression problems, and max_features=sqrt(n_features) for classification tasks 
# Good results are often achieved when setting max_depth=None in combination with min_samples_split=1 
# The relative rank (i.e. depth) of a feature used as a decision node in a tree can be used to assess the relative importance of that feature with respect to the predictability of the target variable.
EMF_ClassificationDecisionTree_Info = {
	'model_short_name': 'ClassTree',
	'supervised': True,
	'computational_cost_construction': lambda numSamples, numFeatures: (numSamples*log(numSamples)*numFeatures),
	'computational_cost_query': lambda numSamples, numFeatures: (log(numSamples)),
	'allowed_predVar_types': [
		'categorical_unbounded', 
		'categorical_bounded', 
		'continuous'
	],
	'allowed_respVar_types': [
		'categorical_unbounded',
		'categorical_bounded'
	],
	'kwargs': {
		'max_depth':			3,
		# 'min_samples_split':	10,
		# 'max_leaf_nodes':		20,
		'min_samples_leaf':		2,
	},
}
class EMF_ClassificationDecisionTree(EMF_Model_Handle, EMF_Model_Template):
	def __init__(self, hndl_WordSet):
		self.__dict__ = EMF_ClassificationDecisionTree_Info
		super(EMF_ClassificationDecisionTree, self).__init__(hndl_WordSet)
		from sklearn.tree import DecisionTreeClassifier
		self.model = DecisionTreeClassifier(**self.kwargs)

EMF_RegressionDecisionTree_Info = {
	'model_short_name': 'RegrTree',
	'supervised': True,
	# 'computational_cost_construction': lambda numSamples, numFeatures: (numSamples*log(numSamples)*numFeatures),
	# 'computational_cost_query': lambda numSamples, numFeatures: (log(numSamples)),
	'allowed_predVar_types': [
		'categorical_unbounded', 
		'categorical_bounded',
		'continuous'
	],
	'allowed_respVar_types': [
		'continuous',
	],
	'kwargs': {
		'max_depth':				3,
		# 'min_samples_split':		10,
		# 'min_samples_leaf':		20,
		'min_weight_fraction_leaf': .01,
	},
}
class EMF_RegressionDecisionTree(EMF_Model_Handle, EMF_Model_Template):
	'''
	http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html
	'''
	def __init__(self, hndl_WordSet):
		self.__dict__ = EMF_RegressionDecisionTree_Info
		super(EMF_RegressionDecisionTree, self).__init__(hndl_WordSet)
		from sklearn.tree import DecisionTreeRegressor
		self.model = DecisionTreeRegressor(**self.kwargs)

AvailableModels = {
	'BCM': None,
	'ClassDecisionTree': EMF_ClassificationDecisionTree,
	'RegrDecisionTree': EMF_RegressionDecisionTree,
	'RandomForest':	None,
	'ExtraTrees':	None,
	'Bayesian': None,
	'LinearRegression': None,
}
