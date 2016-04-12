# TODO:
#	can we make kwargs functions? We want to pass in dynamic values
#		(suppose we want to get 2% of data set size for min_samples_split)
# 	We're not using kwargDefaults
#	VERIFY THAT DEC TREE CAN ACCEPT CATEGORICAL VARIABLES!
# 	Instead of using Categorical Bounded, we should have Categorical Ordered

# EMF 		From...Import
from template_Model 	import EMF_Model_Template
from handle_Model 		import EMF_Model_Handle
# System 	From...Import
from math 				import log
from string 			import join

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
	'model_ID': 2,
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

	def save_model_attributes(self, pred_words, resp_word):
		pass

EMF_RegressionDecisionTree_Info = {
	'model_ID': 1,
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
		'max_depth':				4,
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

	def save_model_attributes(self, pred_words, resp_word):
		raise NotImplementedError
		left = self.model.tree_.children_left
		right = self.model.tree_.children_right
		threshold = self.model.tree_.threshold
		value = self.model.tree_.value
		features  = [str(pred_words[i]) for i in self.model.tree_.feature]

		def recurse(left, right, threshold, features, node):
			if (threshold[node] != -2):
				print "if ( " + features[node] + " <= " + str(threshold[node]) + " ) {"
				if left[node] != -1:
					 recurse (left, right, threshold, features,left[node])
				print "} else {"
				if right[node] != -1:
					recurse (left, right, threshold, features,right[node])
				print "}"
			else:
				print "return " + str(value[node])
	 	recurse(left, right, threshold, features, 0)


############# LINEAR REGRESSION

EMF_OLSRegression_Info = {
	'model_ID': 3,
	'model_short_name': 'OLSLinearRegression',
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
	'kwargs': {},
}
class EMF_OLSRegression(EMF_Model_Handle, EMF_Model_Template):
	'''
	http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
	'''
	def __init__(self, hndl_WordSet):
		self.__dict__ = EMF_OLSRegression_Info
		super(EMF_OLSRegression, self).__init__(hndl_WordSet)
		from sklearn.linear_model import LinearRegression
		self.model = LinearRegression(**self.kwargs)

	def save_model_attributes(self, pred_words, resp_word):
		pass

AvailableModels = {
	'BCM': None,
	'ClassDecisionTree': EMF_ClassificationDecisionTree,
	'RegrDecisionTree': EMF_RegressionDecisionTree,
	'RandomForest':	None,
	'ExtraTrees':	None,
	'Bayesian': None,
	'LinearRegression': EMF_OLSRegression,
	'ARDRegression': None,
	'BayesianRidgeRegression': None,
	'RANSACRegression': None,
	'TheilSenRegression': None,
}
