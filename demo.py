import math

a = (0, 0)
b = (100 ,0)
c = (120, -100)

v1 = (b[0] - a[0], b[1] - a[1])
v2 = (c[0] - b[0], c[1] - b[1])

dot = v1[0] * v2[0] + v1[1] * v2[1]

v1v = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
v2v = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

result = math.acos(dot / (v1v * v2v))

print(result * 180 / math.pi)
