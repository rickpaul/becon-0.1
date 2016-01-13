from abc import ABCMeta, abstractmethod

class EMF_Model_Template:
	__metaclass__ = ABCMeta

	@abstractmethod
	def train_model(self):
		pass

	@abstractmethod
	def determine_accuracy(self, test_predVars, test_respVars, sample_weights=None):
		pass

	@abstractmethod
	def feature_importances(self):
		pass

	@abstractmethod
	def save_model(self):
		pass

	@abstractmethod
	def evaluate_model(self):
		pass
