from sklearn.cluster import KMeans
import numpy as np
import math
from .GetAnalyticsData import getAnalyticsData
from .GetSurveyFields import getSurveyFields

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
	index = 0
	for field in fields:
		indices[field.value] = index
		values[index] = field.value
		index += 1
	
	
	print('{} {} {}'.format(str(lastInterval), str(midInterval), str(firstInterval)))
	surveyResults = getAnalyticsData(survey)
	
	#so hacky, but a better way to do this eludes me, so this is how it is.
	total = 0
	for participant in surveyResults:
		total += len(surveyResults[participant])
	responseMatrix = np.empty([total,2], dtype=int)
	idx = 0
	for participant in surveyResults:
		for response in surveyResults[participant]:
			responseMatrix[idx] = [response.orderPosition, indices[response.surveyFieldID.value]]
			idx += 1
			print('[{},{}]'.format(str(response.orderPosition), str(indices[response.surveyFieldID.value])))
	
	kmeans = KMeans(n_clusters=2, random_state=0).fit(responseMatrix)
	
	#calculate total reponse weight for each question
	weights = {}
	for participant in surveyResults:
		for response in surveyResults[participant]:
			split = response.orderPosition
			if split < firstInterval or split > midInterval:
				score = 3
			else:
				score = 0
			
			if response.surveyFieldID.value in weights:
				weights[response.surveyFieldID.value] += score
			else:
				weights[response.surveyFieldID.value] = score
	return weights
