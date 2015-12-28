# EMF 		From...Import
from 	handle_QuandlAPI 	import EMF_QuandlAPI_Handle
# System 	Import...As
import	numpy	as 	np

def main():
	handle = EMF_QuandlAPI_Handle('WIKI','FB')
	(dates, values) = handle.get_data(columnName='Open')
	handle.set_extra_parameter('column_index', 1)
	(dates2, values2) = handle.get_data()
	assert np.all(dates==dates2)
	assert np.all(values==values2)
	print np.vstack((dates, values))

if __name__ == '__main__':
	main()