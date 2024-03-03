import math
import cv2 as cv
import numpy as np
from typing import Iterable

def combinations(list_1, list_2):
    unique_combinations = []
    for i in range(len(list_1)):
        for j in range(len(list_2)):
            unique_combinations.append((list_1[i], list_2[j]))
    return unique_combinations

def cross_product(array):
    permutations = []
    for i, val1 in enumerate(array):
        for val2 in array[i+1:]:
            permutations.append((val1, val2))
    return permutations


def extrude_line(line, coeff=0.01):
    sign = lambda x: 0 if x == 0 else abs(x) // x
    x1, y1, x2, y2 = line
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)

    x1 += int(sign(x1 - x2) * coeff * length)
    x2 += int(sign(x2 - x1) * coeff * length)
    y1 += int(sign(y1 - y2) * coeff * length)
    y2 += int(sign(y2 - y1) * coeff * length)
    dx = x2 - x1
    dy = y2 - y1
    return x1, y1, x2, y2

def line_intersection(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    dx1 = x2 - x1
    dx2 = x4 - x3
    dy1 = y2 - y1
    dy2 = y4 - y3
    dx3 = x1 - x3
    dy3 = y1 - y3

    det = dx1 * dy2 - dx2 * dy1
    det1 = dx1 * dy3 - dx3 * dy1
    det2 = dx2 * dy3 - dx3 * dy2

    if det == 0.0:  # lines are parallel
        if det1 != 0.0 or det2 != 0.0:  # lines are not co-linear
            return None  # so no solution

        if dx1:
            if x1 < x3 < x2 or x1 > x3 > x2:
                return None
        else:
            if y1 < y3 < y2 or y1 > y3 > y2:
                return None

        if line1[0] == line2[0] or line1[1] == line2[0]:
            return line2[0]
        elif line1[0] == line2[1] or line1[1] == line2[1]:
            return line2[1]

        return None  # no intersection

    s = det1 / det
    t = det2 / det

    if 0.0 < s < 1.0 and 0.0 < t < 1.0:
        return int(x1 + t * dx1), int(y1 + t * dy1)


def get_junctions(*, is_main: bool = False) -> tuple[cv.Mat, list[tuple[int, int]], list[tuple[int, int]]]:
    filename = 'assets/map.png'
    src = cv.imread(cv.samples.findFile(filename))
    im_bw = cv.ximgproc.thinning(cv.bitwise_not(cv.cvtColor(src, cv.COLOR_BGR2GRAY)))
    if src is None:
        print('Error opening image!')
        return -1
    dst = im_bw
    cdstP = cv.cvtColor(im_bw, cv.COLOR_GRAY2BGR)
    # cv.imshow("Source", cdstP)
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 20)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 1, cv.LINE_AA)

    # cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
    

    intersection_points: list[tuple[int, int]] = []
    t_junctions = []
    plinesP = linesP.tolist()
    for a, b in cross_product(plinesP):
        if a == b: continue
        linea, lineb = a[0], b[0]

        linea_long, lineb_long = extrude_line(linea), extrude_line(lineb)
        intersection_point_long = line_intersection(linea, lineb_long)
        if intersection_point_long:
            print('!')
            cv.circle(cdstP, intersection_point_long, 5, (255, 255, 0), 3)
            t_junctions.append([intersection_point_long, lineb])
        intersection_point_long = line_intersection(linea_long, lineb)
        if intersection_point_long:
            print('!')
            cv.circle(cdstP, intersection_point_long, 5, (0, 255, 255), 3)
            t_junctions.append([intersection_point_long, linea])

        intersection_point = line_intersection(linea, lineb)
        if not intersection_point:
            continue
        intersection_points.append(intersection_point)
        cv.circle(cdstP, intersection_point, 5, (0, 255, 0), 3)

    if is_main:
        cv.imshow("Detected Four-Way Juntions (in yellow)", cdstP)
        cv.waitKey()
        return 0
    else:
        return cdstP, intersection_points, t_junctions


if __name__ == "__main__":
    get_junctions(is_main=True)
