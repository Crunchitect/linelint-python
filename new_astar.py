import cv2
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# matrix = [
#   [1, 1, 1],
#   [1, 0, 1],
#   [1, 1, 1]
# ]
matrix = cv2.imread('assets/real.png', cv2.IMREAD_GRAYSCALE)
(_, matrix) = cv2.threshold(matrix, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
matrix = cv2.bitwise_not(matrix).transpose().tolist()
grid = Grid(matrix=matrix)

start = grid.node(104, 45)
end = grid.node(98, 434)

finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
path, runs = finder.find_path(start, end, grid)

print('operations:', runs, 'path length:', len(path))
print([(node.x, node.y) for node in path])