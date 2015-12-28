#TODO: DELETE
#	No Decision Tree Here
import matplotlib.pyplot as plt
import matplotlib.patches as ptchs

import operator as op

from DecisionTreeNode import BranchNode
from DecisionTreeNode import LeafNode

def drawDecisionTree(DT, dataSet):
	if DT is None:
		plt.scatter(dataSet[:,0],dataSet[:,1],c=dataSet[:,2])
		plt.show()
	else:
		sbplt = plt.subplot(111)
		xMin = min(dataSet[:,0])
		xMax = max(dataSet[:,0])
		yMin = min(dataSet[:,1])
		yMax = max(dataSet[:,1])
		plt.xlim(xMin, xMax)
		plt.ylim(yMin, yMax)
		drawDecisionTreeNode(DT, sbplt, xMin, xMax, yMin, yMax)
		plt.scatter(dataSet[:,0],dataSet[:,1],c=dataSet[:,2])
		plt.show()

def drawDecisionTreeNode(DT, subplot, xMin, xMax, yMin, yMax, verbose=True):
	'''
	Recursive drawing of DecisionTree Point for 2D boundary
	'''
	if isinstance(DT, BranchNode):
		if DT.logicalOperator == op.lt:
			index = DT.predictorIndex
			decisionPoint = DT.decisionPoint
			if index == 0: # split on x variable
				drawDecisionTreeNode(DT.trueChildNode, subplot, xMin, decisionPoint, yMin, yMax)
				drawDecisionTreeNode(DT.falseChildNode, subplot, decisionPoint, xMax, yMin, yMax)
			elif index == 1: # split on y variable
				drawDecisionTreeNode(DT.trueChildNode, subplot, xMin, xMax, yMin, decisionPoint)
				drawDecisionTreeNode(DT.falseChildNode, subplot, xMin, xMax, decisionPoint, yMax)
			else:
				raise Exception('Drawing only works on two-dimensional plots')
		elif DT.logicalOperator == op.gt:
			index = DT.predictorIndex
			decisionPoint = DT.decisionPoint			
			if index == 0: # split on x variable
				drawDecisionTreeNode(DT.trueChildNode, subplot, decisionPoint, xMax, yMin, yMax)
				drawDecisionTreeNode(DT.falseChildNode, subplot, xMin, decisionPoint, yMin, yMax)
			elif index == 1: # split on y variable
				drawDecisionTreeNode(DT.trueChildNode, subplot, xMin, xMax, decisionPoint, yMax)
				drawDecisionTreeNode(DT.falseChildNode, subplot, xMin, xMax, yMin, decisionPoint)
			else:
				raise Exception('Drawing only works on two-dimensional plots')
		elif logicalOperator == op.eq:
			# TODO: Implement
			raise NotImplementedError('Drawing not available for categorical variables')
		else:
			raise NameError('Logical Operator not recognized')
	elif isinstance(DT, LeafNode):
		if DT.value:
			color = '#727f3f'
		else:
			color = '#3f597f'
		subplot.add_patch(ptchs.Rectangle((xMin,yMin), xMax-xMin, yMax-yMin, alpha=0.75*DT.purityProportion, facecolor=color))
		if verbose and DT.value:
			print 'true  at [{0:.3f} to {1:.3f},{2:.3f} to {3:.3f}] {4:.2f}'.format(xMin, xMax, yMin, yMax, DT.purityProportion)
		if verbose and not DT.value:
			print 'false at [{0:.3f} to {1:.3f},{2:.3f} to {3:.3f}] {4:.2f}'.format(xMin, xMax, yMin, yMax, DT.purityProportion)		
	else:
		raise NameError('Tree Type not recognized')
