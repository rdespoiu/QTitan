from sklearn.cluster import KMeans
import numpy as np
import math
from .GetAnalyticsData import getAnalyticsData
from .GetSurveyFields import getSurveyFields


############# RelationGraph class ###########
class RelationGraph:
	def __init__(self, surveyResults, numOptions):
		self.surveyResults = surveyResults
		self.lowerInterval = 3
		self.midInterval = numOptions - 3

		#generate a node for each participant and their results
		self.Nodes = []
		for participant in surveyResults:
			self.Nodes.append(Node(participant, surveyResults[participant]))

		#analyze each node for relationships
		for node in self.Nodes:
			self.Connect(node)
	
	def Connect(self, node):
		#for all of this node's responses
		for response in node.responses:
			score = self.getScore(response.orderPosition)
			# connect to the other nodes in this graph
			for otherNode in self.Nodes:
				if node == otherNode:
					continue
				
				#find the score for this response option in the other node
				for otherResponse in otherNode.responses:
					if otherResponse.surveyFieldID.value == response.surveyFieldID.value:
						otherScore = self.getScore(otherResponse.orderPosition)
						break
				
				#if the intervals are the same
				if score == otherScore:
					node.addConnection(otherNode, score)
					otherNode.addConnection(node, score)
	
	def getScore(self, pos):
		ret = 0
		if pos <= self.lowerInterval:
			ret = 3
		elif pos > self.lowerInterval and pos <= self.midInterval:
			ret = 0
		elif pos > self.midInterval:
			ret = -3
		return ret

########## Node Class ##########################
class Node:
	def __init__(self, participant, responses):
		self.connections = {}
		self.responses = responses
		self.participant = participant

	#Adds a connection between this node and the incoming node.
	def addConnection(self, node, magnitude):
		key = node.participant.username
		if key in self.connections:
			self.connections[key] += magnitude
		else:
			self.connections[key] = magnitude



########## Other functions #############
def getOptionScore(survey, pos):
	fields = getSurveyFields(survey)
	numOptions = len(fields)
	careSize = math.floor(numOptions / 10) + 1
	careSize = careSize * 3
	lastInterval = numOptions
	midInterval = lastInterval - careSize
	firstInterval = careSize
	
	if pos <= firstInterval or pos > midInterval:
		score = 3
	else:
		score = 0
	return score

def identifyClusters(survey):
	fields = getSurveyFields(survey)
	numOptions = len(fields)
	careSize = math.floor(numOptions / 10) + 1
	careSize = careSize * 3
	lastInterval = numOptions
	midInterval = lastInterval - careSize
	firstInterval = careSize

	indices = {}
	values = {}
	index = 1
	for field in fields:
		indices[field.value] = index
		values[index] = field.value
		index += 1
	
	
	print('{} {} {}'.format(str(lastInterval), str(midInterval), str(firstInterval)))
	surveyResults = getAnalyticsData(survey)
	
	#so hacky, but a better way to do this eludes me, so this is how it is.
	total = 0
	index = 1
	pindices = {}
	for participant in surveyResults:
		total += len(surveyResults[participant])
		pindices[participant.username] = index
		index+=1
	ptotal = len(surveyResults)
	'''
	numentries = (numOptions - (numOptions - 6)) * ptotal
	responseMatrix = np.zeros([numentries+1,3], dtype=int)
	idx = 0
	weights = {}
	for participant in surveyResults:
		for response in surveyResults[participant]:
			score = getOptionScore(survey, response.orderPosition)
			if score != 0:
				responseMatrix[idx] = [pindices[participant.username], response.orderPosition, indices[response.surveyFieldID.value]]
			idx += 1
			if response.surveyFieldID.value in weights:
				weights[response.surveyFieldID.value] += score
			else:
				weights[response.surveyFieldID.value] = score
			print('[{},{}]'.format(str(response.orderPosition), str(indices[response.surveyFieldID.value])))
	
	kmeans = KMeans(n_clusters=2, random_state=0).fit(responseMatrix)
	'''
	fields = getSurveyFields(survey)
	numOptions = len(fields)
	G = RelationGraph(surveyResults, numOptions)
	return G
