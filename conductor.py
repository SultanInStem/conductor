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
        self.q_electron = -1

        ### Initializing an array of protons
        x, y = np.meshgrid(np.arange(self.n_side) * lattice_spacing, np.arange(self.n_side) * lattice_spacing)
        self.protons = np.column_stack([x.ravel(), y.ravel()]) 
        ### Initital positions of electrons are near their respective protons with a small offset 
        self.electrons = []
    def show(self, screen): 
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.size, self.size), 1)