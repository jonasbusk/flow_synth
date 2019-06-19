import pygame

from .base import Module


class Keyboard(Module):

    def __init__(self, update_frequency=0.01):
        self.update_frequency = update_frequency
        self.last_update = 0

        # defaults
        self.octave = 5
        self.key = None
        self.quit = False

        pygame.init()

    def terminate(self):
        pygame.quit()

    def out(self, t):
        self.update(t)
        if self.key is not None:
            return 12 * self.octave + self.key
        else:
            return None

    def trigger(self, t):
        self.update(t)
        if self.key is not None:
            return True
        else:
            return False

    def update(self, t):
        # check if already updated recently
        if t - self.last_update < self.update_frequency:
            return
        self.last_update = t

        # update
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        # events
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.quit = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                self.octave += 1
            if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                self.octave -= 1
        # key
        self.key = None
        if keys[pygame.K_a]:
            self.key = 0
        if keys[pygame.K_w]:
            self.key = 1
        if keys[pygame.K_s]:
            self.key = 2
        if keys[pygame.K_e]:
            self.key = 3
        if keys[pygame.K_d]:
            self.key = 4
        if keys[pygame.K_f]:
            self.key = 5
        if keys[pygame.K_t]:
            self.key = 6
        if keys[pygame.K_g]:
            self.key = 7
        if keys[pygame.K_y]:
            self.key = 8
        if keys[pygame.K_h]:
            self.key = 9
        if keys[pygame.K_u]:
            self.key = 10
        if keys[pygame.K_j]:
            self.key = 11
        if keys[pygame.K_k]:
            self.key = 12
