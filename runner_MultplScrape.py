# EMF 		From...Import
from 	handle_DB		 	import EMF_Database_Handle
from 	handle_DataSeries 	import EMF_DataSeries_Handle
from 	handle_Logging		import EMF_Logging_Handle
from 	lib_EMF		 		import TEMP_MODE
from	util_EMF			import get_EMF_settings

from 	bs4 				import BeautifulSoup



class EMF_Multpl_Runner:
	def __init__(self, mode=TEMP_MODE):
		settings = get_EMF_settings(mode)
		self.hndl_Log = EMF_Logging_Handle(mode=mode)
		self.hndl_DB = EMF_Database_Handle(settings['dbLoc'])

