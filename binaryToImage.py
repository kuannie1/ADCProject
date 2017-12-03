import cv2
import numpy as np
import re

file = open("binaryOutput.dat", "r")

binaryStr = file.read()
file.close()

binaryList = re.findall('........', binaryStr) # all the binary values we need
print "binaryList length: ", len(binaryList)

# convert each binary value into integers

decimalList = [(lambda binaryString : int(binaryString, 2))(x) for x in binaryList]

pixelList = []
# loop through decimalList in threes to restore original image:
for pixelIndex in range(0, len(decimalList), 3):
	b = decimalList[pixelIndex + 0]
	g = decimalList[pixelIndex + 1]
	r = decimalList[pixelIndex + 2]
	pixelValue = [b, g, r]
	pixelList.append(pixelValue)


# given we know the # of columns and rows, we can reconstruct the nested list of the picture
numColumns = 100
numRows = 100
print "# of pixels / column: ", len(pixelList)/numColumns

columnsList = []
for columnIndex in range(0, len(pixelList), numColumns):
	for pixelOffset in range(len(pixelList)/numColumns):

		columnsList.append(pixelList[pixelOffset + columnIndex])
	# columnsList.append(column)
print "columnsList length: ", len(columnsList)

rowsList = []
for rowIndex in range(0, len(columnsList), numRows):
	row = []
	for columnOffset in range(len(columnsList)/numRows):
		row.append(columnsList[columnOffset + rowIndex])
	rowsList.append(row)

print "rowsList length: ", len(rowsList)

picture = np.array(rowsList)
print picture

cv2.imwrite("result.jpg", picture)



file.close()