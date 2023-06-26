from compansation import Compansation, cv
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
    length1, length2, length3 = len(start), len(middle), len(end)
    tmp_state_lst = [length1, length2, length3]
    tmp_parameter_lst= [start, middle, end]
    for length, parameter in zip(tmp_state_lst, tmp_parameter_lst):
        if length == 5:
            parameter_lst.append(parameter[2:])
        else:
            parameter_lst.append([0])
    return parameter_lst

def isPointOnLine(x1, y1, x2, y2, x, y):
    if (x1 <= x <= x2 or x2 <= x <= x1) and (y1 <= y <= y2 or y2 <= y <= y1):
        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1
        if y == m * x + c:
            return True
    return False

def toolsDrawer(obj, contents):
    points_lst = []
    parameter_lst = []
    for i in range(0, len(contents)):
        if i % 2 == 0 and i + 2 <= len(contents) - 1:
            start = tuple(contents[i])
            middle = tuple(contents[i + 1])
            end = tuple(contents[i + 2])

            tmp_parameter_lst = stateRecorder(start, middle, end)
            parameter_lst.append(tmp_parameter_lst)

            new_points = obj.typeJudgement((start[0], start[1]), (middle[0], middle[1]), (end[0], end[1]))
            for i in range(0, len(new_points)):
                points_lst.append((int(new_points[i][0]), int(new_points[i][1])))
        else:
            continue
            
    #TODO: finish the trajectory of tools(line and radian)
    for i in range(-1,2):
        signal1 = isPointOnLine(contents[0][0], contents[0][1], contents[-1][0], contents[-1][1], points_lst[i][0], points_lst[i][1])
        signal2 = isPointOnLine(contents[0][0], contents[0][1], contents[1][0], contents[1][1], points_lst[i][0], points_lst[i][1])
        signal = signal1 or signal2
        if signal:
            del points_lst[0]
            del points_lst[-1]

            del parameter_lst[0]
            del parameter_lst[-1]
            break

    for i in range(0, len(points_lst)):
        if i + 1 == len(points_lst):
            i = -1
        obj.drawToolsLine((int(points_lst[i][0]), int(points_lst[i][1])),(int(points_lst[i + 1][0]), int(points_lst [i + 1][1])))
        # cv.circle(obj.board, points_lst[i], 3, (0,0,255), 2)

if __name__ == '__main__':
    obj = Compansation(offset=8, type=0)
    contents = read("./parameters.txt")

    workPiecesDrawer(obj, contents)
    toolsDrawer(obj, contents)
    cv.imshow("output", obj.board)
    cv.waitKey(0)
    cv.destroyAllWindows()