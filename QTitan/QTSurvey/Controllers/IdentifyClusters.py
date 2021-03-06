from sklearn.cluster import KMeans
from ..models import *
import numpy as np
import math
import random
import copy
import sys
from .GetAnalyticsData import getAnalyticsData
from .GetSurveyFields import getSurveyFields


############# RelationGraph class ###########
class RelationGraph:
	def __init__(self, interval, surveyResults, numOptions):
		self.surveyResults = surveyResults
		self.interval = interval
		self.posInterval = self.interval
		self.negInterval = numOptions - self.interval
		self.numOptions = numOptions
		self.DEBUG = False
		self.Strongest_Connected_Node = None
		self.Strongest_Connection_val = -1
		self.clusters = []

		if self.DEBUG: print("Options start at: {}, there are {} options, options end at: {}".format(interval, numOptions, numOptions))

		#generate a node for each participant and their results
		self.Nodes = []
		for participant in surveyResults:
			self.Nodes.append(Node(participant, surveyResults[participant]))

		#analyze each node for relationships
		for node in self.Nodes:
			self.Connect(node)

		# if there weren't any node to connect to, set us to the only node
		if self.Strongest_Connected_Node is None:
			self.Strongest_Connected_Node = self.Nodes[0]
			self.Strongest_Connection_val = 0

		if self.DEBUG:
			self.printNodes()
	
	def printNodes(self):
		for node in self.Nodes:
			sys.stdout.write("{} connected to: [".format(node.participant.username))
			for c in node.connections:
				sys.stdout.write("{}: {}, ".format(c.participant.username, node.connections[c]))
			print("]")
			for otherNode in node.sameresponses:
				sys.stdout.write("{} and {} have same responses: [".format(node, otherNode))
				for response in node.sameresponses[otherNode]:
					sys.stdout.write("{}, ".format(response))
				print("]")

	#Connect the node to the graph. The more strongly a node agrees on a response, the stronger the connection.
	# The sum of these agreements determines the overall connection of the node.
	# Therefore, nodes which have more important questions in common will be more strongly connected.
	def Connect(self, node):
		#for all of this node's responses
		for response in node.responses:
			# connect to the other nodes in this graph
			for otherNode in self.Nodes:
				if node == otherNode:
					continue
				
				relativeWeight, sameResponses = self.getRelativeWeight(self.interval, self.numOptions, node, otherNode)
				node.addConnection(otherNode, relativeWeight, sameResponses)
				otherNode.addConnection(node, relativeWeight, sameResponses)

				if relativeWeight > self.Strongest_Connection_val:
					self.Strongest_Connection_val = relativeWeight
					self.Strongest_Connected_Node = node
	
	#Identify the score of a any response at the given position
	def getScore(self, pos):
		ret = 0
		if pos < self.posInterval:
			ret = 1
		elif pos >= self.posInterval and pos <= self.negInterval:
			ret = 0
		elif pos > self.negInterval:
			ret = -1
		return ret
	

	#create and return a dictionary containing the total consensus, a sum of the scores for this question of all participants/nodes
	def getTotalConsensus(self):
		posWeights = {}
		negWeights = {}
		ntlWeights = {}
		responses = []
		for node in self.Nodes:
			for response in node.responses:
				if response.surveyFieldID.value not in responses:
					responses.append(response.surveyFieldID.value)

				score = self.getScore(node.getRelativePosition(response.orderPosition))
				if score > 0:
					weights = posWeights
				elif score == 0:
					weights = ntlWeights
				else:
					weights = negWeights

				if response.surveyFieldID.value in weights:
					weights[response.surveyFieldID.value] += 1
				else:
					weights[response.surveyFieldID.value] = 1

		return Consensus(posWeights, negWeights, ntlWeights, responses)

	def getRelativeWeight(self, interval, numOptions, n1, n2):
		posInterval = interval
		negInterval = numOptions - interval
		total = 0
		sameresponses = []
		for response in n1.responses:
			# exit early if the response isn't significant
			orderPos = n1.getRelativePosition(response.orderPosition)

			if orderPos > posInterval and orderPos <= negInterval:
				continue

			# find the same response value in n2
			n2pos = -1
			response2 = None
			for r2 in n2.responses:
				if response.surveyFieldID.value == r2.surveyFieldID.value:
					n2pos = n2.getRelativePosition(r2.orderPosition)
					response2 = r2
					break
			
			#break early if n2's response position isn't significant
			if n2pos > posInterval and n2pos <= negInterval:
				continue

			#add to the total if the responses are within interval - 1 of each other
			if abs(orderPos - n2pos) < interval:
				if self.DEBUG: print("n1: {}, n2: {}, r: {}, o1: {}, o2: {}, sub: {}, i: {}".format(n1, n2, response.surveyFieldID.value, orderPos, n2pos, abs(orderPos - n2pos), interval))
				sameresponses.append(response.surveyFieldID.value)
				total += 1
			#else: #otherwise, they are opposing viewpoints, so the relative weight loses one
				#total -= 1
		
		return total, sameresponses

	def getClusters(self):
		#Starting with the strongest connected node, create a cluster
		c = Cluster(self, 0, self.Strongest_Connection_val, self.Strongest_Connected_Node)
		self.clusters.append(c)
		if self.DEBUG: print("Adding first cluster {} to clusters".format(c))

		pool = []
		for node in self.Nodes:
			pool.append(node)

		if self.DEBUG: 
			sys.stdout.write("Pool contains: ")
			for node in pool:
				sys.stdout.write("{}, ".format(node))
			print("")
		
		numClusters = 0
		node = self.Strongest_Connected_Node
		while pool:
			#add this node's strongest connected otherNode to this node's cluster
			#find the strongest connected node
			maxNode = None
			maxCon = -1
			for otherNode in node.connections:
				if node.connections[otherNode] > maxCon:
					maxNode = otherNode
					maxCon = node.connections[otherNode]

			# if this node doesn't have a cluster, check the maxNode
				#if the maxNode doesn't have a cluster, then create a new cluster for the pair
				#if the maxNode does have a cluster, add this node to it
			# if the node does have a cluster, add the maxnode to it
			if node.cluster is None:
				if maxNode.cluster is None:
					numClusters += 1
					if self.DEBUG: print("Creating new cluster {}, maxCon: {}, initialNode: {}".format(numClusters, maxCon, node))
					c = Cluster(self, numClusters, maxCon, node)
					c.addNode(maxNode)
					if self.DEBUG: print("Created new cluster: {}".format(c))
					self.clusters.append(c)
				else:
					maxNode.cluster.addNode(node)
			else:
				node.cluster.addNode(maxNode)
			
			pool.remove(node)
			if maxNode in pool:
				pool.remove(maxNode)
			if pool:
				if self.DEBUG: print("Getting next node")
				node = random.choice(pool) #increment the node to another one that hasn't been assigned yet

		if self.DEBUG: 
			print("Pool empty. number of clusters in list: {}".format(len(self.clusters)))
			for cluster in self.clusters:
				print(cluster)

		return self.clusters
		

########## Node Class ##########################
class Node:
	def __init__(self, participant, responses):
		self.connections = {}
		self.responses = responses
		self.participant = participant
		self.cluster = None
		self.sameresponses = {}
		self.baseDemographic = BaseDemographic.objects.get(userID = participant.id)
		
		self.minOrder = sys.maxsize
		for response in responses:
			if response.orderPosition < self.minOrder:
				self.minOrder = response.orderPosition
	
	def __str__(self):
		return self.participant.username

	#Adds a connection between this node and the incoming node.
	def addConnection(self, node, magnitude, sameresponses):
		if node in self.connections:
			if self.connections[node] != magnitude:
				print("Same connection has differing magnitude?")
			return
		else:
			self.connections[node] = magnitude
			self.sameresponses[node] = sameresponses
	
	def getRelativePosition(self, pos):
		return pos - self.minOrder + 1

	def getConnectionRange(self):
		maxCon = max(self.connections.values())
		minCon = min(self.connections.values())
		return minCon, maxCon

#################### Cluster Class #############################
class Cluster:
	def __init__(self, graph, identifier, initialWeight, initialNode):
		self.identifier = identifier
		self.Nodes = []
		self.Nodes.append(initialNode)
		self.startWeight = initialWeight
		self.name = "Cluster " + str(self.identifier)
		initialNode.cluster = self

	def __str__(self):
		return self.name

	def addNode(self, node):
		if node is None:
			return False
		if not node in self.Nodes:
			self.Nodes.append(node)
			if node.cluster is not None:
				print("Error, node has been assigned to more than one cluster")
			node.cluster = self
			return True
		else:
			return False

	def consensus(self, g):
		posWeights = {}
		negWeights = {}
		ntlWeights = {}
		responses = []

		for node in self.Nodes:
			for response in node.responses:
				if response.surveyFieldID.value not in responses:
					responses.append(response.surveyFieldID.value)
				
				score = g.getScore(node.getRelativePosition(response.orderPosition))
				if score > 0:
					weights = posWeights
				elif score == 0:
					weights = ntlWeights
				else:
					weights = negWeights

				if response.surveyFieldID.value in weights:
					weights[response.surveyFieldID.value] += 1
				else:
					weights[response.surveyFieldID.value] = 1
		
		self.weights = Consensus(posWeights, negWeights, ntlWeights, responses)

############################ Consensus Class #############################################
class Consensus:
	def __init__(self, posWeights, negWeights, ntlWeights, names):
		self.DEBUG = False
		self.posWeights = posWeights
		self.negWeights = negWeights
		self.ntlWeights = ntlWeights
		self.names = names

		for response in self.names:
			if response not in self.posWeights:
				self.posWeights[response] = 0
			if response not in self.negWeights:
				self.negWeights[response] = 0
			if response not in self.ntlWeights:
				self.ntlWeights[response] = 0





########## Other functions #############
def identifyClusters(survey):
	surveyResults = getAnalyticsData(survey)
	fields = getSurveyFields(survey)
	numOptions = len(fields)

	if len(surveyResults.values()) == 0:
		return None, None

	if numOptions < 4:
		interval = 1
	elif numOptions < 9:
		interval = 2
	else:
		interval = 3

	graph = RelationGraph(interval, surveyResults, numOptions)
	clusters = graph.getClusters()

	if clusters is not None:
		for c in clusters:
			c.consensus(graph)

	return graph, clusters

