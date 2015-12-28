# TODO:
#	can we make kwargs functions? 
#		(suppose we want to get 2% of data set size for min_samples_split)

from template_Model import EMF_Model_Template
from handle_Model import EMF_Model_Handle
from math import log

kwargDefaults = {
	'max_depth':			3,
	'min_samples_split':	10,
	'max_leaf_nodes':		20,
	'oob_score':			True,
	'max_features':			None, # n_features for regression, sqrt(n_features) for classification
	'bootstrap':			None, # True for RandomForest, False for ExtraTrees
	'n_jobs':				-1, # Use All Available Cores
}


# BCM = {
# 	'supervised': False,
# 	'dependent_variables': ['categorical'],
# 	'kwargs': [],
# }

#Empirical good default values are max_features=n_features for regression problems, and max_features=sqrt(n_features) for classification tasks 
# Good results are often achieved when setting max_depth=None in combination with min_samples_split=1 
# The relative rank (i.e. depth) of a feature used as a decision node in a tree can be used to assess the relative importance of that feature with respect to the predictability of the target variable.
EMF_ClassificationDecisionTree_Info = {
	'supervised': True,
	'computational_cost_construction': lambda numSamples, numFeatures: (numSamples*log(numSamples)*numFeatures),
	'computational_cost_query': lambda numSamples, numFeatures: (log(numSamples)),
	'allowed_dependent_variable_types': [
		'categorical_unbounded', 
		'categorical_bounded', 
		'continuous'
	],
	'allowed_independent_variable_types': [
		'categorical_unbounded',
		'categorical_bounded'
	],
	'kwargs': {
		'max_depth':			3,
		# 'min_samples_split':	10,
		# 'max_leaf_nodes':		20,
	},
}
class EMF_ClassificationDecisionTree(EMF_Model_Handle, EMF_Model_Template):
	def __init__(self):
		self.__dict__ = EMF_ClassificationDecisionTree_Info
		super(EMF_ClassificationDecisionTree, self).__init__()
		from sklearn.tree import DecisionTreeClassifier
		self.model = DecisionTreeClassifier(**self.kwargs)

	def determine_accuracy(self):
		raise NotImplementedError

	def save_model(self):
		raise NotImplementedError

	def evaluate_model(self):
		raise NotImplementedError

EMF_RegressionDecisionTree_Info = {
	'supervised': True,
	# 'computational_cost_construction': lambda numSamples, numFeatures: (numSamples*log(numSamples)*numFeatures),
	# 'computational_cost_query': lambda numSamples, numFeatures: (log(numSamples)),
	'allowed_dependent_variable_types': [
		'categorical_unbounded', 
		'categorical_bounded',
		'continuous'
	],
	'allowed_independent_variable_types': [
		'continuous',
	],
	'kwargs': {
		'max_depth':			3,
		# 'min_samples_split':	10,
		# 'min_samples_leaf':		20,
		'min_weight_fraction_leaf': .01,
	},
}
class EMF_RegressionDecisionTree(EMF_Model_Handle, EMF_Model_Template):
	'''
	http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html
	'''
	def __init__(self):
		self.__dict__ = EMF_RegressionDecisionTree_Info
		super(EMF_RegressionDecisionTree, self).__init__()
		from sklearn.tree import DecisionTreeRegresson
		self.model = DecisionTreeRegresson(**self.kwargs)

	def determine_accuracy(self):
		'''
		Gives R^2 of test set
		
		'''
		raise NotImplementedError
		return self.model.score(test_IndVars, test_DepVars, sample_weights)

	def feature_importances(self):
		raise NotImplementedError

# OrdinaryLeastSquares = {
# 	'supervised': True,
# 	'dependent_variables': [
# 		'continuous'
# 	],
# 	'independent_variables': [
# 		'continuous'
# 	],
# }

AvailableModels = {
	'BCM': None,
	'ClassDecisionTree': EMF_ClassificationDecisionTree,
	'RegrDecisionTree': EMF_RegressionDecisionTree,
	'RandomForest':	None,
	'ExtraTrees':	None,
	'Bayesian': None,
	'Regression': None,
}
