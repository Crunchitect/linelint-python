from get_junctions import get_junctions
from astar import get_path
import cv2, numpy as np, math


def dist(p1: list[int, int], p2: list[int, int]):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def cross_product(v1: list[int, int], v2: list[int, int]):
    return (v1[0] * v2[1]) - (v1[1] * v2[0])


path_str = "c"
maze = cv2.imread('assets/qwertyuiop.png')
path = np.array(get_path(maze, (100, 150), (100, 32)))
junctions = get_junctions(cv2.imread('assets/map.png'))
# print(junctions)
for x1, y1, x2, y2, x3, y3 in np.lib.stride_tricks.sliding_window_view(path.flatten(), (6,))[::2]:
    for junction_type, positions in junctions.items():
        for position in positions:
            is_intersection = (x2 == position[0] and y2 == position[1])
            in_between_intersection = (dist((x2, y2), position) == 1 and dist((x3, y3), position) == 1)
            if is_intersection or in_between_intersection:
                u = [x2 - x1, y2 - y1]
                v = [x3 - x2, y3 - y2]
                output = cross_product(u, v)
                if output > 0:
                    path_str += "lc"
                elif output == 0:
                    path_str += "fc"
                else:
                    path_str += "rc"
                break

print(path_str)
            