from EMF_lib import HomeDirectory

######################## DATABASE CODE
DBRepository = HomeDirectory + 'database/'
ProdDBFilePath = DBRepository + 'prod_economicData.db'
QADBFilePath = DBRepository + 'qa_economicData.db'
TestDBFilePath = DBRepository + 'test_economicData.db'

testDB = TestDBFilePath
defaultDB = TestDBFilePath