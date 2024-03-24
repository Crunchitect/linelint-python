import cv2

maze = cv2.imread('assets/maze.png')
ssawezsfynijkm = cv2.bitwise_not(cv2.ximgproc.thinning(cv2.bitwise_not(cv2.cvtColor(maze, cv2.COLOR_BGR2GRAY))))
cv2.imwrite('jello.png', ssawezsfynijkm)