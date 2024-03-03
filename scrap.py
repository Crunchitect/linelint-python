import math

x1, y1 = 1, 1
x2, y2 = 0.98, 2
dx = x2 - x1
dy = y2 - y1
theta = math.atan(dy / dx)

print(theta)