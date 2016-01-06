# EMF 		From...Import
from 	template_SerialHandle 	import EMF_Serial_Handle



class EMF_TestSeries_Handle(EMF_Serial_Handle):
	def __init__(self):
		self.values = None
		self.dates = None

	def set_series_values(self, values):
		self.values = values

	def set_series_dates(self, dates):
		self.dates = dates

	def get_series_values(self):
		return self.values

	def get_series_dates(self):
		return self.dates