# -*- coding: utf-8 -*-

import cv2, numpy as np
from constants import *
from typing import Callable
from copy import deepcopy

maps = ['map.png', 'ttttttt.png', 'w.png']
map_index = 0

cross = np.array([
    [-0.5, 1, -0.5],
    [1, 1, 1],
    [-0.5, 1, -0.5]
], dtype=np.byte)


# funky notation lol
t_junction_kernels = {
    '⊢': np.array([[-0.5, 1, -0.5], [-0.5, 1, 1], [-0.5, 1, -0.5]], dtype=np.byte),
    '⊣': np.array([[-0.5, 1, -0.5], [1, 1, -0.5], [-0.5, 1, -0.5]], dtype=np.byte),
    '⊤': np.array([[-0.5, -0.5, -0.5], [1, 1, 1], [-0.5, 1, -0.5]], dtype=np.byte),
    '⊥': np.array([[-0.5, 1, -0.5], [1, 1, 1], [-0.5, -0.5, -0.5]], dtype=np.byte),
}

# `numpy` should have this as a builtin
def setdiff2d(x: np.array, y: np.array, /):
    return np.array(list(set(map(tuple, x.tolist())) - set(map(tuple, y.tolist()))))


def preprocess(img: cv2.Mat):
    grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thinned = cv2.ximgproc.thinning(cv2.bitwise_not(grayscaled))
    _, im_bw = cv2.threshold(thinned, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return cv2.bitwise_not(im_bw)

def detect(img: cv2.Mat, kernel: np.array):
    filtered_image = cv2.filter2D(img, -1, kernel)
    positions = np.vectorize(np.flip)(np.dstack(np.where(filtered_image == 0))[0])
    return positions

def get_junctions(img: cv2.Mat):
    to_tuple: Callable[[np.ndarray], tuple] = lambda matrix: tuple(map(tuple, matrix))
    results = {}
    field = preprocess(img)

    intersections = detect(field, cross)
    results[to_tuple(cross)] = intersections
    for t_junction_kernel in t_junction_kernels.values():
        t_junctions = detect(field, t_junction_kernel)
        t_junctions = setdiff2d(t_junctions, intersections)
        results[to_tuple(t_junction_kernel)] = t_junctions
    
    return results

def main():
    while True:
        img = cv2.imread(f'assets/{maps[map_index]}')
        grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thinned = cv2.ximgproc.thinning(cv2.bitwise_not(grayscaled))
        _, im_bw = cv2.threshold(thinned, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        crossed = cv2.filter2D(cv2.bitwise_not(thinned), -1, cross)
        intersections = np.dstack(np.where(crossed == 0))[0]
        for intersection in intersections:
            cv2.circle(img, np.flip(intersection), 3, (255, 0, 0), 3)

        for kernel_type, t_junction_kernel in t_junction_kernels.items():
            t_junction_filter = cv2.filter2D(cv2.bitwise_not(thinned), -1, t_junction_kernel)
            t_junctions = np.dstack(np.where(t_junction_filter == 0))[0]
            t_junctions = set(map(tuple, t_junctions.tolist())) - set(map(tuple, intersections.tolist()))
            for t_junction in t_junctions:
                cv2.circle(img, np.flip(t_junction), 3, (0, 0, 255), 3)
        
        cv2.imshow('result', img)
        if cv2.waitKey(1) == ESCAPE_KEY:
            break

if __name__ == '__main__':
    main()