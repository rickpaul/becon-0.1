
from lib_EMF import HomeDirectory

# DB Modes
SQLITE_MODE = 'SQLITE'
MYSQL_MODE = 'MYSQL'

# SQLite DB Directories
DBRepository = HomeDirectory + 'database/'
ProdDB_SQLite = DBRepository + 'prod_economicData.db'
QADB_SQLite = DBRepository + 'qa_economicData.db'
TestDB_SQLite = DBRepository + 'test_economicData.db'
TempDB_SQLite = DBRepository + 'delete_me.db'

# MySQL DB Parameters
username='root'
password='[]{}[]'
host='localhost'
ProdDB_MySQL = 'EMF_prod'
QADB_MySQL   = 'EMF_qa'
TestDB_MySQL = 'EMF_test'
TempDB_MySQL = 'EMF_temp'