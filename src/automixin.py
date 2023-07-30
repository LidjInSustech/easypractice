import pygame as pg
import random

class Chemotaxis():
    def free(self):
        thoughts = ['forward', 'turn_left', 'turn_right']
        if getattr(self, 'thought', None) is None:
            self.thought = 0
        match thoughts[self.thought]:
            case 'forward':
                self.move()
            case 'turn_left':
                self.orientation += 3
            case 'turn_right':
                self.orientation -= 3
            case _:
                self.thought = random.randint(0,2)
        limit = 0.02
        result = random.random()
        if result < limit/2:
            self.thought = (self.thought + 1) % 3
        elif result < limit:
            self.thought = (self.thought + 2) % 3

class Navigated():
    def navigate(self, destination):
        vector = destination - self.loc
        length, angle = vector.as_polar()
        angle = (angle - self.orientation) % 360
        turn = self.properties['turn']
        if angle < 180 and angle > turn:
            self.orientation += turn
        elif angle >= 180 and angle < 360 - turn:
            self.orientation -= turn
        else:
            self.move()

class RandomDestination(Navigated):
    def free(self):
        if getattr(self, 'destination', None) is None:
            self.destination = self.new_destination()
        if self.loc.distance_to(self.destination) < 10:
            self.destination = self.new_destination()
        self.navigate(self.destination)
    
    def new_destination(self):
        boundary = self.controller.boundary
        return pg.math.Vector2(random.randint(-boundary.x, boundary.x), random.randint(-boundary.y, boundary.y))

class Patrol(RandomDestination):
    def set_path(self, points):
        self.path = points
        self.point = 0

    def new_destination(self):
        if getattr(self, 'path', None) is None:
            raise Exception('Please set path first')
        destination =  self.path[self.point]
        self.point = (self.point + 1) % len(self.path)
        return destination
        