from os import path
import pygame
import sys
from setting import *
from sprites import *
from waitting_hall import *
import random
from game_setting import *

condition_mode_training = True
condition_mode_1v1 = True
condition_mode_1v1_of_restart = True
condition_mode_training_of_restart = True
ĐK = True

class Game:
    def __init__(self):
        pygame.init()  # khởi tạo pygame
        # pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)
        pygame.display.set_caption(TITLE)
        self.data()

        self.running = True  # Trạng thái hoạt động của module player

    def data(self):
        self.death_time = []  # danh sách thời gian chết
        self.respawn_time = 3  # delay hồi sinh là 3 giây
        self.maze = []  # ma trận
        # i=random.randint(1,5)
        with open(path.join(maze_forder, 'MAZE1.txt'),
                  'rt') as f:  # cái này sửa lại tất cả file ma trận thành 24 dòng 32 cột rồi làm thành random , giờ demo thì lấy lại MAZE1.txt tại sửa file đó rồi
            for line in f:
                self.maze.append(line)
        # self.maze.append()
        self.wall_image = pygame.image.load(path.join(image_folder, WALL_IMAGE)).convert()  # lấy hình tường
        self.bullet_image = pygame.image.load(path.join(image_folder, BULLET_IMAGE)).convert()  # lấy hình đạn
        self.bullet_image.set_colorkey(WHITE)
        self.mode = 1  # chế độ game 1 là 1v1, 2 là training

    def run(self):  # hàm này để chạy các chế độ game
        self.playing = True
        while self.playing:
            self.changing_time = self.clock.tick(FPS) / 1000  # tính thời gian trôi qua kể từ khung hình trước(giây)
            self.auto_respawn()  # hàm auto hồi sinh
            # if self.events_enabled:  # Kiểm tra trạng thái của biến boolean
            self.events()  # Xử lý sự kiện khi biến là True
            self.update()  # hàm này gọi tất cả hàm update của các sprites
            self.draw()  # hàm này vẽ tất cả sprites


    def get_setting_coordinates(self):
        # Tính toán tọa độ của hình ảnh setting
        settings_x = WIDTH - 75
        settings_y = -20
        return settings_x, settings_y

    def draw(self):
        self.screen.fill(DARK_SEA_GREEN)
        # self.grid()
        self.all_sprites.draw(self.screen)
        # Hiển thị hình ảnh setting
        settings_x, settings_y = self.get_setting_coordinates()
        settings = pygame.image.load(r'img\setting.png')
        settings = pygame.transform.scale(settings, (100, 100))  # Chỉnh kích thước hình ảnh nếu cần
        self.screen.blit(settings, (settings_x, settings_y))  # Hiển thị ở góc trên cùng bên phải

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if settings_x <= mouse_pos[0] <= settings_x + 100 and settings_y <= mouse_pos[1] <= settings_y + 100:
                    self.running = False  # Tạm dừng sự kiện của module player
                    global condition_mode_1v1_of_restart,condition_mode_training_of_restart
                    if not condition_mode_1v1:
                        condition_mode_1v1_of_restart = False
                    if not condition_mode_training:
                        condition_mode_training_of_restart = False
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

    def new(self):  # hàm khởi lại tất cả nhóm sprites và các đối tượng
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        for row, tiles in enumerate(self.maze):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    wall(self, col, row)
                if tile == '*':
                    self.player1 = Player1(self, col, row)
                if tile == '-' and self.mode == 1:
                    self.player2 = Player2(self, col, row)
                if tile == '-' and self.mode == 2:
                    self.enemy = enemy(self, col, row)

    def update(self):
        self.all_sprites.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def auto_respawn(self):
        if self.mode == 2:
            pos_respawn = []
            for row, tiles in enumerate(self.maze):
                for col, tile in enumerate(tiles):
                    if tile != '1' and tile != '\n':
                        pos_respawn.append((col, row))
            if not PLAYER:
                current_time = time.time()
                death_time = self.death_time[0]
                if current_time - death_time >= self.respawn_time:
                    pos_respawn_random = random.choice(pos_respawn)
                    self.player1 = Player1(self, pos_respawn_random[0], pos_respawn_random[1])
                    self.death_time.remove(death_time)
            if not ENEMY:
                current_time = time.time()
                death_time = self.death_time[0]
                if current_time - death_time >= self.respawn_time:
                    pos_respawn_random = random.choice(pos_respawn)
                    self.enemy = enemy(self, pos_respawn_random[0], pos_respawn_random[1])
                    self.death_time.remove(death_time)

    def keys(self,button1,button2):  # hàm này dùng để demo thôi , khi ấn nút 1 thì mode 1v1 ,2 thì mode training, sau sẽ thay bằng hàm ấn các button trên UI để vào các chế độ
        global condition_mode_training, condition_mode_1v1  # Thêm dòng này để sử dụng biến toàn cục
        mouse_pos = pygame.mouse.get_pos()
        if button1.x <= mouse_pos[0] <= button1.x + button1.width and button1.y <= mouse_pos[1] <= button1.y + button1.height:
            condition_mode_training = False
            self.mode = 2
            self.mode_training()
        if button2.x <= mouse_pos[0] <= button2.x + button2.width and button2.y <= mouse_pos[1] <= button2.y + button2.height:
            condition_mode_1v1 = False
            self.mode = 1
            self.mode_1v1()

    def mode_1v1(self):  # chế độ 1v1
        PLAYER.clear()
        ENEMY.clear()
        self.new()
        self.run()

    def mode_training(self):  # chế độ training (enemy AI)
        PLAYER.clear()
        ENEMY.clear()
        self.new()
        self.run()

def main(button1, button2):
    icon = pygame.image.load(r'img\logo.png')
    pygame.display.set_icon(icon)

    g = Game()
    while True:
        for event in pygame.event.get():  # Kiểm tra tất cả các sự kiện
            if event.type == pygame.QUIT:  # Nếu nhấn nút đóng cửa sổ
                g.quit()  # Gọi hàm quit để kết thúc game
        g.events()  # Xử lý các sự kiện khác
        g.keys(button1, button2)  # Xử lý các sự kiện từ các nút trên giao diện

if __name__ == "__main__":
    main()