class EMF_WordSet:
'''
Defines a set of EMF_Words that can be used to sample variables.
'''
	bound_PredictorPeriodicity = None
	bound_PredictorfirstData = None
	bound_PredictorfinalData = None
	bound_PredictorDataPoints = None
	predictors = []
	transformations = []
	def __init__(self, db_conn, db_cursor):
		pass

	def set_PredictorVariables(self):
		pass

	def set_PredictorBounds(self):
		pass

	def set_TransformationSet(self):
		pass

	def register_SingleTransformation(self):
		pass

	def register_SinglePredictor(self):
		pass

	def createRandomPredictors(self, n=5):
		'''
		creates predictors set 
		'''
		pass

	def createEffectivePredictors(self, n=5, threshhold=0.5):
		'''
		creates predictors based on previous effectiveness of variables
		'''
		pass