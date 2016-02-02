from abc import ABCMeta, abstractproperty


class EMF_Serial_Handle(object):
	__metaclass__ = ABCMeta

	@abstractproperty
	def values(self):
		pass

	@abstractproperty
	def dates(self):
		pass