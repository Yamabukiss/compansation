from compansation import Compansation, cv, math
from file_operation import read

def workPiecesDrawer(obj, contents):
    for i in range(0, len(contents) - 1):
        now = tuple(contents[i])
        after = tuple(contents[i + 1])
        try:
            if len(now) == 2 and len(after) == 2: # line 2 line
                start = now
                end = after
                obj.drawWorkPiecesLine(start, end)

            elif len(now) == 2 and len(after) == 5: # line 2 circle
                start = now
                end = (after[0], after[1])
                center = (after[2], after[3])
                radius = after[4]

                obj.drawWorkPiecesCircle(start, end, center, radius)

            elif len(now) == 5 and len(after) == 2: # circle 2 line
                start = (now[0], now[1])
                end = after
                obj.drawWorkPiecesLine(start, end)

            elif len(now) == 5 and len(after) == 5: # circle 2 circle
                start = (now[0], now[1])
                end = (after[0], after[1])
                center = (after[2], after[3])
                radius = after[4]

                obj.drawWorkPiecesCircle(start, end, center, radius)
            else:
                raise ValueError("You may have entered the wrong format in the parameters file")

        except:
            raise ValueError("You may have entered the wrong format in the parameters file")


def stateRecorder(start, middle, end):
    parameter_lst = []
    tmp_parameter_lst= [start, middle, end]
    for parameter in tmp_parameter_lst:
        parameter_lst.append(parameter)
    return parameter_lst

def isPointOnLine(x1, y1, x2, y2, x, y):
    if (x1 <= x <= x2 or x2 <= x <= x1) and (y1 <= y <= y2 or y2 <= y <= y1):
        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1
        if y == m * x + c:
            return True
    return False

def centerCompensation(center, p1, p2, new_p1, new_p2):
    new_p1x = new_p1[0] - p1[0]
    new_p1y = new_p1[1] - p1[1]

    new_p2x = new_p2[0] - p2[0]
    new_p2y = new_p2[1] - p2[1]

    new_x = center[0] + new_p1x + new_p2x
    nex_y = center[1] + new_p1y + new_p2y

    return new_x, nex_y


def directionJudgement(p1, p2, center):
    v1 = [p1[0] - center[0], p1[1] - center[1]]
    v2 = [p2[0] - center[0], p2[1] - center[1]]

    cross_product = v1[0] * v2[1] - v1[1] * v2[0]

    if cross_product > 0:
        radius = -math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    else:
        radius = math.sqrt(v1[0] ** 2 + v1[1] ** 2)

    return radius

def toolsDrawer(obj, contents):
    point_param_lst = []
    for i in range(0, len(contents)):
        if i % 2 == 0 and i + 2 <= len(contents) - 1:
            start = tuple(contents[i])
            middle = tuple(contents[i + 1])
            end = tuple(contents[i + 2])
            points_lst = []
            parameter_lst = []

            tmp_parameter_lst = stateRecorder(start, middle, end)
            parameter_lst.append(tmp_parameter_lst)

            new_points = obj.typeJudgement((start[0], start[1]), (middle[0], middle[1]), (end[0], end[1]))
            for i in range(0, len(new_points)):
                points_lst.append((int(new_points[i][0]), int(new_points[i][1])))
            point_param_lst.append([points_lst, parameter_lst])
        else:
            continue

    result_points = []
    for points,parameter  in point_param_lst:
        parameter = parameter[0]
        num_points = len(points)
        # if num_points == 3:
        for i in range(0, num_points - 1):
            if num_points == 4 and i == 1:
                p1 = (int(points[i][0]), int(points[i][1]))
                p2 = (int(points[i + 1][0]), int(points[i + 1][1]))
                result_points.extend([p1,p2])
                del points[i]
                i -= 1
                continue
            p1 = (int(points[i][0]), int(points[i][1]))
            p2 = (int(points[i + 1][0]), int(points[i + 1][1]))
            param1 = parameter[i]
            param2 = parameter[i + 1]

            # cv.circle(obj.board, p1, 3, (0, 0, 255), 2)
            # cv.circle(obj.board, p2, 3, (0, 0, 255), 2)

            if len(param1) == 2 and len(param2) == 2: # line 2 line
                result_points.extend([p1, p2])

            elif len(param1) == 2 and len(param2) == 5: # line 2 circle
                center = (param2[2], param2[3])
                radius = param2[4]
                points_lst = obj.generateArcPoints(center[0], center[1], radius, param1, param2, 100)
                new_points_lst = obj.toolsPathPlanning(points_lst, param1, param2, center)

                result_points.extend([p1, *new_points_lst, p2])

            elif len(param1) == 5 and len(param2) == 2: # circle 2 line
                result_points.extend([p1, p2])

            elif len(param1) == 5 and len(param2) == 5: # circle 2 circle
                center = (param2[2], param2[3])
                radius = param2[4]
                points_lst = obj.generateArcPoints(center[0], center[1], radius, param1, param2, 100)
                new_points_lst = obj.toolsPathPlanning(points_lst, param1, param2, center)

                result_points.extend([p1, *new_points_lst, p2])

            else:
                raise ValueError("You may have entered the wrong format in the parameters file")
    for i in range(0, len(result_points) - 1):
        obj.drawToolsLine(result_points[i], result_points[i + 1])
    if obj.work_pieces:
        obj.drawToolsLine(result_points[0], result_points[-1])

if __name__ == '__main__':
    obj = Compansation(offset=8, type=0)
    contents = read("./parameters.txt")

    workPiecesDrawer(obj, contents)
    toolsDrawer(obj, contents)
    cv.imshow("output", obj.board)
    cv.waitKey(0)
    cv.destroyAllWindows()