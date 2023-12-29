import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Helper:
	@staticmethod
	def rectangles_overlap(rect1, rect2, horizontal_margin = 0, vertical_margin=0):
		x1, y1, w1, h1 = rect1
		x2, y2, w2, h2 = rect2

		w1 += horizontal_margin

		# Check for horizontal overlap
		horizontal_overlap = (x1 < x2 + w2) and (x1 + w1 > x2)

		# Check for vertical overlap
		vertical_overlap = (y1 < y2 + h2) and (y1 + h1 > y2)

		# The rectangles overlap if there is both horizontal and vertical overlap
		return horizontal_overlap and vertical_overlap

	@staticmethod
	def merge(rect1, rect2):
		x_merge = min(rect1[0], rect2[0])
		y_merge = min(rect1[1], rect2[1])
		w_merge = max(rect1[0] + rect1[2], rect2[0] + rect2[2]) - x_merge
		h_merge = max(rect1[1] + rect1[3], rect2[1] + rect2[3]) - y_merge
		merged_rectangle = (x_merge, y_merge, w_merge, h_merge)
		return merged_rectangle


	@staticmethod
	def replace(rectangles, i, j, rect):
		if(i > j):
			rectangles.remove(rectangles[i])
			rectangles.remove(rectangles[j])
		else:
			rectangles.remove(rectangles[j])
			rectangles.remove(rectangles[i])

		rectangles.append(rect)




rect1 = (0, 0, 10, 10)
rect2 = (2, 2, 2, 2)
print(Helper.rectangles_overlap(rect1, rect2))
