import 	EMF_Quandl_lib as quandlLib
from 	EMF_CSVHandle 			import EMF_CSV_Handle 		as csvHandle
from 	EMF_QuandliAPIHandle	import EMF_QuandlAPI_Handle as quandlHandle

class EMF_Quandl_Runner:
	def __init__(self):
		self.CSVHandle = csvHandle(quandlLib.QuandlCSVLocation)
		self.QndlHandle = quandlHandle()
