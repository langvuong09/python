import pygame

from setting import *
from GameStatistics import *


class show_kill: #hiển thị số lần giết
    def __init__(self,screen,direction):
        self.screen = screen
        self.direction = direction
        self.count=0
        self.font = pygame.font.Font(None, 30)  # Chọn font và kích cỡ
    def draw(self,count,color):
        self.text = self.font.render("Kill: " + str(count), True, color)  # Tạo đối tượng văn bản
        self.pos()
        self.screen.blit(self.text, self.text_rect)  # Vẽ văn bản lên màn hình
    def pos(self): # Đặt vị trí của văn bản
        if self.direction == "left":
            self.text_rect = self.text.get_rect(center=(50, 20))
            return
        self.text_rect = self.text.get_rect(center=((WIDTH // 2) + 350, 20))  # Đặt vị trí của văn bản
