from abc import ABCMeta, abstractproperty

class EMF_Series_Template(object):
	__metaclass__ = ABCMeta

	@abstractproperty
	def values(self):
		pass

	@abstractproperty
	def dates(self):
		pass