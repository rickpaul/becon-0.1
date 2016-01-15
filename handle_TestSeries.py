# EMF 		From...Import
from 	template_SerialHandle 	import EMF_Serial_Handle



class EMF_TestSeries_Handle(EMF_Serial_Handle):
	def __init__(self):
		self.values = None
		self.dates = None
		self.values_basis = None
		self.dates_basis = None

	def set_series_values(self, values):
		self.values = values

	def set_series_dates(self, dates):
		self.dates = dates

	def get_series_values(self):
		return self.values

	def get_series_dates(self):
		return self.dates



	# Word Series
	def set_values_basis(self, values):
		self.values_basis = values

	def set_dates_basis(self, dates):
		self.dates_basis = dates

	def get_values_basis(self):
		# For mimicking 
		return self.values

	def get_dates_basis(self):
		return self.dates