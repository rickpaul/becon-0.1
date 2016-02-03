import lib_Transformation 	as lib_Trns

def generate_Word_Series_name(dataHandle, trnsHandle):
	return str(dataHandle) + ":" + str(trnsHandle)

def generate_Word_Series_generic_desc(dataHandle, trnsHandle):
	fn = lib_Trns.TransformationDescs[trnsHandle.name][0]
	return fn(trnsHandle.parameters, dataHandle.ticker)

def generate_Word_Series_categorical_desc(dataHandle, trnsHandle):
	return '{0} in {1}'.format(dataHandle.category_meaning, dataHandle.subcategory) 
