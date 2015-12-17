

sampleModes = {
	'pasting' #full features, random data samples without replacement
	'bagging' #full features, random data samples with replacement
	'randomSubspaces' #random features, full data samples
	'randomPatches' #random features, random data samples without replacement
}


class EMF_Sampler_Handle:
	def __init__(self):
		raise NotImplementedError

	def assignColumnFeatures(self):
		'''
		
		'''
		raise NotImplementedError


	def assignRowSampleIDs(self):
		raise NotImplementedError

	def createSample(self, mode='randomPatches')