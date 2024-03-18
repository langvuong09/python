import pygame
from setting import *
from waitting_hall import *
from player import *
import player
import sprites
import setting
import zombie
import waitting_hall

def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    icon = pygame.image.load(r'img\logo.png')
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Tạo nút chơi lại và quay về màn hình chính
    k = 160
    restart_Button = Button(screen, (screen.get_width() - 200) // 2, (screen.get_height() - 50) // 2 + k, 200, 50, SILVER,
                     BLACK, 3, "RESTART")
    exit_Button = Button(screen, (screen.get_width() - 200) // 2, (screen.get_height() - 50) // 2 + k + 70, 200, 50, SILVER,
                     BLACK, 3, "EXIT")

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # So sánh tọa độ x y của nút với của con trỏ chuột
                if restart_Button.x <= mouse_pos[0] <= restart_Button.x + restart_Button.width and restart_Button.y <= mouse_pos[1] <= restart_Button.y + restart_Button.height:
                    if player.condition_mode_training == False:
                        player.main(restart_Button, exit_Button)
                    if player.condition_mode_1v1 == False:
                        player.main(exit_Button, restart_Button)
                    if zombie.condition_mode_zombie == False:
                        setting.number_kill = 0
                        zombie.main()

                if exit_Button.x <= mouse_pos[0] <= exit_Button.x + exit_Button.width and exit_Button.y <= mouse_pos[1] <= exit_Button.y + exit_Button.height:
                    waitting_hall.main()

        # Vẽ màn hình
        screen.fill(DARK_SEA_GREEN)

        # Đoạn code kiểm tra nếu Player1 hoặc Player2 còn sống thì gán result là hình ảnh win
        if sprites.player1_alive and player.condition_mode_1v1 == False:
            # Kết quả trò chơi
            result = pygame.image.load(r"img\win.jpg")
            screen.blit(result, (235, 180))
        else:
            result = pygame.image.load(r"img\game over.png")
            screen.blit(result, (160, 120))

        # Vẽ các nút
        restart_Button.draw()
        exit_Button.draw()

        # Cập nhật màn hình
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
