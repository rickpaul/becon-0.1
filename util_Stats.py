# EMF       Import...As
from    lib_DBInstructions      import retrieveStats_DataStatsTable, retrieveStats_WordStatsTable
from    lib_DBInstructions      import replaceStats_DataStatsTable, replaceStats_WordStatsTable
# System    Import...As
import  random
# System    From...Import
from    scipy.stats             import moment
from 	collections 			import Counter

################################ INFORMATION THEORY: CONTINUOUS



################################ INFORMATION THEORY: DISCRETE
def information_gain(data):
	len_ = len(data)
	informationGain = 0
	dct = dict(Counter(data).most_common())
	for num in dct.values():
		freq = (float(num)/len_)
		informationGain -= freq*log(freq,2)
	return informationGain

def gini_coefficient(data):
	len_ = len(data)
	giniImpurity = 1
	dct = dict(Counter(data).most_common())
	for num in dct.values():
		giniImpurity -= (float(num)/len_)**2
	return giniImpurity

################################ ONE-DIMENSIONAL STATISTICAL MOMENTS
def moments(array):
	moment_ = lambda x: moment(array, x)
	return map(moment_, xrange(1,5))

################################ ONE-DIMENSIONAL STATISTICAL MOMENT COMBINATION
def combined_mean(mean_y, len_y, mean_x, len_x):
	combined_len = len_y + len_x
	return (len_y*mean_y + len_x*mean_x)/combined_len

def combined_variance(mean_y, var_y, len_y, mean_x, var_x, len_x):
	'''
	var(x) = E(X^2) - (E(X))^2
	'''
	combined_len_ = len_y + len_x
	combined_mean_ = combined_mean(mean_y, len_y, mean_x, len_x)
	combined_var_ = (len_y*(var_y+mean_y**2) + len_x*(var_x+mean_x**2))/combined_len_ - combined_mean_**2
	return (combined_mean_, combined_var_, combined_len_)


COMBINE_VAR = lambda (mean_y, var_y, len_y), (mean_x, var_x, len_x): \
				combined_variance(mean_y, var_y, len_y, mean_x, var_x, len_x)

################################ STATISTICAL DATABASE TABLE HELPER
def simplify_data_stats_db(conn, cursor, respID, predID):
	results = retrieveStats_DataStatsTable(cursor, respID, predID)
	if results is not None and len(results) > 1:
		(mean_, var_, len_) = reduce(COMBINE_VAR, results)
		replaceStats_DataStatsTable(conn, cursor, 
									respID, predID, 
									mean_, var_, len_)

def simplify_word_stats_db(conn, cursor, respID, predID):
	results = retrieveStats_WordStatsTable(cursor, respID, predID)
	if results is not None and len(results) > 1:
		(mean_, var_, len_) = reduce(COMBINE_VAR, results)
		replaceStats_WordStatsTable(conn, cursor, 
									respID, predID, 
									mean_, var_, len_)

################################ WEIGHTED RANDOM CHOICE 
def weighted_choice(choices_iter, total):
	'''
	modified from
	http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
	'''
	r = random.uniform(0, total)
	upto = 0
	for c, w in choices_iter:
		if upto + w >= r:
			return c
		upto += w
	assert False, "Shouldn't get here"