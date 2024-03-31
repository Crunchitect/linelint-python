from modules.astar import get_path
import cv2

maze = cv2.imread('jello.png')
path = get_path(maze, (64, 521), (518, 233))
print(path)