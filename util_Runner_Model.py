

import numpy as np
from sklearn.metrics import precision_recall_fscore_support as pr
from math import floor

more_than_three = lambda x: abs(x)>=3.0
more_than_two = lambda x: abs(x)>=2.0
more_than_one = lambda x: abs(x)>=1.0


kwargDefaults = {
	'splitLength': 36,
	'numSplits': 10
}

def split_time_series(data, kwargs={}, backwards=True):
	'''
	RETURNS:
				Array of split data
	'''
	key = 'splitLength'
	splitLength = kwargs.get(key, kwargDefaults[key])
	out = []
	if backwards:
		for i in xrange(len(data), 0, -splitLength):
			out.append(data[max(i-splitLength, 0):i])
		out.reverse()
		return out
	else:
		len_ = len(data)
		for i in xrange(0, len_, splitLength):
			out.append(data[i:min(i+splitLength, len_)])
		return out

# def split_time_series(data, kwargs):
# 	'''
# 	uses least squares to find optimal splits
# 	RETURNS:
# 				Array of split data
# 	'''
# 	raise NotImplementedError
# 	for i in range(1,self.dataLength-1):
# 			splitVar = np.std(regressorData[0:i])+np.std(regressorData[i:dataLength])

def level_outlier_proportion(raw_data, predicted_data, check_fn=more_than_three):
	assert len(raw_data) == len(predicted_data)
	raw_arrays = split_time_series(raw_data)
	pred_arrays = split_time_series(predicted_data)
	count_ = 0
	len_ = 0
	for (raw_array, pred_array) in zip(raw_arrays, pred_arrays):
		sublen_ = len(raw_array)
		if sublen_ >= 12:
			mean = np.mean(raw_array)
			std = np.std(raw_array)
			normDist = lambda x: (x-mean)/std
			count_ += sum(map(check_fn, map(normDist, pred_array)))
			len_ += sublen_
	return count_*1.0/len_


def change_outlier_proportion(raw_data, predicted_data, check_fn=more_than_three):
	assert len(raw_data) == len(predicted_data)
	raw_arrays = split_time_series(np.ediff1d(raw_data))
	pred_arrays = split_time_series(np.ediff1d(predicted_data))
	count_ = 0
	len_ = 0
	for (raw_array, pred_array) in zip(raw_arrays, pred_arrays):
		sublen_ = len(raw_array)
		if sublen_ >= 12:
			mean = np.mean(raw_array)
			std = np.std(raw_array)
			normDist = lambda x: (x-mean)/std
			count_ += sum(map(check_fn, map(normDist, pred_array)))
			len_ += sublen_
	return count_*1.0/len_

# def count_outliers(data, mean, std, df):
# 	if df>30:
# 	else:
# 	map(dist)
