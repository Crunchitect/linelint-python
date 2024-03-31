import cv2, numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def get_path(maze, start, end):
    matrix = cv2.cvtColor(maze, cv2.COLOR_BGR2GRAY)
    (_, matrix) = cv2.threshold(matrix, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    matrix = cv2.bitwise_not(matrix).transpose().tolist()
    grid = Grid(matrix=matrix)

    # start = grid.node(104, 45)
    # end = grid.node(98, 434)

    startx = grid.node(*(start[::-1]))
    endx = grid.node(*(end[::-1]))

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(startx, endx, grid)

    print('operations:', runs, 'path length:', len(path))
    return np.array([[node.y, node.x] for node in path])