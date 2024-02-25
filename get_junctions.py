import math
import cv2 as cv
import numpy as np


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


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
                return math.inf  # infinitely many solutions
        else:
            if y1 < y3 < y2 or y1 > y3 > y2:
                return math.inf  # infinitely many solutions

        if line1[0] == line2[0] or line1[1] == line2[0]:
            return line2[0]
        elif line1[0] == line2[1] or line1[1] == line2[1]:
            return line2[1]

        return None  # no intersection

    s = det1 / det
    t = det2 / det

    if 0.0 < s < 1.0 and 0.0 < t < 1.0:
        return x1 + t * dx1, y1 + t * dy1


def get_junctions(*, is_main: bool = False) -> tuple[cv.Mat, list[tuple[int, int]], list[tuple[int, int]]]:
    filename = 'map.png'
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)
    (_, im_bw) = cv.threshold(src, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    if src is None:
        print('Error opening image!')
        return -1

    dst = im_bw
    dst = cv.Canny(im_bw, 10, 10, None, 3)

    cdstP = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)

    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 20)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 1, cv.LINE_AA)

    # cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

    intersection_points: list[tuple[int, int]] = []
    plinesP = linesP.tolist()
    for a, b in cross_product(plinesP):
        if a == b: continue
        linea, lineb = a[0], b[0]
        intersection_point = line_intersection(linea, lineb)
        if not isinstance(intersection_point, tuple):
            continue
        intersection_point = (int(intersection_point[0]), int(intersection_point[1]))
        intersection_points.append(intersection_point)
        cv.circle(cdstP, intersection_point, 3, (0, 255, 0), 1)

    # cv.imshow("Detected Corners (in green) - Line Segment Intersection", cdstP)

    y_junctions: list[tuple[int, int]] = []
    # detect y junctions
    for a, b in cross_product(intersection_points):
        if a == b:
            continue
        if a[0] == b[0]:
            y_junction = (a[0], (a[1] + b[1]) // 2)
            
            y_junctions.append(y_junction)
    
    # cv.imshow("Detected Three-Way Juntions (in blue)", cdstP)

    t_junctions: list[tuple[int, int]] = []
    img_width = len(src[0])
    delta = img_width * 0.01
    # detect t junctions
    for a, b in cross_product(y_junctions):
        if a == b:
            continue
        if a[1] == b[1] and abs(a[0] - b[0]) < delta:
            t_junction = ((a[0] + b[0]) // 2, a[1])
            
            t_junctions.append(t_junction)
            y_junctions.remove(a)
            y_junctions.remove(b)
    

    for y_junction in y_junctions:
        cv.putText(cdstP, 'Y', y_junction, cv.FONT_HERSHEY_SIMPLEX, 2.0, (255, 0, 0), 3)
    for t_junction in t_junctions:
        cv.putText(cdstP, 'T', t_junction, cv.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 255), 3)
    
    if is_main:
        cv.imshow("Detected Four-Way Juntions (in yellow)", cdstP)
        cv.waitKey()
        return 0
    else:
        return cdstP, y_junctions, t_junctions


if __name__ == "__main__":
    get_junctions(is_main=True)
