import pygame
from Button import Button
from setting import *


class pauseGUI: #màn hình pause
    def __init__(self, screen):
        self.screen = screen
        self.action = None
        self.addControls()

    def addControls(self):
        k = 160
        self.continue_Button = Button(self.screen, (self.screen.get_width() - 200) // 2, (self.screen.get_height() - 50) // 2 + k - 70, 200, 50, SILVER,
                                 BLACK, 3, "CONTINUE")
        self.restart_button_Setting = Button(self.screen, (self.screen.get_width() - 200) // 2, (self.screen.get_height() - 50) // 2 + k, 200, 50, SILVER,
                                        BLACK, 3, "RESTART")
        self.exit_button = Button(self.screen, (self.screen.get_width() - 200) // 2, (self.screen.get_height() - 50) // 2 + k + 70, 200, 50, SILVER,
                             BLACK, 3, "EXIT")
        
    def draw(self):
        self.continue_Button.draw()
        self.restart_button_Setting.draw()
        self.exit_button.draw()

    def addEvents(self):
        self.action = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if check_btn_click(mouse_pos, self.exit_button):
                    self.running = False
                    self.action=0 # Thoát màn 0 , tiếp tục 1, restart 2
                if check_btn_click(mouse_pos, self.continue_Button):
                    self.running = False
                    self.action=1
                if check_btn_click(mouse_pos, self.restart_button_Setting):
                    self.running = False
                    self.action=2
    def quit(self):
        pygame.quit()
        quit()
    def run(self):
        self.running = True
        while self.running:
            self.addEvents()
            self.draw()
            pygame.display.flip()