# TODO:
#	Implement file versioning system for backups (somehow)
# 	Move test to other file!

# EMF 		From...Import
import 	UnicodeCSV
# System 	Import...As
import logging as log
# System 	From...Import
from 	os.path 	import isfile
from 	os 			import remove
from 	shutil 		import copy2

class EMF_CSV_Handle:
	def __init__(self, csvFileName, columnIndexes=None, editableColumns=None, hasHeader=True):
		self.csvFileName = csvFileName
		self.columnIndexes = columnIndexes
		self.editableColumns = editableColumns
		self.changedContent = None
		self.hasChanged = False
		self.hasHeader = hasHeader
		self.__read_from_CSV(hasHeader)

	def __read_from_CSV(self, hasHeader):
		with open(self.csvFileName, 'rU') as csvFile:
			csvReader = UnicodeCSV.UnicodeReader(csvFile)
			if self.hasHeader:
				self.csvHeader = [next(csvReader)] # Save off header in CSV
			self.fileContent = [list(row) for row in csvReader]
			self.nextRow = 0
			self.contentLength = len(self.fileContent)

	def __iter__(self):
		return self

	def next(self): #__next__(self): in 3.x
		if self.nextRow >= self.contentLength:
			raise StopIteration
		else:
			self.nextRow += 1
			return self.fileContent[self.nextRow-1]

	def change_current_row(self, newValue, columnName=None, columnIndex=None):
		'''

		RETURNS:
					<bool>	Success of operation
		'''
		# Check if Column Name is Sent
		assert ((columnName is not None) or (columnIndex is not None))
		# Convert Column Name to Column Index
		if columnName is not None:
			if columnIndex is None:
				columnIndex = self.columnIndexes[columnName]
			else:
				assert columnIndex == self.columnIndexes[columnName] #Necessary Check?
		# Check if Column Name is Editable
		if self.editableColumns is not None:
			if columnName not in self.editableColumns:
				return False
		# Perform Value Replacement
		currentRow = self.nextRow-1
		currentValue = self.fileContent[currentRow][columnIndex]
		if currentValue == newValue:
			return False
		self.hasChanged = True
		self.fileContent[currentRow][columnIndex] = newValue
		return True

	def write_to_csv(self, writeAsBackup=True):
		'''

		RETURNS:
					<bool>	Success of operation
		'''		
		# Check if Write is Necessary
		if not self.hasChanged:
			return False
		# Copy File to Backup
		if writeAsBackup:
			backupFile = self.csvFileName[:-4] + '_bkup.csv'
			if not isfile(backupFile):
				copy2(self.csvFileName, backupFile)
		# Write New Content to Temp File
		tempFile = self.csvFileName[:-4] + '_temp.csv'
		with open(tempFile, 'wb') as csvFile:
			csvWriter = UnicodeCSV.UnicodeWriter(csvFile)
			if self.hasHeader:
				csvWriter.writerows(self.csvHeader)
			csvWriter.writerows(self.fileContent)
		# Copy File to Main
		copy2(tempFile,self.csvFileName)
		remove(tempFile)
		return True

###### TEST BELOW

def test_editable():
	# Read Test CSV
	testCSV = lib_Qndl.CSVRepository + 'testCSV.csv'
	handle = EMF_CSV_Handle(testCSV, hasHeader=False)
	row = handle.next()
	assert row[0] == 'One'
	# Write To Test CSV
	assert handle.change_current_row('Ein', columnIndex=0) #return success
	assert handle.fileContent[0][0] == 'Ein'
	handle.write_to_csv(writeAsBackup=True)
	# Read Backup
	testCSV_bkup = lib_Qndl.CSVRepository + 'testCSV_bkup.csv'
	handle = EMF_CSV_Handle(testCSV_bkup, hasHeader=False)
	row = handle.next()
	assert row[0] == 'Ein'
	# Delete Backup
	remove(testCSV_bkup)


def test_nonEditable():
	# Read Test CSV
	testCSV = lib_Qndl.CSVRepository + 'testCSV.csv'
	handle = EMF_CSV_Handle(testCSV, hasHeader=False, editableColumns=[])
	count = 0
	for row in handle:	
		count += 1
		print row
	assert count == 2
	try:
		row = handle.next()
		assert False
	except StopIteration:
		pass
def main():
	test_nonEditable()
	test_editable()

if __name__ == '__main__':
	import lib_QuandlAPI as lib_Qndl
	from os import remove
	main()