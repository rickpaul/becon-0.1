from abc import ABCMeta, abstractmethod, abstractproperty

class EMF_Database_Template(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def connect_to_DB(self):
		pass

	@abstractmethod
	def __del__(self):
		pass

	@abstractproperty
	def conn(self):
		pass

	@abstractproperty
	def cursor(self):
		pass