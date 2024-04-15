import random
import pygame

from Button import button_setting
from auto_respawn import *
from gameOverGUI import gameOverGUI
from pauseGUI import pauseGUI
from setting import *
from show_kill import show_kill
from sprites import *


class game:
    def __init__(self,screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)
        pygame.display.set_caption(TITLE)
        self.data()
        self.AddedItems()

    def data(self):
        self.maze = []  # ma trận
        i=random.randint(1,5) # chọn ngẫu nhiên 1 trong 5 ma trận 
        with open(path.join(maze_forder, 'MAZE{}.txt'.format(i)),'rt') as f:  # đọc ma trận từ file
            for line in f:
                self.maze.append(line.strip())
        self.pausing = False
        self.playing = True
        self.respawn = auto_respawn_tank(self, 3)

    def AddedItems(self): #thêm giao diện vào game
        self.btn_setting=button_setting(self.screen, WIDTH - 75, -20, 100, 100)
        self.pause_screen = pauseGUI(self.screen)
        self.show_kill_player1 = show_kill(self.screen, "left") 
    
    def run(self):  # hàm này để chạy các chế độ game
        self.playing = True
        while self.playing:
            self.pausing=False
            while self.pausing == False:
                self.changing_time = self.clock.tick(FPS) / 1000 # tính thời gian trôi qua kể từ lần gọi cuối cùng(giây)
                self.events()  
                self.update()  # hàm này gọi tất cả hàm update của các sprites
                self.update_draw()
                self.auto_respawn()
                self.pause_game()
                

    def pause_game(self): #hàm dừng game
        if self.pausing == True: #nếu bấm nút setting thì dừng game
            self.pause_screen.run() #hiển thị màn hình pause
            self.clock.tick(FPS) #đặt lại thời gian
            self.check_pause_events(self.pause_screen) #kiểm tra sự kiện của màn hình pause

    def auto_respawn(self):
        pass

    def new(self):  # hàm khởi tạo lại tất cả nhóm sprites và các đối tượng, chỉ số
        PLAYER.clear() #xóa tất cả các player
        ENEMY.clear() #xóa tất cả các enemy
        GameStatistics.reset_kill() #reset lại số lần giết
        GameStatistics.reset_death_time() #reset lại thời gian chết
        GameStatistics.reset_bullet() #reset thuộc tính đạn
        self.all_sprites = pygame.sprite.Group() #tạo nhóm tất cả các sprites
        self.bullets = pygame.sprite.Group() #tạo nhóm đạn
        self.walls = pygame.sprite.Group()  # tạo nhóm tường
   
    def draw(self): #vẽ các đối tượng lên màn hình
        self.screen.fill(DARK_SEA_GREEN) #tô màu màn hình
        self.all_sprites.draw(self.screen) #vẽ tất cả các sprites
        self.btn_setting.draw() #vẽ nút setting
        self.show_kill_player1.draw(GameStatistics.number_kill_player1,BLUE) #vẽ số lần giết của player1

    def update_draw(self): #cập nhật và vẽ các đối tượng
        self.draw() 
        pygame.display.flip() #cập nhật màn hình

    def update(self): #cập nhật tất cả các sprites
        self.all_sprites.update()

    def check_pause_events(self,pause_screen): #kiểm tra sự kiện của màn hình pause
        if pause_screen == None or pause_screen.action == None: 
            return
        if pause_screen.action == 1: #tiếp tục
            return
        if pause_screen.action == 0: #thoát
            self.playing = False
        if pause_screen.action == 2: #restart
            self.new()
            pause_screen.action = None

    def events(self): #kiểm tra sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if check_btn_click(mouse_pos, self.btn_setting):
                    self.pausing =True
                    
    def quit(self):
        pygame.quit()
        quit()

class mode_training(game): #chế độ huấn luyện
    def __init__(self,screen):
        super().__init__(screen)
        self.new()
        self.run()

    def new(self):
        super().new()
        for row, tiles in enumerate(self.maze):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    wall(self, col, row) #tạo tường
                if tile == '*':
                    self.player1 = Player1(self, col, row) #tạo player1
                if tile == '-':
                    self.enemy = TankEnemy(self, col, row) #tạo enemy
    
    def auto_respawn(self): #hồi sinh
        self.respawn.respawn_player1()
        self.respawn.respawn_TankEnemy()

    def AddedItems(self):
        super().AddedItems()
        self.show_kill_player2 = show_kill(self.screen, "right") #hiển thị số lần giết của player2
    
    def draw(self):
        super().draw()
        self.show_kill_player2.draw(GameStatistics.number_kill_player2,RED) #vẽ số lần giết của player2

class mode_1v1(game): #chế độ 1v1

    def __init__(self,screen):
        super().__init__(screen)
        self.new()
        self.run()

    def new(self):
        super().new()
        for row, tiles in enumerate(self.maze):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    wall(self, col, row)
                if tile == '*':
                    self.player1 = Player1(self, col, row)
                if tile == '-':
                    self.player2 = Player2(self, col, row)
    
    def AddedItems(self):
        super().AddedItems()
        self.show_kill_player2 = show_kill(self.screen, "right")
    
    def draw(self):
        super().draw()
        self.show_kill_player2.draw(GameStatistics.number_kill_player2,RED) 

    def auto_respawn(self):
        self.respawn.respawn_player1()
        self.respawn.respawn_player2()

class mode_zombie(game): #chế độ zombie
    def __init__(self,screen):
        super().__init__(screen)
        self.new()
        self.run()

    def data(self):
        super().data()
        self.auto_respawn_zombie = auto_respawn_zombie(self, 0.7)

    def AddedItems(self):
        super().AddedItems()
        self.game_over_screen = gameOverGUI(self.screen)
    
    def auto_respawn(self):
        self.auto_respawn_zombie.respawn()

    def pause_game(self):
        super().pause_game()
        if not PLAYER: #nếu player chết thì dừng game
            self.pausing = True
            self.game_over_screen.run()
            self.check_pause_events(self.game_over_screen)

    def new(self):
        super().new()
        GameStatistics.bulletRate = 0.5
        GameStatistics.bulletSpeed = 1000
        for row, tiles in enumerate(self.maze):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    wall(self, col, row)
                if tile == '*':
                    self.player1 = Player1(self, col, row)