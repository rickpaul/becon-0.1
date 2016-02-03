from abc import ABCMeta, abstractmethod, abstractproperty

class EMF_Model_Template:
	__metaclass__ = ABCMeta


	@abstractmethod
	def train_model(self):
		pass

	@abstractmethod
	def determine_accuracy(self, test_predVars, test_respVars, sample_weights=None):
		pass

	@abstractmethod
	def save_model(self):
		pass

	@abstractmethod
	def model_stats(self):
		pass

	@abstractproperty
	def feature_importances(self):
		pass

	@abstractproperty
	def desc(self):
		pass
