
from lib_EMF import HomeDirectory

DBRepository = HomeDirectory + 'database/'

ProdDBFilePath = DBRepository + 'prod_economicData.db'
QADBFilePath = DBRepository + 'qa_economicData.db'
TestDBFilePath = DBRepository + 'test_economicData.db'

TempDBFilePath = DBRepository + 'delete_me.db'