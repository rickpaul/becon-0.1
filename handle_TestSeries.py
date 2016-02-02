# EMF 		From...Import
from 	template_SerialHandle 	import EMF_Serial_Handle

class EMF_TestSeries_Handle(EMF_Serial_Handle):
	def __init__(self):
		self._values = None
		self._dates = None

	def values():
	    doc = "The values property."
	    def fget(self):
	        return self._values
	    def fset(self, value):
	        self._values = value
	    def fdel(self):
	        del self._values
	    return locals()
	values = property(**values())


	def dates():
	    doc = "The dates property."
	    def fget(self):
	        return self._dates
	    def fset(self, value):
	        self._dates = value
	    def fdel(self):
	        del self._dates
	    return locals()
	dates = property(**dates())