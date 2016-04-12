
import lib_TimeSet



def codify_periodicity(str_):
	if str_=='monthly':
		return lib_TimeSet.MONTHS
	elif str_=='quarterly':
		return lib_TimeSet.QUARTERS
	elif str_=='annual':
		return lib_TimeSet.YEARS
	elif str_=='weekly':
		return lib_TimeSet.WEEKS
	elif str_=='daily':
		return lib_TimeSet.DAYS
	else:
		raise NameError

def stringify_periodicity(code_):
	if code_==lib_TimeSet.MONTHS:
		return 'monthly'
	elif code_==lib_TimeSet.QUARTERS:
		return 'quarterly'
	elif code_==lib_TimeSet.YEARS:
		return 'annual'
	elif code_==lib_TimeSet.WEEKS:
		return 'weekly'
	elif code_==lib_TimeSet.DAYS:
		return 'daily'
	else:
		raise NameError