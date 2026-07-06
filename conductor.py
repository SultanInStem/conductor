import pygame
import numpy as np 
import math
import random

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
        self.K = 1 # Couloumb's constant 
        self.eta = 10 # convergence rate in the gradient descent (to be tuned by trial and error)

        self.softening = 0.1 # prevents division by zero in Couloumb's law

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


    def calculate_total_force(self):
        # Force from protons on each electron
        diff_ep = self.electrons[:, None, :] - self.protons[None, :, :]      # (N_e, N_p, 2)
        dist2_ep = (diff_ep ** 2).sum(axis=-1) + self.softening ** 2
        dist_cubed_ep = dist2_ep ** 1.5
        force_ep = self.K * self.q_proton * self.q_electron * diff_ep / dist_cubed_ep[..., None]
        force_from_protons = force_ep.sum(axis=1)                            # (N_e, 2)

        # Force from other electrons on each electron
        diff_ee = self.electrons[:, None, :] - self.electrons[None, :, :]     # (N_e, N_e, 2)
        dist2_ee = (diff_ee ** 2).sum(axis=-1) + self.softening ** 2
        dist_cubed_ee = dist2_ee ** 1.5
        force_ee = self.K * self.q_electron ** 2 * diff_ee / dist_cubed_ee[..., None]

        N_e = self.electrons.shape[0]
        force_ee[np.arange(N_e), np.arange(N_e), :] = 0.0                    # zero self-interaction

        force_from_electrons = force_ee.sum(axis=1)

        return force_from_protons + force_from_electrons


    def update_positions(self): 
        force = self.calculate_total_force()
        new_positions = self.electrons + force * self.eta
        new_positions[:, 0] = np.clip(new_positions[:, 0], self.pos[0], self.pos[0] + self.size)
        new_positions[:, 1] = np.clip(new_positions[:, 1], self.pos[1], self.pos[1] + self.size)
        self.electrons = new_positions
        

    def measure_electric_field(self): 
        n = 30 # number of test points inside and outside 


        ### computing mean electric field inside
        grid_size = 0.5 * self.size # 70 percent of the conductor size 
        low = self.pos[0] + (self.size - grid_size) // 2
        high = low + grid_size

        points_inside = -low + (high - (-low)) * np.random.rand(n, 2)
        E_x = 0 
        E_y = 0

        charge_pos = np.vstack([self.electrons, self.protons])
        charge_q   = np.concatenate([
            np.full(len(self.electrons), self.q_electron),
            np.full(len(self.protons), self.q_proton)
        ])  
        points = np.array(points_inside)
        dx = points[:, 0:1] - charge_pos[:, 0][None, :]    # points_x - charge_x
        dy = points[:, 1:2] - charge_pos[:, 1][None, :]
        dist_cubed = (dx**2 + dy**2 + self.softening**2) ** 1.5

        Ex_matrix = self.K * charge_q[None, :] * (dx) / dist_cubed   # shape (P, N)
        Ey_matrix = self.K * charge_q[None, :] * (dy) / dist_cubed

        E_x = Ex_matrix.sum()   # sum over all points AND all charges
        E_y = Ey_matrix.sum()
        avg_E_inside = np.sqrt(E_x**2 + E_y**2) / n
        print(avg_E_inside)


        ### computing electric field just outside the conductor 

        padding = 10 # perpendicular distance from the boundary 
        points_outside = []
        i = 0
        
               
        return 1
    