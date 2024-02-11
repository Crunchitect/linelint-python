import sys
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


def main(argv):
    default_file = 'map.png'
    filename = argv[0] if len(argv) > 0 else default_file
    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)
    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        print('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1

    dst = cv.Canny(src, 10, 10, None, 3)

    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            cv.line(cdst, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)

    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 20)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 1, cv.LINE_AA)

    plinesP = linesP.tolist()
    for a, b in combinations(plinesP, plinesP):
        linea, lineb = a[0], b[0]
        # linea = [i * 1 for i in linea]
        # lineb = [i * 1 for i in lineb]
        print(linea, lineb)
        intersection_point = line_intersection(linea, lineb)
        if isinstance(intersection_point, int) or not intersection_point or isinstance(intersection_point, float):
            continue
        intersection_point = (int(intersection_point[0]), int(intersection_point[1]))
        print(intersection_point)
        cv.circle(cdstP, intersection_point, 5, (0, 255, 0), 1)

    # cv.imshow("Source", src)
    # cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

    cv.waitKey()
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
