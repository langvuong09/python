import pygame
import sys
import random
import time
from os import path
from setting import *
from sprite1 import *
import sprite1
from waitting_hall import *
from game_setting import *
import setting

condition_mode_zombie = True
condition_mode_zombie_of_restart = True

class Zombie:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)
        pygame.display.set_caption(TITLE)
        self.data()
        self.running_time = True
        # enemy
        self.last_enemy_spawn_time = pygame.time.get_ticks()  # Thời điểm tạo ra Enemy cuối cùng
        self.spawn_interval = 10  # Thời gian giữa mỗi lần xuất hiện enemy (10 giây)
        self.time_since_last_spawn = 0  # Thời gian kể từ lần xuất hiện enemy cuối cùng
        self.time_elapsed = 0  # Thời gian đã trôi qua
        # boss
        self.last_boss_spawn_time = pygame.time.get_ticks()  # Thời điểm tạo ra Boss cuối cùng
        self.spawn_interval_boss = 30  # Thời gian giữa mỗi lần xuất hiện boss (30 giây)
        self.time_since_last_spawn_boss = 0  # Thời gian kể từ lần xuất hiện boss cuối cùng
        self.time_elapsed_boss = 0  # Thời gian đã trôi qua
        self.call_boss_delay = 30  # Thời gian trì hoãn trước khi gọi Boss

    def data(self):
        self.death_time = []
        self.respawn_time = 2
        self.maze = []
        with open(path.join(maze_forder, 'MAZE21.txt'), 'rt') as f: # tọa độ bản đò
            for line in f:
                self.maze.append(line.strip())
        self.wall_image = pygame.image.load(path.join(image_folder, WALL_IMAGE)).convert()
        self.bullet_image = pygame.image.load(path.join(image_folder, BULLET_IMAGE)).convert()
        self.bullet_image.set_colorkey(WHITE)
        self.mode_z = 1

    def run(self):
        self.playing = True
        while self.playing:
            self.changing_time = self.clock.tick(FPS) / 1000
            self.time_elapsed += self.changing_time
            self.auto_respawn_zombie()  # hàm auto hồi sinh zombie
            self.auto_respawn_boss()  # Gọi Boss
            self.events()
            self.update()
            self.draw()
            # Cập nhật spawn_interval sau mỗi khoảng thời gian nhất định của enemy
            if self.spawn_interval >= 7:
                if self.time_elapsed >=10:  # Cập nhật sau mỗi 10 giây
                    self.spawn_interval -= 1  # Giảm spawn_interval đi 1 giây
                    self.time_elapsed = 0  # Reset lại thời gian đã trôi qua
            elif self.spawn_interval >= 2:
                if self.time_elapsed >=18:
                    self.spawn_interval -= 1
                    self.time_elapsed = 0
            elif self.spawn_interval == 1:
                if self.time_elapsed >= 30:
                    self.spawn_interval -= 0.5
                    self.time_elapsed = 0
            else:
                self.spawn_interval = 0.5
            # Cập nhật spawn_interval sau mỗi khoảng thời gian nhất định của boss
            if self.spawn_interval_boss >= 20:
                if self.time_elapsed_boss >= 30:  # Cập nhật sau mỗi 15 giây
                    self.spawn_interval_boss -= 3  # Giảm spawn_interval_boss đi 3 giây
                    self.time_elapsed_boss = 0  # Reset lại thời gian đã trôi qua
            elif self.spawn_interval_boss >= 10:
                if self.time_elapsed_boss >= 8:
                    self.spawn_interval_boss -= 4
                    self.time_elapsed_boss = 0
            else:
                self.spawn_interval_boss = 3

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

        # Vẽ dòng chữ "Kill" ở trên cùng và giữa màn hình
        font = pygame.font.Font(None, 30)  # Chọn font và kích cỡ
        text = font.render("Kill: " + str(setting.number_kill), True, BLACK)  # Tạo đối tượng văn bản
        text_rect = text.get_rect(center=((WIDTH // 2) + 350, 20))  # Đặt vị trí của văn bản
        self.screen.blit(text, text_rect)  # Vẽ văn bản lên màn hình

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if settings_x <= mouse_pos[0] <= settings_x + 100 and settings_y <= mouse_pos[1] <= settings_y + 100:
                    self.running_time = False
                    global condition_mode_zombie_of_restart
                    condition_mode_zombie_of_restart = False
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
                    self.player1 = sprite1.Player1(self, col, row)
                if tile == '-':
                    self.enemy = sprite1.Enemy(self, col, row)
                if tile == '.' and self.time_elapsed_boss >= self.call_boss_delay:
                    self.boss = sprite1.Boss(self, col, row)

    def update(self):
        self.all_sprites.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def auto_respawn_zombie(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn_time >= self.spawn_interval * 1000:
            pos_respawn = []
            for row, tiles in enumerate(self.maze):
                for col, tile in enumerate(tiles):
                    if tile == '?':  # Thay đổi điều kiện để chỉ chọn các vị trí có dấu '-'
                        pos_respawn.append((col, row))
            if pos_respawn:  # Kiểm tra xem danh sách pos_respawn có phần tử nào hay không
                pos_respawn_random = random.choice(pos_respawn)
                self.enemy = sprite1.Enemy(self, pos_respawn_random[0], pos_respawn_random[1])  # Tạo một đối tượng Enemy mới
                self.all_sprites.add(self.enemy)  # Thêm enemy vào nhóm sprite
                self.last_enemy_spawn_time = current_time  # Cập nhật thời điểm cuối cùng mà enemy đã được tạo

    def auto_respawn_boss(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_boss_spawn_time >= self.spawn_interval_boss * 1000:
            pos_respawn = []
            for row, tiles in enumerate(self.maze):
                for col, tile in enumerate(tiles):
                    if tile == '?':  # Thay đổi điều kiện để chỉ chọn các vị trí có dấu '-'
                        pos_respawn.append((col, row))
            if pos_respawn:  # Kiểm tra xem danh sách pos_respawn có phần tử nào hay không
                pos_respawn_random = random.choice(pos_respawn)
                self.boss = sprite1.Boss(self, pos_respawn_random[0], pos_respawn_random[1])  # Tạo một đối tượng Boss mới
                self.all_sprites.add(self.boss)  # Thêm Boss vào nhóm sprite
                self.last_boss_spawn_time = current_time  # Cập nhật thời điểm cuối cùng mà boss đã được tạo

    def mode_zombie(self):
        sprite1.PLAYER.clear()
        sprite1.ENEMY.clear()
        sprite1.BOSS.clear()
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
