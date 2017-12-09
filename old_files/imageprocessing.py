import cv2
import numpy as np

imgName = "rgb.jpg"

img = cv2.imread(imgName)
imgHeight = len(img)
imgWidth = len(img[0])


# get top left corner
roi = img[0:100, 0:100]
print roi
print len(roi)
print len(roi[0])
print len(roi[0][0])


# cv2.imwrite("roi.jpg", roi)

# based on each number in the list, append a 8-bit string for each R, G, and B value
bits = ""
bitlist = []
for row_index in range(len(roi)):

	for column_index in range(len(roi[row_index])):

		for color_index in range(len(roi[row_index][column_index])):

			color_val = roi[row_index][column_index][color_index]
			binaryColorVal = '{0:08b}'.format(color_val)
			bitlist.append(binaryColorVal)
			bits += binaryColorVal
print "length: ",  len(bitlist)

with open("binaryOutput.dat", 'w') as f:
	f.write(bits)


print "one row: ", roi[0]
print "one column: ", roi[0][0]

# # split into RGB channels:

# # b,g,r = cv2.split(img)

# # cv2.imwrite("b.jpg", b)

# # cv2.imwrite("g.jpg", g)

# # cv2.imwrite("a.jpg", r)