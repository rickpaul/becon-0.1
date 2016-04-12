from 	lib_DB					import SQLITE_MODE, MYSQL_MODE
from 	lib_EMF					import TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE
# EMF 		Import...As
import lib_Settings


class EMF_Settings_Handle(object):
	DB_MODE = getattr(lib_Settings, 'DB_MODE', None)
	EMF_MODE = getattr(lib_Settings, 'EMF_MODE', None)

	@classmethod
	def init(cls):
		return cls