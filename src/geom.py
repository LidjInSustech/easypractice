import math

class BasePoint():
    def __init__(self, x = 0, y = 0, rad = 0)
        self.x = x
        self.y = y
        self.rad = rad

    def absolute(self):
        return self.x, self.y, self.rad

    def relative_ab(self):
        ori_x, ori_y, ori_rad = point.absolute()
        rel_x = self.x - ori_x
        rel_y = self.y - ori_y
        x = 1.0 * rel_x * math.cos(ori_rad) + 1.0 * rel_y * math.sin(ori_rad)
        y = 1.0 * rel_y * math.cos(ori_rad) - 1.0 * rel_x * math.sin(ori_rad)
        rad = self.rad - ori_rad
        return x, y, rad

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


class Shape():
    def cross(self):
        return False

class Circle(Shape):
    def __init__(self, center, rad):
        self.center = center
        self.rad = rad

    def cross(self, shape):
        if isinstance(shape, Circle):
            x0, y0, r0 = self.center.absolute()
            x1, y1, r1 = shape.center.absolute()
            return (x1-x0)^2 + (y1-y0)^2 < (self.rad+shape.rad)^2
        else:
            return shape.cross(self)

    def in(self, point):
        x, y, r = point.relative_ab(self.center)
        return x^2 + y^2 < self.rad^2

class Line(Shape):
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
    
    def cross(self, shape):
        if isinstance(shape, Line):
            x0, y0, r = self.point2.relative_ab(self.point1)
            x1, y1, r = shape.point1.relative_ab(self.point1)
            dx, dy, r = shape.point2.relative_ab(shape.point1)
            if dx*y0 == dy*x0:
                return False
            else:
                if x0 != 0:
                    mesure = x1 + dx*(dy*x0-dx*y0)/(y0*x1-x0*y1)
                    if x0 > 0:
                        return (0<mesure & mesure<x0)
                    else:
                        return (x0<mesure & mesure<0)
                else:
                    mesure = y1 + dy*(dy*x0-dx*y0)/(y0*x1-x0*y1)
                    if y0 > 0:
                        return (0<mesure & mesure<y0)
                    else:
                        return (y0<mesure & mesure<0)
        elif isinstance(shape, Circle):
            if shape.in(self.point1):
                return True
            if shape.in(self.point2):
                return True
            x0, y0, r = self.point1.relative_ab(shape.center)
            x1, y1, r = self.point2.relative_ab(shape.center)
            dx = x1 - x0
            dy = y1 - y0
            return - (x0*dx + y0*dy) < dx^2 + dy^2
        else:
            return shape.cross(self)

class Triangle(Shape):
    def __init__(self, point1, point2, point3):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3