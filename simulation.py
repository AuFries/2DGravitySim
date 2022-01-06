import pygame
import particle as p
import math
import random

class Simulation:

    def __init__(self,screen):
        self.particle_list = []
        self.screen = screen
        self.num_particles = 0
        self.massive = None #the current most massive particle

    def add_particle(self,pos): #randomly adds 50 particles to the screen. Removes them if there are already particles on the screen.
        if self.num_particles != 0:
            self.particle_list.clear()
            self.num_particles = 0
        else:
            for _ in range(50):
                xPos = random.uniform(0,1000)
                yPos = random.uniform(0,800)
                new_particle = p.Particle((xPos,yPos),random.uniform(1,10),self.num_particles) #1, 10 for mass
                new_particle.vx = random.uniform(-5,5)
                new_particle.vy = random.uniform(-5,5)

                self.num_particles += 1
                self.particle_list.append(new_particle)

    def draw_particles(self):
        if len(self.particle_list) > 0:
            largest = self.particle_list[0] #black particle is always most massive

        for p in self.particle_list:
            if p.mass > largest.mass:
                largest = p

        for p in self.particle_list:
            if p == largest:
                pygame.draw.circle(self.screen,(0,0,0),(p.x,p.y),p.radius) #screen, color, center, radius
                self.massive = largest
            else:
                pygame.draw.circle(self.screen,(255,0,0),(p.x,p.y),p.radius)

    def compute_forces(self,time): #bulk of simulation, calculates and updates all the forces on each particle
        for p1 in self.particle_list: #computing net force
            p1.net_f_x = 0
            p1.net_f_y = 0
            for p2 in self.particle_list:
                if p1 != p2: #ignore itself when computing gravity
                    x_dist = p2.x-p1.x
                    y_dist = p2.y-p1.y

                    theta = math.atan2(y_dist,x_dist) #using trig to compute direction angle
                    distance = math.sqrt(x_dist**2 + y_dist**2) #pythag theorem

                    # use F = G * ((m1*m2)/r)
                    p1.net_f_x += ((p1.mass*p2.mass)/distance) * math.cos(theta)
                    p1.net_f_y += ((p1.mass*p2.mass)/distance) * math.sin(theta)


        for p in self.particle_list: #computes theta and acceleration based on updated forces
            p.ax = p.net_f_x / p.mass #F = ma
            p.ay = p.net_f_y / p.mass

        self.compute_new_positions(time)


    def compute_new_positions(self,time): #computes and updates all the new positions of particles
        for p in self.particle_list:
            p.x = p.x + p.vx * time + 0.5 * p.ax * (time**2)
            p.y = p.y + p.vy * time + 0.5 * p.ay * (time**2)
            p.vx = p.vx + p.ax * time
            p.vy = p.vy + p.ay * time


    def check_collided(self): #checks whether any particle has collided with another. If so, they are merged.
        for p1 in self.particle_list:
            if p1.collision_cooldown < 10: #increment cooldown for 10 iterations
                p1.collision_cooldown += 1

            for p2 in self.particle_list:
                if p1 != p2 and (p1 in self.particle_list) and (p2 in self.particle_list):
                    distSq = (p2.x - p1.x)**2 + (p2.y - p1.y)**2
                    radSumSq = (p1.radius + p2.radius)**2

                    if distSq <= radSumSq and p1.collision_cooldown == 10 and p2.collision_cooldown == 10: #if the distance from the center is within 20% of the radius, merge them
                        self.particle_list.append(p1.merge(p2,self.num_particles))
                        self.particle_list.remove(p1)
                        self.particle_list.remove(p2)


    def follow_massive(self): #follows the most massive particle by shifting all other particles on the screen
        shift_x = 500 - self.massive.x
        shift_y = 400 - self.massive.y
        self.massive.x = 500
        self.massive.y = 400

        for particle in self.particle_list:
            if particle != self.massive:
                particle.x += shift_x
                particle.y += shift_y
