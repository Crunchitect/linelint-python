from modules.get_junctions import get_junctions
from modules.astar import get_path
from functools import cache
import cv2, numpy as np

@cache
def cross_product(v1: tuple[int, int], v2: tuple[int, int]):
    return (v1[0] * v2[1]) - (v1[1] * v2[0])


path_str = "cross();\n"
maze = cv2.imread('assets/real.png')
path = get_path(maze, (45, 104), (434, 98))
junctions = get_junctions(maze)
i = 0
for x1, y1, x2, y2, x3, y3 in np.lib.stride_tricks.sliding_window_view(path.flatten(), (6,))[::2]:
    print(i)
    i += 1
    for junction_type, positions in junctions.items():
        for position in positions:
            if x2 == position[0] and y2 == position[1]:
                u = (x2 - x1, y2 - y1)
                v = (x3 - x2, y3 - y2)
                output = cross_product(u, v)
                if output > 0:
                    path_str += "\tleft(); cross();\n"
                elif output == 0:
                    path_str += "\tforward(); cross();\n"
                else:
                    path_str += "\tright(); cross();\n"
                break

print(path_str)

source_code = ""

with open("base/sim.txt", "r") as f:
    source_code += f.read()

source_code += path_str
source_code += '}\n'

with open("output.txt", "w") as f:
    f.write(source_code)
