# TODO:
#	Implement as iterator
#	Implement writing as backup
#		Implement file versioning system (somehow)


import logging as log # Needed?

import csv
# from os.path 	import isfile # Deprecated
# from os 		import rename # Deprecated

class EMF_CSV_Handle:
	def __init__(self, csvFileName, readOnly=True):
		self.csvFileName = csvFileName
		self.csvHeader = None
		self.originalContent = None


# class EMF_CSV_Handle:
# 	def __init__(self, csvFileName):
# 		self.csvFileName = csvFileName
# 		self.csvHeader = None
# 		self.originalContent = None
# 		self.changedContent = None
# 		self.hasChanged = False
# 		self.readRow = None

# 	def readFromCSV(self):
# 		with open(self.csvFileName, 'rU') as csvFile:
# 			csvReader = csv.reader(csvFile)
# 			self.csvHeader = [next(csvReader)] # Save off header in CSV
# 			self.originalContent = [list(row) for row in csvReader]
# 			self.readRow = 0
# 			self.contentLength = len(self.originalContent)

# 	def __iter__(self):
# 		return self

# 	def next(self):
# 		if self.
# 		if self.readRow > self.contentLength:
# 			raise StopIteration
# 		else:
# 			self.readRow += 1
# 			return self.originalContent[self.readRow-1]

# 	def writeToCSV(self, writeList, writeAsBackup=True):
# 		with open(self.csvFileName, 'wb') as csvFile:
# 			csvWriter = csv.writer(csvFile)
# 			csvWriter.writerows(self.csvHeader)
# 			csvWriter.writerows(writeList)
