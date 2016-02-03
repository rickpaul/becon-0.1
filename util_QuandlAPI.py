
import lib_TimeSet



def codify_periodicity(str_):
	if str_=='monthly':
		return lib_TimeSet.MONTHS
	elif str_=='quarterly':
		return lib_TimeSet.QUARTERS
	elif str_=='annnual':
		return lib_TimeSet.YEARS
	elif str_=='weekly':
		return lib_TimeSet.WEEKS
	elif str_=='daily':
		return lib_TimeSet.DAYS
	else:
		raise NameError