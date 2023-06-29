import math

class BasePoint():
    def __init__(self, x = 0, y = 0, rad = 0):
        self.x = x
        self.y = y
        self.rad = rad

    def absolute(self):
        return self.x, self.y, self.rad

    def relative_ab(self, point):
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
        x, y, rad = self.base.absolute()
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
    
    def square(self):
        return None, None

class Circle(Shape):
    def __init__(self, center, rad):
        self.center = center
        self.rad = rad

    def square(self):
        x, y, rad = self.center.absolute()
        return (x-self.rad, y-self.rad), (x+self.rad, y+self.rad)

    def cross(self, shape):
        if isinstance(shape, Circle):
            x0, y0, r0 = self.center.absolute()
            x1, y1, r1 = shape.center.absolute()
            return (x1-x0)^2 + (y1-y0)^2 < (self.rad+shape.rad)^2
        else:
            return shape.cross(self)

    def point_in(self, point):
        x, y, r = point.relative_ab(self.center)
        return x^2 + y^2 < self.rad^2

class Line(Shape):
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def square(self):
        x0, y0, r = self.point1.absolute()
        x1, y1, r = self.point2.absolute()
        if x0 < x1:
            x_min = x0
            x_max = x1
        else:
            x_min = x1
            x_max = x0
        if y0 < y1:
            y_min = y0
            y_max = y1
        else:
            y_min = y1
            y_max = y0
        return (x_min, y_min), (x_max, y_max)
    
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
            if shape.point_in(self.point1):
                return True
            if shape.point_in(self.point2):
                return True
            x0, y0, r = self.point1.relative_ab(shape.center)
            x1, y1, r = self.point2.relative_ab(shape.center)
            dx = x1 - x0
            dy = y1 - y0
            return - (x0*dx + y0*dy) < dx^2 + dy^2
        else:
            return shape.cross(self)

class Polygon(Shape):
    def __init__(self, pointlist):
        self.pointlist = pointlist

    def center(self):
        x = 0
        y = 0
        for point in self.pointlist:
            x += point.x
            y += point.y
        return x/len(self.pointlist), y/len(self.pointlist)

    def point_in(self, point):
        point = BasePoint(*point.absolute())
        pointlist = [BasePoint(*point.absolute()) for point in self.pointlist]
        values = []
        for i in range(len(self.pointlist)):
            vec1 = (pointlist[i].x - point.x, pointlist[i].y - point.y)
            vec2 = (pointlist[i-1].x - pointlist[i].x, pointlist[i-1].y - pointlist[i].y)
            values.append(vec1[0]*vec2[1] - vec1[1]*vec2[0])
        if all([value > 0 for value in values]) or all([value < 0 for value in values]):
            return True
        else:
            return False

    def square(self):
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0
        for i in range(len(self.pointlist)):
            x, y, r = self.pointlist[i].absolute()
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y
        return (x_min, y_min), (x_max, y_max)

    def cross(self, shape):
        square_min, square_max = self.square()
        square_min1, square_max1 = shape.square()
        if square_min[0] > square_max1[0] or square_min1[0] > square_max[0]:
            return False
        if square_min[1] > square_max1[1] or square_min1[1] > square_max[1]:
            return False
        if isinstance(shape, Circle):
            for i in range(len(self.pointlist)):
                if shape.point_in(self.pointlist[i]):
                    return True
            for i in range(len(self.pointlist)):
                line = Line(self.pointlist[i-1], self.pointlist[i])
                if line.cross(shape):
                    return True
            if self.point_in(shape.center):
                return True
            return False
        elif isinstance(shape, Line):
            for i in range(len(self.pointlist)):
                line = Line(self.pointlist[i-1], self.pointlist[i])
                if line.cross(shape):
                    return True
            return False
        elif isinstance(shape, Polygon):
            center = BasePoint(*self.center())
            if shape.point_in(center):
                return True
            for i in range(len(self.pointlist)):
                for j in range(len(shape.pointlist)):
                    line = Line(self.pointlist[i-1], self.pointlist[i])
                    if line.cross(Line(shape.pointlist[j-1], shape.pointlist[j])):
                        return True
            return False
        else:
            return shape.cross(self)
        
class Sector(Shape):
    def __init__(self, point, rad, angle1, angle2):
        self.point = point
        self.rad = rad
        self.angle1 = angle1
        self.angle2 = angle2

    def lines(self):
        x, y, r = self.point.absolute()
        x1 = x + self.rad*math.cos(self.angle1)
        y1 = y + self.rad*math.sin(self.angle1)
        x2 = x + self.rad*math.cos(self.angle2)
        y2 = y + self.rad*math.sin(self.angle2)
        return Line(self.point, BasePoint(x1, y1)), Line(self.point, BasePoint(x2, y2))

    def point_in(self, point):
        x, y, r = point.absolute()
        if x^2 + y^2 > self.rad^2:
            return False
        angle = math.atan2(y-self.point.absolute()[1], x-self.point.absolute()[0])
        if self.angle1 < self.angle2:
            if self.angle1 < angle & angle < self.angle2:
                return True
            else:
                return False
        else:
            if self.angle1 < angle | angle < self.angle2:
                return True
            else:
                return False
            
    def square(self):
        x, y, r = self.point.absolute()
        x_min = x - self.rad
        x_max = x + self.rad
        y_min = y - self.rad
        y_max = y + self.rad
        return (x_min, y_min), (x_max, y_max)
    
    def cross(self, shape):
        square_min, square_max = self.square()
        square_min1, square_max1 = shape.square()
        if square_min[0] > square_max1[0] or square_min1[0] > square_max[0]:
            return False
        if square_min[1] > square_max1[1] or square_min1[1] > square_max[1]:
            return False
        if isinstance(shape, Circle):
            line1, line2 = self.lines()
            if line1.cross(shape):
                return True
            if line2.cross(shape):
                return True
            if not shape.cross(Circle(self.point, self.rad)):
                return False
            x, y, r = shape.center.absolute()
            angle = math.atan2(y-self.point.absolute()[1], x-self.point.absolute()[0])
            if self.angle1 < self.angle2:
                if self.angle1 < angle & angle < self.angle2:
                    return True
                else:
                    return False
            else:
                if self.angle1 < angle | angle < self.angle2:
                    return True
                else:
                    return False
        elif isinstance(shape, Line):
            line1, line2 = self.lines()
            if line1.cross(shape):
                return True
            if line2.cross(shape):
                return True
            if self.point_in(shape.point1) | self.point_in(shape.point2):
                return True
            return False
        elif isinstance(shape, Polygon):
            line1, line2 = self.lines()
            for i in range(len(shape.pointlist)):
                if self.point_in(shape.pointlist[i]):
                    return True
                if line1.cross(Line(shape.pointlist[i-1], shape.pointlist[i])):
                    return True
                if line2.cross(Line(shape.pointlist[i-1], shape.pointlist[i])):
                    return True
                
            