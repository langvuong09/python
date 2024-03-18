import pygame
from setting import *
import player
import zombie
import setting

class Button:
    def __init__(self, screen, x, y, width, height, color, border_color, border_width, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.text = text

    def draw(self):
        # vẽ viền cho nút
        pygame.draw.rect(self.screen, self.border_color, (self.x, self.y, self.width, self.height), self.border_width)
        # vẽ nút
        pygame.draw.rect(self.screen, self.color, (self.x + self.border_width, self.y + self.border_width, self.width - self.border_width * 2, self.height - self.border_width * 2))
        # canh chỉnh chữ trong nút
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        self.screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    icon = pygame.image.load(r'img\logo.png')
    background = pygame.image.load(r'img\background.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Gán các button vào các biến
    x = 160
    zombie_Button = Button(screen, (screen.get_width() - 200) // 2, (screen.get_height() - 50) // 2 + x - 70, 200, 50,SILVER, BLACK, 3, "ZOMBIE WORLD")
    training_Button = Button(screen, (screen.get_width() - 200) // 2, (screen.get_height() - 50) // 2 + x, 200, 50, SILVER, BLACK, 3, "TRAINING")
    pvp_Button = Button(screen, (screen.get_width() - 200) // 2, (screen.get_height() - 50) // 2 + x + 70, 200, 50, SILVER, BLACK, 3, "2 PLAYERS")
    button_quit = Button(screen, (screen.get_width() - 200) // 2, (screen.get_height() - 50) // 2 + x + 140, 200, 50, SILVER, BLACK, 3, "QUIT")

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # so sánh tọa độ x y của nút với của con trỏ chuột
                if button_quit.x <= mouse_pos[0] <= button_quit.x + button_quit.width and button_quit.y <= mouse_pos[1] <= button_quit.y + button_quit.height:
                    run = False  # Thoát chương trình
                if training_Button.x <= mouse_pos[0] <= training_Button.x + training_Button.width and training_Button.y <= mouse_pos[1] <= training_Button.y + training_Button.height:
                    player.condition_mode_1v1 = True
                    player.condition_mode_1v1_of_restart = True
                    zombie.condition_mode_zombie = True
                    zombie.condition_mode_zombie_of_restart = True
                    player.main(training_Button,pvp_Button)
                if pvp_Button.x <= mouse_pos[0] <= pvp_Button.x + pvp_Button.width and pvp_Button.y <= mouse_pos[1] <= pvp_Button.y + pvp_Button.height:
                    player.condition_mode_training = True
                    player.condition_mode_training_of_restart = True
                    zombie.condition_mode_zombie = True
                    zombie.condition_mode_zombie_of_restart = True
                    player.main(training_Button,pvp_Button)
                if zombie_Button.x <= mouse_pos[0] <= zombie_Button.x + zombie_Button.width and zombie_Button.y <= mouse_pos[1] <= zombie_Button.y + zombie_Button.height:
                    player.condition_mode_training = True
                    player.condition_mode_training_of_restart = True
                    player.condition_mode_1v1 = True
                    player.condition_mode_1v1_of_restart = True
                    zombie.condition_mode_zombie = False
                    setting.number_kill = 0
                    zombie.main()
        screen.blit(background, (0, 0))
        zombie_Button.draw()
        training_Button.draw()
        pvp_Button.draw()
        button_quit.draw()
        pygame.display.update()

    # Kết thúc Pygame khi vòng lặp kết thúc
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
