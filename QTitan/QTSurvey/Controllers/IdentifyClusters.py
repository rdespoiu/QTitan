from sklearn.cluster import KMeans
import numpy as np
import math
import random
import copy
import sys
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
	
	def printNodes(self):
		for node in self.Nodes:
			sys.stdout.write("{} connected to: [".format(node.participant.username))
			for c in node.connections:
				sys.stdout.write("{}: {}, ".format(c.participant.username, node.connections[c]))
			print("]")

	#Connect the node to the graph. The more strongly a node agrees on a response, the stronger the connection.
	# The sum of these agreements determines the overall connection of the node.
	# Therefore, nodes which have more important questions in common will be more strongly connected.
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
	
	#Identify the score of a any response at the given position
	def getScore(self, pos):
		ret = 0
		if pos <= self.lowerInterval:
			ret = 3
		elif pos > self.lowerInterval and pos <= self.midInterval:
			ret = 0
		elif pos > self.midInterval:
			ret = -3
		return ret
	
	#create and return a dictionary containing the total consensus, a sum of the scores for this question of all participants/nodes
	def getTotalConsensus(self):
		weights = {}
		for node in self.Nodes:
			for response in node.responses:
				if response.surveyFieldID.value in weights:
					weights[response.surveyFieldID.value] += self.getScore(response.orderPosition)
				else:
					weights[response.surveyFieldID.value] = self.getScore(response.orderPosition)
		return weights
	
	def getClusters(self):
		self.clusters = []
		maxScore = self.getScore(0) # the score of the first option will always be the highest

		#identify the range of minimum and maximum connection weights for a random node.
		rn = random.choice(self.Nodes)
		minCon, maxCon = rn.getConnectionRange()
		
		#Add each of the nodes in the graph to a cluster, creating clusters as appropriate
		currentWeight = maxCon
		clusteredNodes = []
		cnum = 0
		pool = []
		for n in self.Nodes:
			pool.append(n)
		
		### DEBUG
			
		
		node = rn # start with the random node from above
		while pool:
			#If we have tried all the possible weights for this node
			if currentWeight < minCon:
				print("Iterating node")
				node = random.choice(pool) # pick a random new node from those remaining
				currentWeight = maxCon # reset the weight we are looking for

			if currentWeight in node.connections.values():
				c = Cluster(cnum, currentWeight, node)
				cnum += 1
				print(c)
				maxWeight = currentWeight + maxScore
				minWeight = currentWeight - maxScore
				
				# for each connected node
				for n in node.connections:
					#attach the node to the cluster if the connection strength is within the range of currentweight give or take the max score for a single option
					# that is, attach the node to the cluster if the node agrees to the strength of this cluster, give or take a response
					if n in pool:
						self.assignToCluster(maxWeight, minWeight, pool, c, n, node)
					
				#add the created cluster to the list
				self.clusters.append(c)

			# if we didn't find a connection in this node at the current weight
			print("iterating weight")
			currentWeight -= (maxScore * 2) # decrement the weight we are looking for by 2 questions
			
			
		return self.clusters
			
	#recursively add this 'node' to 'cluster' if the connection between it and its 'parent' is between maxWeight and minWeight, inclusive
	# because it is recursive, it'll also add similar relationships this node has with other nodes it is connected to.
	def assignToCluster(self, maxWeight, minWeight, pool, cluster, node, parent):
		if parent != node and parent.connections[node] >= minWeight and parent.connections[node] <= maxWeight:
			print("adding node {}, {} to cluster {}".format(node.participant.username, node, cluster))
			if node in pool:
				print("node in pool!")
			else:
				print("Node not in pool?")

			added = cluster.addNode(node)
			#if node in pool:
			pool.remove(node)
			
			if added:
				for n in node.connections:
					if n in pool:
						self.assignToCluster(maxWeight, minWeight, pool, cluster, n, node)
		

########## Node Class ##########################
class Node:
	def __init__(self, participant, responses):
		self.connections = {}
		self.responses = responses
		self.participant = participant

	#Adds a connection between this node and the incoming node.
	def addConnection(self, node, magnitude):
		key = node
		if key in self.connections:
			self.connections[key] += magnitude
		else:
			self.connections[key] = magnitude

	def getConnectionRange(self):
		maxCon = max(self.connections.values())
		minCon = min(self.connections.values())
		return minCon, maxCon

class Cluster:
	def __init__(self, identifier, initialWeight, initialNode):
		self.identifier = identifier
		self.Nodes = []
		self.Nodes.append(initialNode)
		self.startWeight = initialWeight

	def __str__(self):
		return "Cluster" + str(self.identifier)

	def addNode(self, node):
		if not node in self.Nodes:
			self.Nodes.append(node)
			return True
		else:
			return False

	def consensus(self, g):
		self.weights = {}
		for node in self.Nodes:
			for response in node.responses:
				if response.surveyFieldID.value in self.weights:
					self.weights[response.surveyFieldID.value] += g.getScore(response.orderPosition)
				else:
					self.weights[response.surveyFieldID.value] = g.getScore(response.orderPosition)

		  





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
	surveyResults = getAnalyticsData(survey)
	fields = getSurveyFields(survey)
	numOptions = len(fields)
	
	graph = RelationGraph(surveyResults, numOptions)
	clusters = graph.getClusters()

	for c in clusters:
		c.consensus(graph)

	return graph, clusters

def identifyClustersOld(survey):
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
