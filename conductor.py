import pygame
import numpy as np 

class Conductor: 
    def __init__(self, size, color, pos, lattice_spacing = 10):
        self.pos = pos
        self.size = size
        self.color = color
        self.lattice_spacing = lattice_spacing
        self.n_side = size // lattice_spacing
        self.q_proton = +1
        self.proton_radius = 2
        self.q_electron = -1

        ### Initializing an array of protons
        x, y = np.meshgrid(np.arange(self.n_side) * lattice_spacing + pos[0] + self.proton_radius, np.arange(self.n_side) * lattice_spacing + pos[1] + self.proton_radius)
        self.protons = np.column_stack([x.ravel(), y.ravel()]) 
        ### Initital positions of electrons are near their respective protons with a small random offset 
        self.electrons = self.protons + np.random.uniform(-1, 1, self.protons.shape)

    def show(self, screen): 
        for i in range(0, len(self.protons)): 
            x,y = self.protons[i]
            pygame.draw.circle(screen, (255, 50, 50), (x,y), self.proton_radius)
            x,y = self.electrons[i]
            pygame.draw.circle(screen, (50, 50, 255), (x,y), 1)
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.size, self.size), 1)