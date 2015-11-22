# TODOS:
#	Make cleaner
#	Test __getFromDB/__sendToDB

from EMF_Database_lib import DBRepository
import EMF_DatabaseCreator
import EMF_DatabaseCreator_util
import numpy as np
import sqlite3 as sq
from os import remove
DBFilePath = DBRepository + 'delete_me.db'
conn = None

def createTestDB():
	'''
	TODOS:
	Refactor this into own testing library
	'''
	tableCreationInstructions = EMF_DatabaseCreator.fullTableCreationInstructions
	EMF_DatabaseCreator_util.doOneTimeDBCreation(DBFilePath, tableCreationInstructions, force=True)


def testDataSeriesHandle(conn, cursor):
	np.random.seed(10)
	dates = np.reshape(np.arange(200),(200,))
	data = np.random.randint(100,size=(200,))/2.0
	dataHandle = EMF_DataSeries_Handle(conn, cursor)
	name = 'testSeries'
	ticker = 'test'
	dataHandle.setDataSeries(name=name, ticker=ticker)	
	assert dataHandle.dataName == name
	assert dataHandle.dataTicker == ticker
	dataHandle.insertDataHistory(dates, data)
	dataSeries = dataHandle.getDataHistory()
	assert np.all(dataSeries['date'] == dates)
	assert np.all(dataSeries['value'] == data)
	dataHandle.unsetDataSeries()	
	assert dataHandle.dataName == None
	assert dataHandle.dataTicker == None


def cleanupDB():
	if conn is not None:
		conn.close()
	remove(DBFilePath)

def main():
	try:
		createTestDB()
		conn = sq.connect(DBFilePath)
		cursor = conn.cursor()
		testDataSeriesHandle(conn, cursor)

	except Exception, e:
		raise
	else:
		pass
	finally:
		cleanupDB()

if __name__ == '__main__':
	main()