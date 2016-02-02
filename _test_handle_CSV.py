
# EMF 		From...Import
from 	handle_CSV 			import EMF_CSV_Handle
# EMF 		Import...As
import 	lib_QuandlAPI 		as lib_Qndl
# System 	From...Import
from 	os 					import remove
from 	shutil 				import copy2

def test_editable():
	testCSV = lib_Qndl.CSVRepository + 'testCSV.csv'
	testCSV_bkup = lib_Qndl.CSVRepository + 'testCSV_bkup.csv'
	# Read Test CSV
	handle = EMF_CSV_Handle(testCSV, hasHeader=False)
	row = handle.next()
	assert row[0] == 'One'
	# Write To Test CSV
	assert handle.change_current_row('Ein', columnIndex=0) #return success
	assert handle.fileContent[0][0] == 'Ein'
	handle.write_to_csv(writeBackup=True)
	# Read Backup
	handle = EMF_CSV_Handle(testCSV_bkup, hasHeader=False)
	row = handle.next()
	assert row[0] == 'One'
	# Read Changed
	handle = EMF_CSV_Handle(testCSV, hasHeader=False)
	row = handle.next()
	assert row[0] == 'Ein'
	# Delete Backup, Reset Main
	copy2(testCSV_bkup, testCSV)
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
	main()



