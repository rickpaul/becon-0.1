import numpy as np
from scipy import stats
from math import floor

import warnings
warnings.filterwarnings('error')

class SequentialRegressionWindow:
	'''
	Sequential means that the x value is a range
	Basically, x is time.
	This is a way of boiling down a slope and intercept.
	'''	
	def __init__(self, data, window, interceptFrom0=True):
		# Save off data, windowSize
		self.data = data
		self.dataLength = len(data)
		self.windowSize = int(window)
		# Initialize Empty Containers for Slope and Intercept
		self.slopes = np.empty((self.dataLength - self.windowSize,1))
		self.intercepts = np.empty((self.dataLength - self.windowSize,1))
		self.rs = np.empty((self.dataLength - self.windowSize,1))
		self.variances = np.empty((self.dataLength - self.windowSize,1))
		# Determine Constant X Sums for Use In Window Moves 
		x = float(self.windowSize) - 1
		self.sumX = x*(x+1)/2.0
		sumSq = lambda(n):  n**3/3.0 + n**2/2.0 + n/6.0
		self.sumSqX = sumSq(x)
		self.meanX = self.sumX / float(self.windowSize)
		self.xDenominator = self.windowSize*self.sumSqX - self.sumX**2
		self.stdX = np.sqrt(2 * sumSq(self.meanX) / float(self.windowSize)) #can use for rs
		# Determine Initial Y Sums for Use in Window Moves
		self.currentSumY = sum(data[0:self.windowSize])
		self.currentSumSqY = sum([y**2 for y in data[0:self.windowSize]]) #can use for rs
		varY = (self.currentSumSqY / self.windowSize*1.0) - (self.currentSumY / float(self.windowSize))**2 #can use for rs
		## Fill in initial data
		(slope, intercept, r_value, p_value, std_err) = stats.linregress(np.arange(0,window), data[0:window])
		self.currWindowStart = 0
		self.slopes[0] = self.currentSlope = slope
		self.intercepts[0] = self.currentIntercept = intercept
		self.rs[0] = self.currentSlope * self.stdX / np.sqrt(varY)
		self.variances[0] = varY
		self.__findRegressionEquations(interceptFrom0=interceptFrom0)

	def __findRegressionEquations(self, interceptFrom0=True):
		for i in range(int(self.dataLength - self.windowSize - 1)):
			self.__moveWindowOneStep(interceptFrom0=interceptFrom0)

	def __moveWindowOneStep(self, interceptFrom0=True):
		oldY = self.data[self.currWindowStart]
		newY = self.data[self.currWindowStart + self.windowSize]
		deltaSumY = newY - oldY
		deltaSumSqY = newY**2 - oldY**2
		deltaSumXY = (float(self.windowSize)-1)*newY - self.currentSumY + oldY
		newSlope = 	self.currentSlope + \
					(float(self.windowSize)*deltaSumXY - self.sumX*deltaSumY) / self.xDenominator
		self.currentSumY = self.currentSumY + deltaSumY
		self.currentSumSqY = self.currentSumSqY + deltaSumSqY
		varY = (self.currentSumSqY / float(self.windowSize)) - (self.currentSumY / float(self.windowSize))**2 #can use for rs
		self.slopes[self.currWindowStart + 1] = self.currentSlope = newSlope
		intercept = self.currentSumY / float(self.windowSize) - (self.currentSlope * self.meanX)
		if not interceptFrom0:
			intercept += self.currWindowStart * self.currentSlope
		self.intercepts[self.currWindowStart + 1] = intercept
		try:
			self.rs[self.currWindowStart + 1] = self.currentSlope * self.stdX / np.sqrt(varY)
		except RuntimeWarning:
			print varY
		self.variances[self.currWindowStart + 1] = varY
		self.currWindowStart += 1

class NonSequentialRegressionWindow:
	'''
	NonSequential means that the x value is filled (it's not a range of values over time)
	'''
	def __init__(self, dataX, dataY, window):
		# Save off dataX, dataY, windowSize
		self.dataX = dataX
		self.dataY = dataY
		self.dataLength = len(dataX)
		if len(dataY) != self.dataLength:
			raise Exception('data sizes not consistent')
		self.windowSize = int(window)
		# Initialize Empty Containers for Slope and Intercept
		self.slopes = np.empty((self.dataLength - self.windowSize,1))
		self.intercepts = np.empty((self.dataLength - self.windowSize,1))
		## Determine Initial Sums for Use in Window Moves
		self.currentSumX = sum(dataX[0:self.windowSize])
		self.currentSumY = sum(dataY[0:self.windowSize])
		currentSumSqX = sum([a**2 for a in dataX[0:self.windowSize]])
		self.currentDen = self.windowSize*currentSumSqX - self.currentSumX**2
		## Fill in Initial Data
		(slope, intercept, r_value, p_value, std_err) = stats.linregress(dataX[0:window], dataY[0:window])
		self.currWindowStart = 0
		self.slopes[0] = self.currentSlope = slope
		self.intercepts[0] = intercept
		self.__findRegressionEquations()

	def __findRegressionEquations(self):
		for i in range(int(self.dataLength - self.windowSize - 1)):
			self.__moveWindowOneStep()

	def __moveWindowOneStep(self):
		# Save Helpful Values
		oldY = self.dataY[self.currWindowStart]
		newY = self.dataY[self.currWindowStart + self.windowSize]
		oldX = self.dataX[self.currWindowStart]
		newX = self.dataX[self.currWindowStart + self.windowSize]
		# Determine New Slope
		deltaNum = 	(self.windowSize-1)*(newX*newY-oldX*oldY) - \
					(newY-oldY)*(self.currentSumX-oldX) - \
					(newX-oldX)*(self.currentSumY-oldY)
		deltaDen = 	(self.windowSize-1)*newX**2 - \
					(self.windowSize+1)*oldX**2 + \
					2*self.currentSumX*(oldX-newX) + \
					2*oldX*newX
		newSlope = (self.currentSlope*self.currentDen + deltaNum) / (self.currentDen + deltaDen)
		# Update Saved Values
		self.currentSumX += (newX - oldX)
		self.currentSumY += (newY - oldY)
		# Determine Intecept		
		intercept = self.currentSumY/float(self.windowSize) - (newSlope * self.currentSumX/float(self.windowSize))
		# Save Slope and Intercept
		self.intercepts[self.currWindowStart + 1] = intercept
		self.slopes[self.currWindowStart + 1] = self.currentSlope = newSlope
		# Update Saved Values
		self.currentDen += deltaDen
		self.currWindowStart += 1

class RollingMeanVarianceWindow:
	def __init__(self, data, window):
		# Save off data, windowSize
		self.data = data
		self.dataLength = len(data)
		self.windowSize = int(window)		
		# Initialize Empty Containers for Mean and Variances
		self.means = np.empty((self.dataLength - self.windowSize,1))
		self.variances = np.empty((self.dataLength - self.windowSize,1))
		# Determine Initial Y Sums for Use in Window Moves
		self.currentSumY = sum(data[0:self.windowSize])
		self.currentSumSqY = sum([y**2 for y in data[0:self.windowSize]]) #can use for rs
		varY = (self.currentSumSqY / float(self.windowSize)) - (self.currentSumY / float(self.windowSize))**2
		## Fill in Initial Data
		self.currWindowStart = 0
		self.means[0] = self.currentSumY/float(self.windowSize)
		self.variances[0] = varY
		self.__findStats()

	def __findStats(self):
		for i in range(int(self.dataLength - self.windowSize - 1)):
			self.__moveWindowOneStep()

	def __moveWindowOneStep(self):
		# Save Helpful Values
		oldY = self.data[self.currWindowStart]
		newY = self.data[self.currWindowStart + self.windowSize]
		# Determine Changes		
		self.currentSumY += (newY - oldY)
		self.currentSumSqY += newY**2 - oldY**2
		# Calculate Stats
		varY = (self.currentSumSqY / float(self.windowSize)) - (self.currentSumY / float(self.windowSize))**2
		self.currWindowStart += 1
		self.means[self.currWindowStart] = self.currentSumY/float(self.windowSize)
		self.variances[self.currWindowStart] = varY
