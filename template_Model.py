from abc import ABCMeta, abstractmethod

class EMF_Model_Template:
	__metaclass__ = ABCMeta

	@abstractmethod
	def determine_accuracy(self):
		pass

	@abstractmethod
	def run_model(self):
		pass

	@abstractmethod
	def save_model(self):
		pass

	@abstractmethod
	def evaluate_model(self):
		pass