# -*- coding: utf-8 -*-

import cv2, numpy as np
# from modules.constants import *
from typing import Callable

maps = ['map.png', 'ttttttt.png', 'w.png']
map_index = 0

cross = np.array([
    [-3, 1, -3],
    [1, 1, 1],
    [-3, 1, -3]
], dtype=np.byte)


# funky notation lol
kernels = [
    np.array([[-3, 1, -3], [-3, 1, 1], [-3, 1, -3]]),
    np.array([[-3, 1, -3], [1, 1, -3], [-3, 1, -3]]),
    np.array([[-3, -3, -3], [1, 1, 1], [-3, 1, -3]]),
    np.array([[-3, 1, -3], [1, 1, 1], [-3, -3, -3]]),
    np.array([[-3, 1, -3], [1, 1, -3], [-3, -3, -3]]),
    np.array([[-3, 1, -3], [-3, 1, 1], [-3, -3, -3]]),
    np.array([[-3, -3, -3], [-3, 1, 1], [-3, 1, -3]]),
    np.array([[-3, -3, -3], [1, 1, -3], [-3, 1, -3]]),
]

# `numpy` should have this as a builtin
def setdiff2d(x: np.array, y: np.array, /):
    return np.array(list(set(map(tuple, x.tolist())) - set(map(tuple, y.tolist()))))


def preprocess(img: cv2.Mat, thin=True):
    grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if thin:
        thinned = cv2.ximgproc.thinning(cv2.bitwise_not(grayscaled))
    else:
        thinned = cv2.bitwise_not(grayscaled)
    _, im_bw = cv2.threshold(thinned, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow("a", im_bw)
    # cv2.waitKey(0)
    return im_bw

def detect(img: cv2.Mat, kernel: np.array):
    image = img.astype(np.int16)
    image[image == 255] = -1
    image[image == 0] = 1
    filtered_image = cv2.filter2D(image, -1, kernel)
    positions = np.vectorize(np.flip)(np.dstack(np.where(filtered_image >= 7))[0])
    return positions

def get_junctions(img: cv2.Mat, thin=True):
    to_tuple: Callable[[np.ndarray], tuple] = lambda matrix: tuple(map(tuple, matrix))
    results = {}
    field = preprocess(img, thin)

    intersections = detect(field, cross)
    print(intersections)
    results[to_tuple(cross)] = intersections
    # for kernel in kernels:
    #     junctions = detect(field, kernel)
    #     results[to_tuple(kernel)] = junctions
    return intersections
    # return results

def main():
    while True:
        img = cv2.imread(f'jello.png')
        grayscaled = cv2.bitwise_not(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
        # thinned = cv2.ximgproc.thinning(cv2.bitwise_not(grayscaled))
        _, im_bw = cv2.threshold(grayscaled, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        im_bw = im_bw.astype(np.int16)
        im_bw[im_bw == 255] = -1
        im_bw[im_bw == 0] = 1
        crossed = cv2.filter2D(im_bw, -1, cross)
        intersections = np.dstack(np.where(crossed >= 7))[0]
        for intersection in intersections:
            cv2.circle(grayscaled, np.flip(intersection), 3, (69, 0, 0), 3)

        for i, kernel in enumerate(kernels):
            filtered = cv2.filter2D(im_bw, -1, kernel)
            junctions = np.dstack(np.where(filtered == np.max(filtered)))[0]
            junctions = set(map(tuple, junctions.tolist())) - set(map(tuple, intersections.tolist()))
            for junction in junctions:
                cv2.circle(grayscaled, np.flip(junction), 3, (0, 0, 128), 3)
        
        cv2.imshow('result', grayscaled)
        if cv2.waitKey(1) == 27:
            break

if __name__ == '__main__':
    main()