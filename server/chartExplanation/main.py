import os
import flask
#import explanationMethods as em
import explanationMethods_ver2 as em
from urllib.parse import unquote

CONDITION_CODE = {
	'00': em.declarative,
	'01': em.procedural,
	'10': em.declarative_compare,
	'11': em.procedural_compare
}
visArr = em.importCsv("vis_spec.csv")

augmentedExplanations = {
	"nightingale chart": {
		"000": "A nightingale chart has a circular shape. There are pie slices, which encodes information through their color, length, and position. The color of the pie slice represents a category. Different colors represent different categories and same colors represent the same category. Then, the length of the pie slice represents a number. A longer pie slice represents a bigger number than a shorter pie slice. Next, the clock position of the pie slice represents time. A pie slice at the clockwise direction of another represents a later time.",
		"001": "A nightingale chart has a circular shape. There are pie slices, which encodes information through their color, length, and position. For example, consider a nightingale chart that shows information about fruits in a grocery store. The color of the pie slice represents the type of fruit. Different colors represent different types of fruit and same colors represent the same kind of fruit. Then, the length of the pie slice represents the price of fruit. A longer pie slice represents a higher price than a shorter pie slice. Next, the clock position of the pie slice represents the year. A pie slice in the clockwise direction of another represents the next year.",
		"010": "Imagine that you are drawing the chart in the air with your fingers. Let me explain how to create a nightingale chart. Assume you have a list of data, each consisting of a category, a number, and time. First, think of a circle. You will then draw pie slices to visualize data. Now, a category is mapped to the color of the pie slices. Each category is mapped to a different color. Next, a number is mapped to the length of the pie slices. A higher number is mapped to a longer pie slice, and a smaller number is mapped to a shorter pie slice. Next, time is mapped to the clock position of the pie slices. A later time is mapped to the clockwise direction of its previous time. If you are done, you have finished drawing a nightingale chart.",
		"011": "Imagine that you are drawing the chart in the air with your fingers. Let me explain how to create a nightingale chart, with an example about fruits in a grocery store. Assume you have information about the type of fruit, the price of fruit, and year. First, think of a circle, You will then draw pie slices to visualize data. Now, the type of fruit is mapped to the color of the pie slices. Data with different categories are mapped to different colors and data with the same category is mapped to a same color. Next, the price of fruit is mapped to the length of the pie slices. A higher price is mapped to a longer pie slice, and a shorter pie slice is mapped to a shorter pie slice. Next, year is mapped to the clock position of the pie slices. A year is mapped to the clockwise direction of its previous year. If you are done, you have finished drawing a nightingale chart."
	},
	"nightingale chart-pie chart": {
		"100": "A nightingale chart is similar to a pie chart, with minor differences. A pie chart has a circular shape, which is the same for a nightingale chart. A pie chart shows data with pie slices. Similarly, a nightingale chart has pie slices. In a pie chart, the color of the pie slice represents a category. This is the same for a nightingale chart. Each color represents a different category. Then, in a pie chart, the central angle of the pie slice represents a number. However, in a nightingale chart, the length of the pie slice represents a number. A longer pie slice represents a bigger number than a shorter pie slice. Furthermore, a nightingale chart has an additional property. The clock position of the pie slice represents time. A pie slice at the clockwise direction of another represents a later time.",
		"101": "A nightingale chart is similar to a pie chart, with minor differences. A pie chart has a circular shape, which is the same for a nightingale chart. A pie chart shows data with pie slices. Similarly, a nightingale chart has pie slices. For example, consider a nightingale chart and a pie chart that shows information about fruits in a grocery store. In a pie chart, the color of the pie slice represents the type of fruit. This is the same for a nightingale chart. Each color represents a different type of fruit. Then, in a pie chart, the central angle of the pie slice represents the price of fruit. However, in a nightingale chart, the length of the pie slice represents the number of fruits sold. A longer pie slice represents more fruits sold than a shorter pie slice. Furthermore, a nightingale chart has an additional property. The clock position of the pie slice represents the year. A pie slice in the clockwise direction of another represents the next year.",
		"110": "Let me explain how to create a nightingale chart with a pie chart. Assume you have a list of data, each consisting of a category, a number, and time. First, think of a circle, just like when you want to draw a pie chart. You will then draw pie slices to visualize data, just like a pie chart. To start, a category is mapped to the color of the pie slice, which is the same when drawing a pie chart. Each category is mapped to a different color. Then, a number is mapped to the length of the pie slice, while in a pie chart, a number is mapped to the central angle of the pie slice. A higher number is mapped to a longer pie slice, and a smaller number is mapped to a shorter pie slice. Next, time is mapped to the clock position of the pie slice, though this is not the case in a pie chart. A later time is mapped to the clockwise direction of its previous time. If you are done, you have finished drawing a nightingale chart.",
		"111": "Let me explain how to create a nightingale chart with a pie chart. We will use fruits in a grocery store as an example. Assume you have a list of data, each consisting of the type of fruit, the price of fruit, and year. First, think of a circle, just like when you want to draw a pie chart. You will then draw pie slices to visualize data, just like a pie chart. To start, the type of fruit is mapped to the color of the pie slice, which is the same when drawing a pie chart. Each type of fruit is mapped to a different color. Then, the number of fruits sold is mapped to the length of the pie slice, while in a pie chart, the number of fruits sold is mapped to the central angle of the pie slice. A higher number of fruits sold is mapped to a longer pie slice than a smaller number of fruits sold. Next, the year is mapped to the clock position of the pie slice, though this is not the case in a pie chart. A year is mapped to the clockwise direction of its previous year. If you are done, you have finished drawing a nightingale chart."
	},
	"table heatmap": {
		"000": "A table heatmap has a horizontal axis and a vertical axis. There are rows and columns of rectangular areas like a grid, which encodes information through their position and brightness of color. The vertical position of the rectangular area represents a category. Different horizontal positions represent different categories. Then, the vertical position of the rectangular area represents a number. A higher vertical position represents a higher number than a lower position. Next, the brightness of color of the rectangular area represents a number. A darker color represents a higher number than a brighter color.",
		"001": "A table heatmap has a horizontal axis and a vertical axis. There are rows and columns of rectangular areas like a grid, which encodes information through their position and brightness of color. For example, consider a table heatmap that shows information about fruits in a grocery store. The position of the rectangular area represents the type of fruit. Different horizontal positions represent different types of fruit. Then, the vertical position of the rectangular area represents the price of fruit. A higher vertical position represents a higher number than a lower position. Next, the brightness of color of the rectangular area represents the number of fruits sold. A darker color represents a higher number of fruits sold than a brighter color. ",
		"010": "Imagine that you are drawing the chart in the air with your fingers. Let me explain how to create a table heatmap. Assume you have a list of data, each consisting of a category, a number, and a number. First, draw a horizontal and a vertical axis. You will then draw rows and columns of rectangular areas like a grid to visualize data. Now, a category is mapped to the horizontal position of the rectangular areas. Each category is mapped to a different horizontal position. Next, a number is mapped to the vertical position of the rectangular areas. A higher number is mapped to a higher vertical position than a lower number. Next, another number is mapped to the brightness of color of the rectangular areas. A higher number is mapped to a darker color than a lower number. If you are done, you have finished drawing a table heatmap.",
		"011": "Imagine that you are drawing the chart in the air with your fingers. Let me explain how to create a table heatmap, with an example about fruits in a grocery store. Assume you have information about the type of fruit, the price of fruit, and the number of fruit sold. First, draw a horizontal and a vertical axis. You will then draw rows and columns of rectangular areas like a grid to visualize data. Now, the type of fruit is mapped to the horizontal position of the rectangular areas. Each type of fruit is mapped to a different horizontal position. Next, the price of fruit is mapped to the vertical position of the rectangular areas. A higher price is mapped to a higher vertical position than a lower price. Next, the number of fruits sold is mapped to the brightness of color of the rectangular areas. A higher number of fruit sold is mapped to a darker color than a lower number of fruit sold.If you are done, you have finished drawing a table heatmap.",
	},
	"table heatmap-line chart": {
		"100": "A table heatmap is similar to a line chart, with minor differences. A line chart has a horizontal axis and a vertical axis, which is the same for table heatmap. A line chart shows data with lines. However, a table heatmap shows data with rows and columns of rectangular areas like a grid. In a line chart, the horizontal position of the line represents time. However, in a table heatmap, the horizontal position of the rectangular area represents a category. Different horizontal positions represent different categories and the same horizontal position represents the same category. Next, in a line chart, the vertical position of the line represents a number. Similarly, in a table heatmap, the vertical position of a rectangular area represents a number. A higher vertical position represents a higher number than a lower position. Then, in a line chart, the color of the line represents a category. However, in a table heatmap, the brightness of color of rectangular areas represent a number. A darker color represents a higher number of fruits sold than a brighter color. ",
		"101": "A table heatmap is similar to a line chart, with minor differences. A line chart has a horizontal axis and a vertical axis, which is the same for table heatmap. A line chart shows data with lines. However, a table heatmap shows data with rows and columns of rectangular areas like a grid,. For example, consider a table heatmap and a line chart that shows information about fruits in a grocery store. In a line chart, the horizontal position of the line represents the year. However, in a table heatmap, the horizontal position of the rectangular area represents the type of fruit. Different horizontal positions represent different types of fruit and the same horizontal position represents the same type of fruit. Next, in a line chart, the vertical position of the line represents the price of fruit. Similarly, in a table heatmap, the vertical position of a rectangular area represents the price of fruit. A higher vertical position represents a higher price than a lower position. Then, in a line chart, the color of the line represents the type of fruit. However, in a table heatmap, the brightness of color of rectangular areas represent the number of fruits sold. A darker color represents a higher number of fruits sold than a brighter color. ",
		"110": "Let me explain how to create a table heatmap with a line chart. Assume you have a list of data, each consisting of a category, a number, and a number. First, draw a horizontal and a vertical axis, just like when you want to draw a line chart. You will then draw rows and columns of rectangular areas like a grid to visualize data, instead of lines as in a line chart. To start, a category is mapped to the horizontal position of the rectangular area, while in a line chart, a category is mapped to the color of the lines. Each cateogry is mapped to a different horizontal position. Then, a number is mapped to the vertical position of the rectangular area, just like in a line chart, where a number is mapped to the vertical position of the lines. A higher number is mapped to a higher vertical position than a lower number. Next, another number is mapped to the brightness of color of the rectangular area, which is not the case in a line chart. A higher number of fruits sold is mapped to a darker color than a lower number. If you are done, you have finished drawing a table heatmap. ",
		"111": "Let me explain how to create a table heatmap with a line chart. We will use fruits in a grocery store as an example. Assume you have a list of data, each consisting of the type of fruit, the price of fruit, and the number of fruit sold. First, draw a horizontal and a vertical axis, just like when you want to draw a line chart. You will then draw rows and columns of rectangular areas like a grid to visualize data, instead of lines as in a line chart. To start, the type of fruit is mapped to the horizontal position of the rectangular area, while in a line chart, the type of fruit is mapped to the color of the lines. Each type of fruit is mapped to a different horizontal position. Then, the price of fruit is mapped to the vertical position of the rectangular area, just like in a line chart, where the price of fruit is mapped to the vertical position of the lines. A higher price of fruit is mapped to a higher vertical position than a lower price of fruit. Next, the number of fruits sold is mapped to the brightness of color of the rectangular area. A higher number of fruits sold is mapped to a darker color than a lower number of fruits sold. If you are done, you have finished drawing a table heatmap. "
	},
	"donut chart": {
		"000": "A donut chart has a circular shape. There are donut slices, which encodes information through their color, and central angle. The color of the donut slice represents a category. Each color represents a different category. Then, the central angle of the donut slice represents a number. Wider central angle represents a higher number than a narrower central angle.",
		"001": "A donut chart has a circular shape. There are donut slices, which encodes information through their color, and central angle. For example, consider a donut chart that shows information about fruits in a grocery store. The color of the donut slice represents the type of fruit. Each color represents a different type of fruit. Then, the central angle of the donut slice represents how many fruits were sold. Wider central angle represents a higher number of sold fruits than a narrower central angle.",
		"010": "Imagine that you are drawing the chart in the air with your fingers. Let me explain how to create a donut chart. Assume you have a list of data, each consisting of a category, and a number. First, think of a circle. You will then draw donut slices to visualize data. Now, a category is mapped to the color of the donut slices. Each category is mapped to a different color. Next, a number is mapped to the central angle of the donut slices. Higher number is mapped to a wider central angle than a lower number. If you are done, you have finished drawing a donut chart.",
		"011": "Imagine that you are drawing the chart in the air with your fingers. Let me explain how to create a donut chart, with an example about fruits in a grocery store. Assume you have information about the type of fruit, and the price of fruit. First, think of a circle. You will then draw donut slices to visualize data. Now, how many fruits were sold is mapped to the color of the donut slices. Each type of fruit is mapped to a different color. Next, the number of fruits sold is mapped to the central angle of the donut slices. Higher number of fruits sold is mapped to a wider central angle than a lower number of fruits sold. If you are done, you have finished drawing a donut chart."
	},
	"donut chart-pie chart": {
		"100": "A donut chart is similar to a pie chart, with minor differences. A pie chart has a circular shape, which is the same for a donut chart. A pie chart shows data with pie slices. However, a donut chart shows data with donut slices. In a pie chart, the color of the pie slice represents a category.  This is the same for a donut chart. Each color represents a different category. Then, in a pie chart, the central angle of the pie slice represents a number. This is also the same for a donut chart. Wider central angle represents a higher number than a narrower central angle.",
		"101": "A donut chart is similar to a pie chart, with minor differences. A pie chart has a circular shape, which is the same for donut chart. A pie chart shows data with pie slices. However, a donut chart shows data with donut slices. For example, consider a donut chart and a pie chart that shows information about fruits in a grocery store. In a pie chart, the color of the pie slice represents the type of fruit. This is the same for a donut chart. Each color represents a different type of fruit. Then, in a pie chart, the central angle of the pie slice represents the price of fruit. This is also the same for a donut chart. Wider central angle represents a higher number of sold fruits than a narrower central angle.",
		"110": "Let me explain how to create a donut chart with a pie chart. Assume you have a list of data, each consisting of a category, and a number. First, think of a circle, just like when you want to draw a pie chart. You will then draw donut slices to visualize data, instead of pie slices as in a pie chart. To start, a category is mapped to the color of the donut slice, which is the same when drawing a pie chart. Each category is mapped to a different color. Then, a number is mapped to the central angle of the donut slice, which is also the same when drawing a pie chart.  Higher number is mapped to a wider central angle than a lower number. If you are done, you have finished drawing a donut chart. ",
		"111": "Let me explain how to create a donut chart with a pie chart. We will use fruits in a grocery store as an example. Assume you have a list of data, each consisting of the type of fruit, and the price of fruit. First, think of a circle, just like when you want to draw a pie chart. You will then draw donut slices to visualize data, instead of pie slices as in a pie chart. To start, the type of fruit is mapped to the color of the donut slice, which is the same when drawing a pie chart. Each type of fruit is mapped to a different color. Then, the price of fruit is mapped to the central angle of the donut slice, which is also the same when drawing a pie chart. Higher number of fruits sold is mapped to a wider central angle than a lower number of fruits sold. If you are done, you have finished drawing a donut chart. "
	},
	"treemap": {
		"000": "A treemap has a horizontal axis and a vertical axis. There are rectangular areas, which encodes information through their position, and size. The nested position of the rectangular area represents a category. A rectangular area placed inside another rectangular area represents that a category is a part of another category. Then, the size of the rectangular area represents a number. Bigger size represents a bigger number than smaller size.",
		"001": "A treemap has a horizontal axis and a vertical axis. There are rectangular areas, which encodes information through their position, and size. For example, consider a treemap that shows information about fruits in a grocery store. The nested position of the rectangular area represents the type of fruit. A rectangular area placed inside another rectangular area represents that a type of fruit is a part of another type of fruit. Then, the size of the rectangular area represents the price of fruit. Bigger size represents a higher price of fruit than smaller size.",
		"010": "Imagine that you are drawing the chart in the air with your fingers. Let me explain how to create a treemap. Assume you have a list of data, each consisting of a category, and a number. First, draw a horizontal and a vertical axis. You will then draw rectangular areas to visualize data. Now, a category is mapped to the nested position of the rectangular areas. If a category is a part of another category, a rectangular area is placed inside another rectangular area. Next, a number is mapped to the size of the rectangular areas. A bigger number is mapped to a bigger rectangular area than a smaller number. If you are done, you have finished drawing a treemap. ",
		"011": "Imagine that you are drawing the chart in the air with your fingers. Let me explain how to create a treemap, with an example about fruits in a grocery store. Assume you have information about the type of fruit, and the price of fruit. First, draw a horizontal and a vertical axis. You will then draw rectangular areas to visualize data. Now, the type of fruit is mapped to the nested position of the rectangular areas.  If a type of fruit  is a part of another type of fruit, a rectangular area is placed inside another rectangular area. Next, the price of fruit is mapped to the size of the rectangular areas. If you are done, you have finished drawing a treemap. A higher price of fruit is mapped to a bigger rectangular area than a lower price. "
	},
	"treemap-bar chart": {
		"100": "A treemap is similar to a bar chart, with minor differences. A bar chart has a horizontal axis and a vertical axis, which is the same for treemap. A bar chart shows data with bars. However, a treemap shows data with rectangular areas. In a bar chart, the horizontal position of the bar represents a category, while in a treemap, the nested position of the rectangular area represents a category. A rectangular area placed inside another rectangular area represents that a category is a part of another category. Then, in a bar chart, the length of the bar represents a number. However, in a treemap, the size of the rectangular area represents a number. Bigger size represents a bigger number than smaller size.",
		"101": "A treemap is similar to a bar chart, with minor differences. A bar chart has a horizontal axis and a vertical axis, which is the same for treemap. A bar chart shows data with bars. However, a treemap shows data with rectangular areas. For example, consider a treemap and a bar chart that shows information about fruits in a grocery store. In a bar chart, the horizontal position of the bar represents the type of fruit, while in a treemap, the nested position of the rectangular area represents the type of fruit. A rectangular area placed inside another rectangular area represents that a type of fruit is a part of another type of fruit. Then, in a bar chart, the length of the bar represents the price of fruit. However, in a treemap, the size of the rectangular area represents the price of fruit. Bigger size represents a higher price of fruit than smaller size.",
		"110": "Let me explain how to create a treemap with a bar chart. Assume you have a list of data, each consisting of a category, and a number. First, draw a horizontal and a vertical axis, just like when you want to draw a bar chart. You will then draw rectangular areas to visualize data, instead of bars as in a bar chart. To start, a category is mapped to the nested position of the rectangular area, while in a bar chart, a category is mapped to the horizontal position of the bar. If a category is a part of another category, a rectangular area is placed inside another rectangular area. Then, a number is mapped to the size of the rectangular area, while in a bar chart, a number is mapped to length. A bigger number is mapped to a bigger rectangular area than a smaller number. If you are done, you have finished drawing a treemap.",
		"111": "Let me explain how to create a treemap with a bar chart. We will use fruits in a grocery store as an example. Assume you have a list of data, each consisting of the type of fruit, and the price of fruit. First, draw a horizontal and a vertical axis, just like when you want to draw a bar chart. You will then draw rectangular areas to visualize data, instead of bars as in a bar chart. To start, the type of fruit is mapped to the nested position of the rectangular area, while in a bar chart, the type of fruit is mapped to the horizontal position of the bar. If a type of fruit is a part of another type of fruit, a rectangular area is placed inside another rectangular area. Then, the price of fruit is mapped to the size of the rectangular area, while in a bar chart, the price of fruit is mapped to length. A higher price of fruit is mapped to a bigger rectangular area than a lower price of fruit. If you are done, you have finished drawing a treemap."		
	},
	"stacked bar chart": {
		"000": "A stacked bar chart has a horizontal axis and a vertical axis. There are bars, which encodes information through their position, color, and length. The horizontal position of the bar represents a category. Then, the color of the bar represents another category. Next, the length of each bar represents a number. Bars with different colors but with the same horizontal position are stacked on top of one another.",
		"001": "A stacked bar chart has a horizontal axis and a vertical axis. There are multiple bars, which encode information through their horizontal position, color, and vertical length. For example, consider a stacked bar chart that shows the price of different types of fruit for each month. First, the horizontal position of the bar represents the month. Next, the color of the bar represents the type of fruit. Then, the length of the bar represents the price of fruit. Bars that represent different types of fruit but are in the same month are vertically stacked on top of one another.",
		"010": "Let me explain how to create a stacked bar chart. Assume you have a list of data, each consisting of a category, another category, and a number. First, draw a horizontal and a vertical axis. You will then draw bars to visualize data. Now, a category is mapped to the horizontal position of the bars. Next, another category is mapped to the color of the bars. Next, a number is mapped to the length of the bars. Bars with different colors but with the same horizontal position are stacked on top of one another. If you are done, you have finished drawing a stacked bar chart. "
	},
	"stacked bar chart-bar chart": {
		"111": "Let me explain how to create a stacked bar chart with a bar chart. We will use fruits in a grocery store as an example. Assume you have a list of data, each consisting of the type of fruit and the price of fruit for each month. First, draw a horizontal and a vertical axis, just like a bar chart. You will then draw bars to visualize data, just like a bar chart. To start, each month is represented by the horizontal position of the bar, just like in a bar chart. Then, the price of fruit is represented by the vertical length of the bar, just like in a bar chart. Next, the color of fruit is represented by the color of the bar. Bars that represent different types of fruit but represent the same month are vertically stacked on top of one another. If you are done, you have finished drawing a stacked bar chart."
	},
	"radar chart": {
		"010": "Imagine that you are drawing the chart in the air with your fingers. Let me explain how to create a radar chart. Assume you have a list of data, each consisting of a category, and a number. First, think of a circular axis or a clock. You will then draw points and connect them with line segments to visualize data. A category is mapped to the clockwise position of the point. Different categories are mapped to different positions around the circular axis. Then, a number is mapped to the point’s distance from the center. Higher number is mapped to further distance from the center than a smaller number. Finally, you connect the points with line segments, just like in a line chart. If you are done, you have finished drawing a radar chart. "
	},
	"radar chart-line chart": {
		"110": "Let me explain how to create a radar chart with a line chart. Assume you have a list of data, each consisting of a category, and a number. First, think of a circle or a clock, instead of a horizontal axis and a vertical axis as you would in a line chart. You will then draw points and connect them with line segments, just like in a line chart. To start, a category is mapped to the clockwise position of the point, though this is not the case in a line chart. Then, a number is mapped to the point’s distance from the center, which is also not the case in a line chart. Finally, you connect the points with line segments, just like in a line chart. If you are done, you have finished drawing a radar chart.",
		"101": "A radar chart is similar to a line chart, with minor differences. A line chart has a horizontal axis and a vertical axis, whereas a radar chart has a shape of a circle or a clock. A line chart shows data with line segments that connect points. Similarly, a radar chart has line segments that connect points. For example, consider a radar chart and a line chart that shows information about fruits in a grocery store. In a line chart, the vertical position of a point represents the price of fruit, though in a radar chart, the point’s distance from the center represents the price of fruit. Then, in a line chart, the horizontal position of a point represents the year. On the other hand, in a radar chart, the clockwise position of a point represents the type of fruit.",
		"111": "Imagine that you are drawing the chart in the air with your fingers. Let me explain how to create a radar chart with a line chart. Assume you want to draw a radar chart that shows the prices of different types of fruit. First, think of a circle, instead of a horizontal and a vertical axis. You will then draw points and connect them with line segments, just like in a line chart. To start, the type of fruit is represented by the clockwise position of the point. Then, the price of fruit is represented by the point’s distance from the center of the circle. Finally, connect the points with a line, just like a line chart. If you are done, you have finished drawing a radar chart."
	},
	"radial bar chart": {
		"001": "A radial bar chart has a circular shape. There are bars, which encode information through their position from the center, and the length around the circle. For example, consider a radial bar chart that shows information about fruits in a grocery store. The distance of the bar’s position from the center of the circle represents the type of fruit. Different distances from the center represent different types of fruit. Then, the length of the bars around the circle represents the price of fruit. Bars that goes around the circle longer represent higher prices."
	},
	"radial bar chart-bar chart": {
		"100": "A radial bar chart is similar to a bar chart, with minor differences. Unlike a bar chart, a radial bar chart has a circular axis. A radial bar chart has bars, like a bar chart. In a radial bar chart, the distance of the bar from the center of the circle represents a category, while in a bar chart, the horizontal position represents a category. Then, in a radial bar chart, the length of the bars around the circle represents a number, while in a bar chart, the vertical length of the bars represent a number."
	}
}

def getExplanations(request):
	if request.method == 'OPTIONS':
	# Allows GET requests from any origin with the Content-Type
	# header and caches preflight response for an 3600s
		headers = {
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'GET',
			'Access-Control-Allow-Headers': 'Content-Type',
			'Access-Control-Max-Age': '3600'
		}
		return ('', 204, headers)

	# Set CORS headers for the main request
	headers = {
		'Access-Control-Allow-Origin': '*'
	}

	args = request.args
	
	visArr = em.importCsv("vis_spec.csv")

	text = ""
	if not args: 
		return False

	conditions = args["condition"].split(',')
	chartTypes = args["stimuli"].split(',')
	for i in range(len(chartTypes)):
		cond = conditions[i]
		concrete = False
		if cond[2] == '1':
			concrete = True
		if cond[0] == '1':
			viss = list(map(unquote, chartTypes[i].split('-')))
			orig = viss[0] + '-' + viss[1]
			if orig in augmentedExplanations and cond in augmentedExplanations[orig]:
					text += augmentedExplanations[orig][cond]
			else:
				visA = em.getVisFromArr(visArr, viss[0])
				visB = em.getVisFromArr(visArr, viss[1])
				text += CONDITION_CODE[cond[0:2]](visA, visB, visArr, concrete)
		else:
			visA = em.getVisFromArr(visArr, unquote(chartTypes[i]))
			visName = visA['name']
			if visName in augmentedExplanations and cond in augmentedExplanations[visName]:
					text += augmentedExplanations[visName][cond]
			else:
				text += CONDITION_CODE[cond[0:2]](visA, visArr, concrete)
		if i != len(chartTypes) - 1:
			text += '|||'

	return (text, 200, headers)

def getDistance(visAName, visBName):
	visA = em.getVisFromArr(visArr, visAName)
	visB = em.getVisFromArr(visArr, visBName)
	# return em.distance(visA, visB)[0]
	return("%s-%s: %d" % (visAName, visBName, em.distance(visA, visB)[0]))

if __name__ == "__main__":
	### Condition code description
	### Condition code is a three-digit binary string, from 000 to 111
	### first digit: 0 means no comparison, 1 means comparison
	###		if this is 1, then the 'stimuli' string must be in the format of "chart1-chart2", 
	### 	where chart 1 is explaned by comparing it to chart 2
	### second digit: 0 means declarative, 1 means procedural
	### third digit: 0 means abstract, 1 means concrete

	### stimuli string description
	### the type of chart that you want explanation for
	### refer to vis_spec.csv for the supported type of charts
	### space is indicated as '%20'. For example, a pie chart is "pie%20chart"  


	### Example: histogram explanation with [no comparison, declarative, abstact] strategy
	# class Rq:
	# 	args = {
	# 		'condition': '000',
	# 		'stimuli': 'histogram'
	# 	}
	# 	method = ""

	### Example: nightingale chart explanation, compared to a pie chart, procedural, and concrete
	class Rq:
		args = {
			'condition': '111',
			'stimuli': 'nightingale%20chart-pie%20chart'
		}
		method = ""

	### Example: explanation of 4 charts, each with different explanation strategy
	# class Rq:
	# 	args = {
	# 		'condition': '000,011,110,101',
	# 		'stimuli': 'histogram,bar%20chart,nightingale%20chart-pie%20chart,colored%20bubble%20chart-scatterplot'
	# 	}
	# 	method = ""

	request = Rq()

	text = getExplanations(request)
	text = text[0].split('|||')
	for i in range(len(text)):
		print("%i. %s" % (i+1, text[i]))