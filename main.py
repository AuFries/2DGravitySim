import pygame
import particle
import simulation

pygame.init()

screen = pygame.display.set_mode((1000,800)) #set screen width and height

pygame.display.set_caption("Gravity Sim") #set window title and icon
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

simulation = simulation.Simulation(screen) #create the simulation object

import time

clock = pygame.time.Clock()
running = True
while running:

    screen.fill((216,216,216))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP: #start the simulation upon a mouse click
            simulation.add_particle(pygame.mouse.get_pos())
            pygame.display.update()

        if event.type == pygame.KEYDOWN: #center the simulation upon a spacebar click
            if event.key == pygame.K_SPACE:
                simulation.follow_massive()

    simulation.compute_forces(0.1) #moves particles in 0.1s increments. Changing this will change the 'speed' of the simulation
    simulation.check_collided()
    simulation.draw_particles()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
