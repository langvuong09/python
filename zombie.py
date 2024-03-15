from os import path
import pygame
import sys
from setting import *
from sprite1 import *
from waitting_hall import *
import random
from game_setting import *

condition_mode_zombie = True

class Zombie:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)
        pygame.display.set_caption(TITLE)
        self.data()
        self.running_time = True

    def data(self):
        self.death_time = []
        self.respawn_time = 3
        self.maze = []
        with open(path.join(maze_forder, 'MAZE21.txt'), 'rt') as f:
            for line in f:
                self.maze.append(line)
        self.wall_image = pygame.image.load(path.join(image_folder, WALL_IMAGE)).convert()
        self.bullet_image = pygame.image.load(path.join(image_folder, BULLET_IMAGE)).convert()
        self.bullet_image.set_colorkey(WHITE)

    def run(self):
        self.playing = True
        while self.playing:
            self.changing_time = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def get_setting_coordinates(self):
        settings_x = WIDTH - 75
        settings_y = -20
        return settings_x, settings_y

    def draw(self):
        self.screen.fill(DARK_SEA_GREEN)
        self.all_sprites.draw(self.screen)
        settings_x, settings_y = self.get_setting_coordinates()
        settings = pygame.image.load(r'img\setting.png')
        settings = pygame.transform.scale(settings, (100, 100))
        self.screen.blit(settings, (settings_x, settings_y))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if settings_x <= mouse_pos[0] <= settings_x + 100 and settings_y <= mouse_pos[1] <= settings_y + 100:
                    self.running_time = False
                    global condition_mode_zombie
                    condition_mode_zombie = False
                    import game_setting
                    game_setting.main()

        pygame.display.flip()

    def quit(self):
        pygame.quit()
        quit()

    def grid(self):
        for x in range(0, WIDTH, SQSIZE):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, SQSIZE):
            pygame.draw.line(self.screen, BLACK, (0, y), (WIDTH, y))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        for row, tiles in enumerate(self.maze):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    wall(self, col, row)
                if tile == '*':
                    self.player1 = Player1(self, col, row)
                if tile == '-':
                    self.enemy = Enemy(self, col, row)

    def update(self):
        self.all_sprites.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def mode_zombie(self):
        PLAYER.clear()
        self.new()
        self.run()

def main():
    icon = pygame.image.load(r'img\logo.png')
    pygame.display.set_icon(icon)
    g = Zombie()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g.quit()
        g.events()
        g.mode_zombie()

if __name__ == "__main__":
    main()
