# TODO:
#	Implement file versioning system for backups (somehow)


import logging as log # Needed?

from shutil import copy2
import csv

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
			csvReader = csv.reader(csvFile)
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
		# Check if Column Index is Editable
		if self.editableColumns is not None:
			if columnIndex not in self.editableColumns:
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
			copy2(self.csvFileName, self.csvFileName[:-4] + '_bkup.csv')
		# Write New Content
		with open(self.csvFileName, 'wb') as csvFile:
			csvWriter = csv.writer(csvFile)
			if self.hasHeader:
				csvWriter.writerows(self.csvHeader)
			csvWriter.writerows(self.fileContent)
			return True

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