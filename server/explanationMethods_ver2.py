import copy
import csv
import pandas as pd
import numpy as np
import networkx as nx
# from pyvis.network import Network

#An example visualization spec object
histogram = {
	'name': 'Histogram',
	'encoding': [
		{
			'data': 'quantitative',
			'channel': 'length'
		},
		{
			'data': 'quantitative',
			'channel': 'position'
		}
	],
	'mark': 'bar',
	'geometry_type': 'function',
	'coordinate_system': 'cartesian'
}

concrete_data = {
	'nominal': [ 'the type of fruit', 'the color of fruit'],
	'quantitative': [ 'the price of fruit', 'the number of fruit sold', 'the weight of fruit', 'the size of fruit'],
	'temporal': ['year']
}


def importCsv(filename):
	visArr = []
	with open(filename, mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			encoding = []
			nominals = row['nominal'].split(', ')
			quants = row['quantitative'].split(', ')
			temporals = row['temporal'].split(', ')
			if nominals[0] != '':
				for channel in nominals:
					encoding.append({
						'data': 'nominal',
						'channel': channel
						})
			if quants[0] != '':
				for channel in quants:
					encoding.append({
						'data': 'quantitative',
						'channel': channel
						})
			if temporals[0] != '':
				for channel in temporals:
					encoding.append({
						'data': 'temporal',
						'channel': channel
						})

			vis = {
				'name': row['chart type'],
				'encoding': encoding,
				'mark': row['mark'],
				'geometry_type': row['geometry type'],
				'coordinate_system': row['coordinate system']
			}
			visArr.append(vis)
	return visArr

def encodingDistance(encA, encB, dist, match):
	if match.count(-1) <= max(len(encA) - len(encB), 0):
		# if dist < minDist[0]:
		# 	minDist[0] = dist
		return dist, match

	dists = []
	for i in range(len(match)):
		if match[i] >= 0:
			continue;
		for j in range(len(encB)):
			if j not in match:
				newDist = dist
				if encA[i]['data'] != encB[j]['data']:
					newDist += 1
				if encA[i]['channel'] != encB[j]['channel']:
					newDist += 1
				newMatch = copy.deepcopy(match)
				newMatch[i] = j
				d, m = encodingDistance(encA, encB, newDist, newMatch)
				dists.append((d,m))

	minDist = 9999
	minMatch = []
	for pair in dists:
		if pair[0] < minDist:
			minDist = pair[0]
			minMatch = pair[1]

	return minDist, minMatch

def distance(A, B):
	match = [-1] * len(A['encoding'])

	dist, match = encodingDistance(A['encoding'], B['encoding'], 0, match)
	dist += 2 * abs(len(A['encoding']) - len(B['encoding']))

	diff = {}
	diff['encodingA'] = {}
	diff['encodingB'] = []
	diff['match'] = match
	#diff['match'] = match

	for i in range(len(match)):
		if match[i] == -1:
			diff['encodingA'][i] = 'number'
		else:
			encA = A['encoding'][i]
			encB = B['encoding'][match[i]]
			if (encA['data'] != encB['data']):
				diff['encodingA'][i] = 'data'
				if (encA['channel'] != encB['channel']):
					diff['encodingA'][i] = 'dataAndChannel'
			elif (encA['channel'] != encB['channel']):
					diff['encodingA'][i] = 'channel'

	if len(A['encoding']) < len(B['encoding']):
		for i in range(len(B['encoding'])):
			if i not in match:
				diff['encodingB'].append(i)

	if A['mark'] != B['mark']:
		dist += 1
		diff['mark'] = True
	else:
		diff['mark'] = False

	if A['geometry_type'] != B['geometry_type']:
		dist += 1
		diff['geometry_type'] = True
	else:
		diff['geometry_type'] = False

	if A['coordinate_system'] != B['coordinate_system']:
		dist += 1
		diff['coordinate_system'] = True
	else:
		diff['coordinate_system'] = False

	return dist, diff

def getVisFromArr(visArr, visName):
	for vis in visArr:
		if vis['name'] == visName:
			return vis
	return None

#function for sorting in rankVisSimilarity
def getDist(e):
  return e['dist']

def rankVisSimilarity(visArr, visName):
	visA = getVisFromArr(visArr, visName)
	distArr = []

	for vis in visArr:
		if vis['name'] != visName:
			dist, diff = distance(visA, vis)
			distArr.append({
				'name': vis['name'],
				'dist': dist,
				'diff': diff
				})

	distArr.sort(key=getDist)
	return distArr

def createDistanceMatrix(visArr):
	dataArr = []
	for i in range(len(visArr)):
		for j in range(len(visArr)):
			if j > i:
				visA = visArr[i]
				visB = visArr[j]
				dist, diff = distance(visA, visB)
				weight = round(1.0/dist, 1)
				if weight > 0.4:
					dataArr.append([visA['name'], visB['name'], 'Undirected', weight])
				#dataArr.append([1.0/dist, 'Undirected', visB['name'], visA['name']])

	pdf = pd.DataFrame(np.array(dataArr), columns=['source', 'target', 'type', 'weight'])
	return pdf

def createNetworkVis(visArr):
	data = createDistanceMatrix(visArr)
	G = nx.from_pandas_edgelist(data, source='source', target='target', edge_attr='weight')
	net = Network('600px', '800px', notebook=True)
	net.from_nx(G)
	net.show('visNetwork.html')

# convert vis terms into layman's
def convertToColloquial(visObj):
	for enc in visObj['encoding']:
		if enc['data'] == 'nominal':
			enc['data'] = 'a category'
		elif enc['data'] == 'quantitative':
			enc['data'] = 'a number'
		elif enc['data'] == 'temporal':
			enc['data'] = 'time'

def convertToConcrete(visObj):
	ncount = 0
	qcount = 0
	tcount = 0
	for enc in visObj['encoding']:
		if enc['data'] == 'nominal':
			enc['data'] = concrete_data['nominal'][ncount]
			ncount += 1
		elif enc['data'] == 'quantitative':
			enc['data'] = concrete_data['quantitative'][qcount]
			qcount += 1
		elif enc['data'] == 'temporal':
			enc['data'] = concrete_data['temporal'][tcount]
			tcount += 1

def reverseMatch(match):
	reversedMatch = {}
	for i in range(len(match)):
		reversedMatch[match[i]] = i;
	return reversedMatch


# assume match[index of A] = index of B
def sortMatch(match, diff):
	matchTuples = []
	for i in range(len(match)):
		if match[i] == -1:
			matchTuples.append((i, -1, 3))
		else:
			code = 0
			
			if i in diff['encodingA']:
				d = diff['encodingA'][i]
				code += 1
				if d == 'channel':
					code += 1
				elif d == 'dataAndChannel':
					code += 2
			matchTuples.append((i, match[i], code))


	matchTuples.sort(key = lambda l : l[2])
	return matchTuples

def declarative(visA, visArr, concrete):
	visA = copy.deepcopy(visA)
	# coordinate system
	text = 'A %s has ' % visA['name']
	if visA['coordinate_system'] == 'cartesian':
		text += 'a horizontal axis and a vertical axis. '
	elif visA['coordinate_system'] == 'linear':
		text += 'a single straight axis. '
	elif visA['coordinate_system'] == 'polar' or visA['coordinate_system'] == 'circular':
		text += 'a circular shape. '

	# mark & list channels
	text += 'There are %ss, which encodes information through their '  % visA['mark']
	n = len(visA['encoding'])
	if n == 1:
		text += '%s. ' % visA['encoding'][0]['channel']
	else:
		for i in range(n):
			enc = visA['encoding'][i]
			if i != n - 1:
				text += '%s, ' % enc['channel']
			else:
				text += 'and %s. ' % enc['channel']

	if concrete:
		text += "For example, consider a %s that shows information about fruits in a grocery store. " % visA['name']
		convertToConcrete(visA)
	else:
		convertToColloquial(visA)

	# encoding
	for i in range(n):
		enc = visA['encoding'][i]
		if i == 0:
			text += 'The '
		elif i == 1:
			text += 'Then, the '
		elif i >= 2:
			text += 'Next, the '
		text += '%s of the %s represents %s. ' % (enc['channel'], visA['mark'], enc['data'])

	return text


# Explain visA, using visB as prior knowledge
def declarative_compare(visA, visB, visArr, concrete):
	visA = copy.deepcopy(visA)
	visB = copy.deepcopy(visB)
	USELESSDISTANCE, diff = distance(visB, visA)

	text = 'A %s is similar to a %s, with minor differences. ' % (visA['name'], visB['name'])
	
	# coordinate system
	text += 'A %s has ' % visB['name']
	if visB['coordinate_system'] == 'cartesian':
		text += 'a horizontal axis and a vertical axis, '
	elif visB['coordinate_system'] == 'linear':
		text += 'a single straight axis, '
	elif visB['coordinate_system'] == 'polar' or visB['coordinate_system'] == 'circular':
		text += 'a circular shape, '
	if diff['coordinate_system']:
		text += 'whereas '
		if visA['coordinate_system'] == 'cartesian':
			text += 'a %s has a horizontal axis and a vertical axis. ' % visA['name']
		elif visA['coordinate_system'] == 'polar' or visA['coordinate_system'] == 'circular':
			text += 'a %s has a circular shape. ' % visA['name']
		elif visA['coordinate_system'] == 'linear':
			text += 'a %s has a single straight axis. ' % visA['name']
	else:
		text += 'which is the same for %s. ' % (visA['name']);

	# mark
	text += 'A %s shows data with %ss. ' % (visB['name'], visB['mark'])
	if diff['mark']:
		text += 'However, a %s shows data with %ss. ' % (visA['name'], visA['mark'])
	else: 
		text += 'Similarly, a %s has %ss. ' % (visA['name'], visA['mark'])

	# geometry type - only explain when there is difference
	if diff['geometry_type']:
		text += ''

	# encoding
	if concrete:
		text += "For example, consider a %s and a %s that shows information about fruits in a grocery store. " % (visA['name'], visB['name'])
		convertToConcrete(visA)
		convertToConcrete(visB)
	else:
		convertToColloquial(visA)
		convertToColloquial(visB)
	matchTuples = sortMatch(diff['match'], diff)
	# TODO: list channels of each vis first, and then explain their encodings

	sameCount = 0
	diffCount = 0
	veryDiffCount = 0
	for pair in matchTuples:
		bi = pair[0]
		ai = pair[1]
		code = pair[2]
		encodingB = visB['encoding'][bi]
		count = sameCount + diffCount + veryDiffCount
		if count == 0:
			text += 'In a '
		elif count == 1:
			text += 'Then, in a '
		elif count >= 2:
			text += 'Next, in a '
		text += '%s, the %s of the %s represents %s' % (visB['name'], encodingB['channel'], visB['mark'], encodingB['data'])
		if code == 3: # no matching encoding (more encoding in visB than in visA)
			if veryDiffCount == 0:
				text += ', though this is not present in a %s. ' % (visA['name'])
			else:
				text += ', which is also not in a %s. ' % (visA['name'])
			veryDiffCount += 1
		else:
			encodingA = visA['encoding'][ai]
			if code == 0: # two exactly same encodings
				if sameCount >= 1:
					text += '. This is also the same for a %s. ' % (visA['name'])
				else:
					text += '. This is the same for a %s. ' % (visA['name'])
				sameCount += 1
			else:
				if code == 1: # difference in data
					text += '. However, in a %s, the %s of the %s represents %s. ' % (visA['name'], encodingA['channel'], visA['mark'], encodingA['data'])
				elif code == 2: # difference in channel
					text += '. However, in a %s, the %s of the %s represents %s. ' % (visA['name'], encodingA['channel'], visA['mark'], encodingA['data'])
				diffCount += 1

	count = 0
	if len(diff['encodingB']) >= 2:
		text += 'Furthermore, a %s has the following additional properties. ' % (visA['name'])
	elif len(diff['encodingB']) == 1:
		text += 'Furthermore, a %s has an additional property. ' % (visA['name'])

	for i in diff['encodingB']:
		encodingA = visA['encoding'][i]
		if count == 0:
			text += 'The %s of the %s represents %s. ' % (encodingA['channel'], visA['mark'], encodingA['data'])
		elif count == 1:
			text += 'And the %s of the %s represents %s. ' % (encodingA['channel'], visA['mark'], encodingA['data'])
		count += 1

	return text

def procedural(visA, visArr, concrete):
	visA = copy.deepcopy(visA)
	if concrete:
		convertToConcrete(visA)
		text = 'Imagine that you are drawing the chart in the air with your fingers. '
		text += 'Let me explain how to create a %s, with an example about fruits in a grocery store. ' % visA['name']
		text += 'Assume you have information about '
	else:
		convertToColloquial(visA)
		text = 'Imagine that you are drawing the chart in the air with your fingers. '
		text = 'Let me explain how to create a %s. ' % visA['name']
		text += 'Assume you have a list of data, each consisting of '

	for i in range(len(visA['encoding']) - 1):
		text += visA['encoding'][i]['data']
		text += ', '
	i = len(visA['encoding']) - 1
	if i == 0:
		text += '%s. ' % visA['encoding'][i]['data']
	else:
		text += 'and %s. ' % visA['encoding'][i]['data']

	# coordinate system
	if visA['coordinate_system'] == 'cartesian':
		text += 'First, draw a horizontal and a vertical axis. '
	elif visA['coordinate_system'] == 'linear':
		text += 'First, draw a single straight axis. '
	elif visA['coordinate_system'] == 'polar' or visA['coordinate_system'] == 'circular':
		text += 'First, think of a circle. '


	# mark
	text += 'You will then draw %ss to visualize data. ' % (visA['mark'])
	enc = visA['encoding']
	for i in range(len(enc)):
		if (i != 0):
			text += 'Next, '
		else:
			text += 'Now, '
		if concrete:
			text += '%s ' % enc[i]['data']
		else:
			text += '%s in the data ' % enc[i]['data']
		text += 'is mapped to the %s of the %ss. ' % (enc[i]['channel'], visA['mark'])

	text += 'If you are done, you have finished drawing a %s. ' % visA['name']
	return text

def procedural_compare(visA, visB, visArr, concrete):
	visA = copy.deepcopy(visA)
	visB = copy.deepcopy(visB)
	USELESSDISTANCE, diff = distance(visA, visB)

	text = 'Imagine that you are drawing the chart in the air with your fingers. '
	text = 'Let me explain how to create a %s with a %s. ' % (visA['name'], visB['name'])
	if concrete:
		text += "We will use fruits in a grocery store as an example. "
		convertToConcrete(visA)
		convertToConcrete(visB)
	else:
		convertToColloquial(visA)
		convertToColloquial(visB)

	#data
	text += 'Assume you have a list of data, each consisting of '
	for i in range(len(visA['encoding']) - 1):
		text += visA['encoding'][i]['data']
		text += ', '
	i = len(visA['encoding']) - 1
	if i == 0:
		text += '%s. ' % visA['encoding'][i]['data']
	else:
		text += 'and %s. ' % visA['encoding'][i]['data']

	# coordinate system
	if visA['coordinate_system'] == 'cartesian':
		text += 'First, draw a horizontal and a vertical axis, '
	elif visA['coordinate_system'] == 'linear':
		text += 'First, draw a single straight axis, '
	elif visA['coordinate_system'] == 'circular' or visA['coordinate_system'] == 'polar':
		text += 'First, think of a circle, '
	if diff['coordinate_system']:
		text += 'instead of '
		if visB['coordinate_system'] == 'cartesian':
			text += 'a horizontal axis and a vertical axis as you would in a %s. ' % (visB['name'])
		elif (visB['coordinate_system'] == 'polar' and not visA['coordinate_system'] == 'circular') or (visB['coordinate_system'] == 'circular' and not visA['coordinate_system'] == 'polar'):
			text += 'a circle as you would in a %s. ' % (visB['name'])
	else:
		text += 'just like when you want to draw a %s. ' % (visB['name']);

	# mark
	text += 'You will then draw %ss to visualize data' % (visA['mark'])
	if diff['mark']: 
		text += ', instead of %ss as in a %s. ' % (visB['mark'], visB['name'])
	else: 
		text += ', just like a %s. ' % (visB['name'])

	# encoding
	matchTuples = sortMatch(diff['match'], diff)
	
	sameCount = 0
	diffCount = 0
	veryDiffCount = 0
	for pair in matchTuples:
		ai = pair[0]
		bi = pair[1]
		code = pair[2]
		enc = visA['encoding'][ai]
		count = sameCount + diffCount + veryDiffCount
		if count == 0:
			text += 'To start, '
		elif count == 1:
			text += 'Then, '
		elif count >= 2:
			text += 'Next, '
		text += '%s in the data is mapped to the %s of the %s' % (enc['data'], enc['channel'], visA['mark'])
		if code == 3: # no matching encoding (more encoding in visA than in visB)
			if veryDiffCount == 0:
				text += ', though this is not the case in a %s. ' % (visB['name'])
			else:
				text += ', which is also not the case in a %s. ' % (visB['name'])
			veryDiffCount += 1
		else:
			if code == 0: # two exactly same encodings
				if sameCount >= 1:
					text += ', which is also the same when drawing a %s. ' % (visB['name'])
				else:
					text += ', which is the same when drawing a %s. ' % (visB['name'])
				sameCount += 1
			else:
				encodingB = visB['encoding'][bi]
				if code == 1: # difference in data
					text += ', while in a %s, %s in the data is mapped to %s. ' % (visB['name'], encodingB['data'], encodingB['channel'])
				elif code == 2: # difference in channel
					text += ', while in a %s, %s in the data is mapped to %s. ' % (visB['name'], encodingB['data'], encodingB['channel'])
				diffCount += 1


	text += 'If you are done, you have finished drawing a %s. ' % visA['name']

	return text