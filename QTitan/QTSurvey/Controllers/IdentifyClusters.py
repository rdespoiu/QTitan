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
	index = 0
	for field in fields:
		indices[field.value] = index
		index += 1
	
	print('{} {} {}'.format(str(lastInterval), str(midInterval), str(firstInterval)))
	surveyResults = getAnalyticsData(survey)
	responseMatrix = np.empty([2,1], dtype=int)
	for participant in surveyResults:
		for response in surveyResults[participant]:
			responseMatrix = np.insert(responseMatrix, [response.orderPosition, indices[response.surveyFieldID.value]])
			print('[{},{}]'.format(str(response.orderPosition), str(indices[response.surveyFieldID.value])))
	
	responseMatrix
	kmeans = KMeans(n_clusters=2, random_state=0).fit(responseMatrix)
	return responseMatrix
