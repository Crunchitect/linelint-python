import math

x1, y1 = 1, 1
x2, y2 = 2, 2
dx = x2 - x1
dy = y2 - y1
length = math.hypot(dx, dy)
coeff = 0.1


x1 += math.copysign(1, x1 - x2) * coeff * length
x2 += math.copysign(1, x2 - x1) * coeff * length
y1 += math.copysign(1, y1 - y2) * coeff * length
y2 += math.copysign(1, y2 - y1) * coeff * length

print(x1, y1, x2, y2)