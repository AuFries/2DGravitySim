import pygame
import math

class Particle: #represents a single particle objeect

    def __init__(self,pos=None,mass=None,particle_number=0):
        self.x = pos[0]
        self.y = pos[1]
        self.radius = mass * 0.9 #radius is dependent on mass
        self.mass = mass
        self.vx = 0 #current velocity in x/y directions
        self.vy = 0
        self.net_f_x = 0 #net force in the x/y directions
        self.net_f_y = 0
        self.theta = 0
        self.ax = 0 #current acceleration in x/y directions
        self.ay = 0
        self.particle_number = particle_number
        self.collision_cooldown = 10 #cooldown is applied after colliding

    def merge(self,other,particle_number): #merges particle 1 and 2 into one larger particle
        if self.mass == other.mass:
            posX = (self.x + other.x) / 2 #midpoint formula to merge the 2 masses
            posY = (self.y + other.y) / 2
        elif self.mass > other.mass:
            posX = self.x
            posY = self.y
        else:
            posX = other.x
            posY = other.y

        merged = Particle((posX,posY),self.mass + other.mass,particle_number)

        merged.radius = math.sqrt(self.radius**2 + other.radius**2) #piR^2 = piR^2 + piR^2

        #calculate new velocity using inelastic collision momentum m1v1x + m2v2x = (m1 + m2)vfx and m1v1y + m2v2y = (m1 + m2)vfy
        merged.vx = ((self.mass * self.vx) + (other.mass * other.vx)) / (self.mass + other.mass)
        merged.vy = ((self.mass * self.vy) + (other.mass * other.vy)) / (self.mass + other.mass)

        return merged

    def __str__(self): #used for debugging
        return f"Particle {self.particle_number}: pX: {self.x} pY: {self.y} \n vX: {self.vx} vY: {self.vy} \n aX: {self.ax} aY: {self.ay} \n fX: {self.net_f_x} fY: {self.net_f_y}"
