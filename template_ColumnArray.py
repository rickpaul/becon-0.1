from abc import ABCMeta, abstractmethod, abstractproperty

class EMF_ColumnArray_Template(object):
	__metaclass__ = ABCMeta

	@abstractproperty
	def log_prefix(self):
		pass

	@abstractproperty
	def metadata_file_path(self):
		pass

	@abstractproperty
	def array_file_path(self):
		pass