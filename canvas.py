import pygame 
from conductor import Conductor


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
FPS = 60




class Canvas:
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
        pygame.display.set_caption("conductor")
        self.conductor = Conductor(400, (255,255,255), (CANVAS_WIDTH // 2 - 200, CANVAS_HEIGHT // 2 - 200))
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()




    def render(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with white
        self.conductor.update_positions()
        self.conductor.show(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)

   

    def run(self):
        while self.running:
            self.handle_events()
            self.render()