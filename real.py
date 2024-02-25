import cv2, copy
from colors import colors

img = cv2.imread('map.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edge_img = cv2.Canny(img, 10, 10)
contours, hierarchy = cv2.findContours(edge_img, 
    cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
img_contour = copy.deepcopy(img)
img_points = copy.deepcopy(img)
for i, contour in enumerate(contours):
    if i != 2: continue
    cv2.drawContours(img_contour, [contour], -1, colors[i+1], 3)
cv2.imshow('Countours', img_contour)

for i, path in enumerate(contours):
    for points in path:
        x, y = points[0]
        cv2.circle(img_points, (x, y), 1, colors[i], 1)
cv2.imshow('Points', img_points)

cv2.waitKey(0)
cv2.destroyAllWindows()