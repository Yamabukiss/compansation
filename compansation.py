import cv2 as cv
import numpy as np
import math

class Compansation():
    def __init__(self, offset=10, type=0):

        '''
        :param offset: the radius of tools
        :param type:  G41 or G42, G41 for 1 G42 for 0
        '''

        self.offset = offset
        self.type = type
        self.board = np.zeros((500, 500, 3), dtype=np.uint8)
        self.board.fill(255)

    def radian2Degree(self, radian):
        return radian * 180 / math.pi

    def degree2Radian(self, degree):
        return degree * math.pi / 180

    def drawLine(self, p1, p2, color):
        cv.line(self.board, p1, p2, color, 2)

    def angleFromMultiplication(self, p1, p2, center):
        vector1 = (p1[0] - center[0], p1[1] - center[1])
        vector2 = (p2[0] - center[0], p2[1] - center[1])

        degree1 = int(cv.phase(vector1[0], vector1[1], None, True)[0][0])
        degree2 = int(cv.phase(vector2[0], vector2[1], None, True)[0][0])

        degree1 = (degree1 + 360) % 360
        degree2 = (degree2 + 360) % 360
        return [degree1, degree2]

    def drawCircle(self, p1, p2, center, radius, color):
        angle = self.angleFromMultiplication(p1, p2, center)
        cv.ellipse(self.board, center, (radius, radius), 0, angle[0], angle[1], color, 2)

    def drawWorkPiecesLine(self, p1, p2):
        self.drawLine(p1, p2, (255, 0, 0))

    def drawToolsLine(self, p1, p2):
        self.drawLine(p1, p2, (0, 255, 0))

    def drawWorkPiecesCircle(self, p1, p2, center, radius):
        self.drawCircle(p1, p2, center, radius, (255, 0, 0))

    def drawToolsCircle(self, p1, p2, center, radius):
        self.drawCircle(p1, p2, center, radius, (0, 255, 0))

    def calculateL(self, alpha):
        return self.offset / math.tan( alpha / 2)

    def calculateL2(self, vector):
        return math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))

    # def calculateTheta(self, p1, p2, p3):
    #     vector1 = (p2[0] - p1[0], p2[1] - p1[1])
    #     vector2 = (p3[0] - p2[0], p3[1] - p2[1])
    #     vector3 = (p3[0] - p1[0], p3[1] - p1[1])
    #
    #     a = self.calculateL2(vector1)
    #     b = self.calculateL2(vector2)
    #     c = self.calculateL2(vector3)
    #
    #     radian = math.acos( (pow(c,2) - pow(a,2) - pow(b,2)) / (2 * a * b) )
    #     degree = self.radian2Degree(radian)
    #
    #     return degree

    def calculateTheta(self, p1, p2, p3):
        dx1 = p1[0] - p2[0] # notice
        dy1 = p1[1] - p2[1]
        dx2 = p3[0] - p2[0]
        dy2 = p3[1] - p2[1]

        length_ab = math.sqrt(dx1 ** 2 + dy1 ** 2)
        length_bc = math.sqrt(dx2 ** 2 + dy2 ** 2)

        dot_product = dx1 * dx2 + dy1 * dy2

        cos_angle = dot_product / (length_ab * length_bc)

        angle_rad = math.acos(cos_angle)

        angle_deg = math.degrees(angle_rad)

        angle_360 = angle_deg % 360

        return angle_360

    def typeJudgement(self, p1, p2, p3):
        degree = self.calculateTheta(p1, p2, p3)
        new_p1, new_p21, u_vector21 = self.calculateLineCompensationPoint(p1, p2)
        new_p23, new_p3, u_vector32 = self.calculateLineCompensationPoint(p2, p3)

        if self.type:
            degree = 360. - degree

        l = self.calculateL(degree)

        vector1 = (p3[0] - p1[0], p3[1] - p1[1])
        vector2 = (new_p23[0] - new_p21[0], new_p23[1] - new_p21[1])

        dot = vector1[0] * vector2[0] + vector1[1] * vector2[1]

        if dot <= 0:
            l = self.calculateL(360 - degree)
            tmp_p = self.shorteningOperator(new_p21, l, u_vector21)
            return [new_p1, tmp_p, new_p3]
        else:
            if degree < 90:
                tmp_p21, tmp_p23 = self.insertionOperator(new_p21, new_p23, l, u_vector21, u_vector32)
                # return [new_p1, new_p21, tmp_p21, tmp_p23, new_p23, new_p3]
                return [new_p1, tmp_p21, tmp_p23, new_p3]
            else:
                 tmp_p = self.expandingOperator(new_p21, l, u_vector21)
                 return [new_p1,  tmp_p,  new_p3]

    def calculateLineCompensationPoint(self,p1, p2): # returns [p1, p2] after compensation
        x_o, y_o = p1[0], p1[1]
        x_a, y_a = p2[0], p2[1]

        dx = x_a - x_o
        dy = y_a - y_o

        length_oa = math.sqrt(dx ** 2 + dy ** 2)
        u_oa = (dx / length_oa, dy / length_oa)

        if self.type:
            ob = (self.offset * u_oa[1], -self.offset * u_oa[0])
        else:
            ob = (self.offset * (-u_oa[1]), self.offset * u_oa[0])

        x_b = x_a + ob[0]
        y_b = y_a + ob[1]

        x_ob = x_o + ob[0]
        y_ob = y_o + ob[1]

        return [(int(x_ob), int(y_ob)), (int(x_b), int(y_b)), u_oa]

    def insertionOperator(self, new_p21, new_p23, l, u_vector21, u_vector32):
        tmp_p21 = (new_p21[0] + l * u_vector21[0], new_p21[1] + l * u_vector21[1])
        tmp_p23 = (new_p23[0] - l * u_vector32[0], new_p23[1] - l * u_vector32[1])
        return tmp_p21, tmp_p23

    def expandingOperator(self, new_p21, l, u_vector21):
        tmp_p = (new_p21[0] + l * u_vector21[0], new_p21[1] + l * u_vector21[1])
        return tmp_p

    def shorteningOperator(self, new_p21, l, u_vector21):
        tmp_p = (new_p21[0] - l * u_vector21[0], new_p21[1] - l * u_vector21[1])
        return tmp_p
