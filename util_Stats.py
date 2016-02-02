
# System    Import...As
import  random
# System    From...Import
from    scipy.stats             import moment

def moments(array):
    moment_ = lambda x: moment(array, x)
    return map(moment_, xrange(1,5))

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