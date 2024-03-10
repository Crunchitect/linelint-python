from get_junctions import get_junctions
from astar import get_path
import cv2, numpy as np

maze = cv2.imread('assets/qwertyuiop.png')
# path = get_path(maze, (100, 150), (100, 32))
print(get_junctions(maze))