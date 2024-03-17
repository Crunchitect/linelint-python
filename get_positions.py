import cv2

filepath = 'assets/map.png'

img = cv2.imread(filepath, cv2.COLOR_BGR2GRAY)

cv2.imshow("Image", img)
cv2.waitKey(0)