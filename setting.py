from os import path
import pygame
vector=pygame.math.Vector2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (120, 120, 120)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (120, 104, 82)
BLUE = (0, 0, 255)
SILVER = (192,192,192)
DARK_SEA_GREEN = (211,211,211)

WIDTH=1024
HEIGHT=768
FPS=60
TITLE='TANK TROUBLE'
BGCOLOR=WHITE

SQSIZE=32 #KÍCH THƯỚC 1 Ô LƯỚI TRONG GAME
GRIDWIDTH=WIDTH/SQSIZE #SỐ Ô THEO CHIỀU RỘNG
GRIDHEIGHT=HEIGHT/SQSIZE #SỐ Ô THEO CHIỀU CAO

playerSpeed=200

WALL_IMAGE='dirt.png' #hình tường
PLAYER_IMAGE1='tank1.png' #hình player1
PLAYER_IMAGE2='tank2.jpg' # hình player2
BULLET_IMAGE='BULLET.png' # hình đạn
ZOMBIE_IMAGE='zombie.png'
number_kill = 0

# RotationSpeedOfPlayer=120

player_box=pygame.Rect(0,0,32,32)
bullet_box=pygame.Rect(0,0,10,10)

#shooting setting
bulletSpeed=500
bullet_rate=1000
bullet_rate_flash = 500
turret=vector(0,30) # vị trí đạn xuất hiện

folder_of_game=path.dirname(__file__) #tạo đường dẫn đến thư mục chứa tệp chỉ định
image_folder = path.join(folder_of_game, 'img') #kết hợp thành đường dẫn đến thư mục img trong folder chưa tệp đang chạy
maze_forder=path.join(folder_of_game,'MAZEFOLDER')

def getImageTank(image,color): # trả về hình tank
    player_image = pygame.image.load(path.join(image_folder, image)).convert() #kết hợp tạo thành đường dẫn đến file ảnh chuyển đổi hình ảnh thành dạng pixel phù hợp với màn hình
    player_image.set_colorkey(color)
    return player_image

def getListImage(str_image,width,height,color,numbers): #lấy danh sách ảnh của cảnh động
    list_image=[]
    for i in range(numbers):
        image=pygame.image.load(path.join(image_folder,str_image+str(i)+'.png'))
        image=pygame.transform.scale(image,(width,height))
        image.set_colorkey(color)
        list_image.append(image)
    return list_image