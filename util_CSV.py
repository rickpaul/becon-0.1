from string import lower


def boolify(str_):
	str_ = lower(str_)
	if str_=='no' or str_=='false':
		return False
	elif str_=='yes' or str_=='true':
		return True
	else:
		try:
			return int(str_)
		except ValueError:
			pass
	return None