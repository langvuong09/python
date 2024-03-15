import pygame
from setting import *
from waitting_hall import *
from player import *
import sprites
import player
import waitting_hall

def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    icon = pygame.image.load(r'img\logo.png')
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    k = 160
    # Tạo nút tiếp tục và quay về màn hình chính
    if player.condition_mode_training_of_restart == False:
        continue_Button = Button(screen, (screen.get_width() - 200) // 2, (screen.get_height() - 50) // 2 + k - 70, 200, 50, SILVER,
                         BLACK, 3, "CONTINUE")
    restart_button_Setting = Button(screen, (screen.get_width() - 200) // 2, (screen.get_height() - 50) // 2 + k, 200, 50, SILVER,
                     BLACK, 3, "RESTART")
    exit_button = Button(screen, (screen.get_width() - 200) // 2, (screen.get_height() - 50) // 2 + k + 70, 200, 50, SILVER,
                     BLACK, 3, "EXIT")

    g = player.Game()  # Sử dụng player.Game thay vì Game
    settings_x, settings_y = g.get_setting_coordinates()  # Sử dụng hàm từ player.Game để lấy tọa độ
    menu = True
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # So sánh tọa độ x y của nút với của con trỏ chuột
                if restart_button_Setting.x <= mouse_pos[0] <= restart_button_Setting.x + restart_button_Setting.width and restart_button_Setting.y <= mouse_pos[
                    1] <= restart_button_Setting.y + restart_button_Setting.height:
                    if player.condition_mode_training_of_restart == False:
                        player.main(restart_button_Setting, exit_button)
                    if player.condition_mode_1v1_of_restart == False:
                        player.main(exit_button, restart_button_Setting)

                if exit_button.x <= mouse_pos[0] <= exit_button.x + exit_button.width and exit_button.y <= mouse_pos[
                    1] <= exit_button.y + exit_button.height:
                    waitting_hall.main()

                if continue_Button.x <= mouse_pos[0] <= continue_Button.x + continue_Button.width and continue_Button.y <= mouse_pos[
                    1] <= continue_Button.y + continue_Button.height:
                    # Thay đổi trạng thái của module player để tiếp tục hoạt động
                    g.running = True
                    # Kết thúc module game_setting
                    run = False

        # Vẽ màn hình
        screen.fill(DARK_SEA_GREEN)

        # Vẽ các nút
        if player.condition_mode_training_of_restart == False:
            continue_Button.draw()
        restart_button_Setting.draw()
        exit_button.draw()

        # Hiển thị hình ảnh setting
        settings = pygame.image.load(r'img\setting.png')
        settings = pygame.transform.scale(settings, (100, 100))  # Chỉnh kích thước hình ảnh nếu cần
        screen.blit(settings, (settings_x, settings_y))  # Hiển thị ở góc trên cùng bên phải

        # Cập nhật màn hình
        pygame.display.update()



if __name__ == "__main__":
    main()
