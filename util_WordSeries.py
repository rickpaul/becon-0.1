# TODO:
#	Can we make prd. only have data, without transformation?

import lib_Transformation 	as lib_Trns

def generate_Word_Series_name(hndl_Data, hndl_Trns):
	return str(hndl_Data) + ":" + str(hndl_Trns)

def generate_Word_Series_generic_desc(hndl_Data, hndl_Trns):
	fn = lib_Trns.TransformationDescs[hndl_Trns.name][0]
	return fn(hndl_Trns.parameters, hndl_Data.ticker)

def generate_Word_Series_categorical_desc(hndl_Data, hndl_Trns):
	return '{0} in {1}'.format(hndl_Data.category_meaning, hndl_Data.subcategory) 
	

def raw_word_key(hndl_Word):
	return 'raw.' + hndl_Word.data_ticker

def prd_word_key(hndl_Word):
	return 'prd.' + str(hndl_Word)

def word_key(hndl_Word):
	return str(hndl_Word)
