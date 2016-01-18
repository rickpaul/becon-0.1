from abc import ABCMeta, abstractmethod


class EMF_Serial_Handle(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def get_series_values(self):
		pass

	@abstractmethod
	def get_series_dates(self):
		pass