import math

class BasePoint():
    def __init__(self, x = 0, y = 0, rad = 0)
        self.x = x
        self.y = y
        self.rad = rad

    def absolute(self):
        return self.x, self.y, self.rad

class Point():
    def __init__(self, rad = 0, distance = 0, orient = 0, base = None):
        self.rad = rad
        self.distance = distance
        self.orient = orient
        if base is None:
            self.base = BasePoint(0, 0, 0)
        else:
            self.base = base

    def absolute(self):
        x, y, rad = base.absolute()
        rad = rad + self.rad
        x = x + self.distance * math.cos(rad)
        y = y + self.distance * math.sin(rad)
        rad = rad + self.orient
        return x, y, rad

    def rebase(self, base):
        self.base = base

    def relative(self, point):
        abs_x, abs_y, abs_rad = self.absolute()
        ori_x, ori_y, ori_rad = point.absolute()
        rel_x = abs_x - ori_x
        rel_y = abs_y - ori_y
        rel_orient = abs_rad - ori_rad
        rel_rad = math.atan(1.0*rel_x/rel_y)
        distance = math.pow(1.0*(rel_x^2+rel_y^2), 0.5)
        return Point(rel_rad, distance, rel_orient)

    def relative_ab(self, point):
        abs_x, abs_y, abs_rad = self.absolute()
        ori_x, ori_y, ori_rad = point.absolute()
        rel_x = abs_x - ori_x
        rel_y = abs_y - ori_y
        x = 1.0 * rel_x * math.cos(ori_rad) + 1.0 * rel_y * math.sin(ori_rad)
        y = 1.0 * rel_y * math.cos(ori_rad) - 1.0 * rel_x * math.sin(ori_rad)
        rad = abs_rad - ori_rad
        return x, y, rad



class Circle():
    def __init__(self, center, rad):
        self.center = center
        self.rad = rad

    def cross(self, shape):
        if shape is Circle:
            x0, y0, r0 = self.center.absolute()
            x1, y1, r1 = shape.center.absolute()
            return (x1-x0)^2 + (y1-y0)^2 < self.rad^2 + shape.rad^2
        else:
            return shape.cross(self)

class Line():
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2