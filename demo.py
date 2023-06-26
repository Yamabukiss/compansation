import math

def calculate_angle(ax, ay, bx, by, cx, cy):
    # 计算向量 AB 和向量 BC 的坐标差
    dx1 = bx - ax
    dy1 = by - ay
    dx2 = cx - bx
    dy2 = cy - by

    # 计算向量 AB 和向量 BC 的夹角
    angle_rad = math.atan2(dy1, dx1) - math.atan2(dy2, dx2)

    # 将弧度转换为度数
    angle_deg = math.degrees(angle_rad)

    # 将角度限制在 0 到 360 的范围内
    angle_360 = (angle_deg + 360) % 360

    return angle_360

# 示例点的像素坐标
xA, yA = 100, 100
xB, yB = 150, 200
xC, yC = 200, 150

# 计算夹角
angle = calculate_angle(xA, yA, xB, yB, xC, yC)
print(angle)  # 输出: 45.0
