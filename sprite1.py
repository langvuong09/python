import math
from os import path
import time
import pygame
from abc import ABC, abstractmethod
from astar import a_star
from setting import *
import zombie
import setting

vector = pygame.math.Vector2  # tạo biến vector2

PLAYER = []
ENEMY = []
BOSS = []

player1_alive = True
game_over = True

turning_x = 0
turning_y = 1

# trong pygame độ xoay dương vector quay theo chiều kim đồng hồ
# trong pygame độ xoay dương hình quay ngược chiều kim đồng hồ
class Player(pygame.sprite.Sprite, ABC):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites  # nhóm các hình ảnh
        # super().__init__(self.groups)
        pygame.sprite.Sprite.__init__(self,self.groups)  # gọi constructor của class cha để thêm sprite của class này vào group sprites
        self.game = game
        self.image_player = image  # ảnh xe
        self.image = self.image_player

        self.vel = vector(0, 0)  # vận tốc của xe
        self.position = vector(x, y) * (SQSIZE) + vector(16, 16)  # vị trí chính giữa rect
        self.hit_rect = self.image.get_rect()  # lấy rect của image
        self.hit_rect.center = self.position  # lấy vị trí chính giữa rect
        self.rect = self.hit_rect.copy()  # copy hit_rect qua rect

        self.is_shoot = False  # biến này cho phép bắn cmn hay ko
        self.rot = 0  # độ xoay của xe
        self.last_fire = pygame.time.get_ticks()  # lần cuối cùng bắn sẽ bằng thời gian từ lúc chạy game đến hiện tại (để tránh việc vừa tạo ra thì nó bắn lun)
        self.target = None  # mục tiêu bắn của xe

        PLAYER.append(self)  # thêm chính nó vào list PLAYER

    def get_game(self):
        return self.game

    def set_rotation_speed(self, speed):
        self.rotation_speed = speed

    def get_rotation_speed(self):
        return self.rotation_speed

    def set_vel(self, vel):
        self.vel = vel

    def get_rot(self):
        return self.rot

    def get_last_fire(self):
        return self.last_fire

    def set_last_fire(self, last_fire):
        self.last_fire = last_fire

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def get_rect(self):
        return self.rect


    def get_is_shoot(self):
        return self.is_shoot

    def set_death_time(self, death_time):
        self.death_time = death_time

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def collide_with_bullet(self):
        pass

    @abstractmethod
    def shoot(self):
        pass

    def auto_targeting(self):
        nearest_target = None
        min_distance = float('inf')  # Khởi tạo khoảng cách nhỏ nhất là vô cùng lớn
        for target in ENEMY + BOSS:  # Kết hợp danh sách ENEMY và BOSS
            distance = ((target.position.x - self.position.x) ** 2 + (
                        target.position.y - self.position.y) ** 2) ** 0.5  # Tính khoảng cách
            if distance < min_distance:  # Nếu khoảng cách nhỏ hơn khoảng cách nhỏ nhất đã tìm thấy trước đó
                min_distance = distance  # Cập nhật khoảng cách nhỏ nhất
                nearest_target = target  # Cập nhật kẻ thù gần nhất
        if nearest_target:  # Nếu tìm thấy kẻ thù gần nhất
            self.target = nearest_target  # Cập nhật mục tiêu của người chơi là kẻ thù gần nhất
            self.rot = self.calculate_rotation_angle(self.target)  # Tính góc xoay để hướng tới kẻ thù
        else:
            self.target = None  # Nếu không có kẻ thù nào trong danh sách, đặt mục tiêu là None
        self.image = pygame.transform.rotate(self.image_player, self.rot)  # Xoay hình ảnh của người chơi
        self.rect = self.image.get_rect()  # Xoay xong thì get_rect lại để hiển thị

    def calculate_rotation_angle(self, target):  # tính độ xoay của hình khi có target(mục tiêu)
        dx = target.position.x - self.position.x
        dy = target.position.y - self.position.y
        x, y = 0, 1
        dot_product = dx * x + dy * y
        magnitude1 = math.sqrt(x ** 2 + y ** 2)
        magnitude2 = math.sqrt(dx ** 2 + dy ** 2)
        cosin_angle = dot_product / (magnitude1 * magnitude2)
        angle_radian = math.acos(cosin_angle)
        angle_degrees = math.degrees(angle_radian)
        if dx < 0:
            angle_degrees = 360 - angle_degrees
        return angle_degrees

    def can_shoot(self):  # kiểm tra xem có được bắn hay không
        if len(PLAYER) <= 2 and ENEMY:
            self.is_shoot = True
        elif len(PLAYER) == 2 or ENEMY:
            self.is_shoot = True
        elif len(PLAYER) <= 2 and BOSS:
            self.is_shoot = True
        elif len(PLAYER) == 2 or BOSS:
            self.is_shoot = True
        else:
            self.is_shoot = False

    def check_collide(self, direction):  # kiểm tra va chạm với tường,người chơi ,enemy
        for wall in self.game.walls:
            if wall.rect.colliderect(self.hit_rect):
                if direction == 'x':
                    if self.vel.x > 0:
                        self.hit_rect.right = wall.rect.left
                    if self.vel.x < 0:
                        self.hit_rect.left = wall.rect.right
                if direction == 'y':
                    if self.vel.y > 0:
                        self.hit_rect.bottom = wall.rect.top
                    if self.vel.y < 0:
                        self.hit_rect.top = wall.rect.bottom
        for enemy in ENEMY:
            if enemy.hit_rect.colliderect(self.hit_rect):
                if direction == 'x':
                    if self.vel.x > 0:
                        self.hit_rect.right = enemy.hit_rect.left
                    if self.vel.x < 0:
                        self.hit_rect.left = enemy.hit_rect.right
                if direction == 'y':
                    if self.vel.y > 0:
                        self.hit_rect.bottom = enemy.hit_rect.top
                    if self.vel.y < 0:
                        self.hit_rect.top = enemy.hit_rect.bottom
        for boss in BOSS:
            if boss.hit_rect.colliderect(self.hit_rect):
                if direction == 'x':
                    if self.vel.x > 0:
                        self.hit_rect.right = boss.hit_rect.left
                    if self.vel.x < 0:
                        self.hit_rect.left = boss.hit_rect.right
                if direction == 'y':
                    if self.vel.y > 0:
                        self.hit_rect.bottom = boss.hit_rect.top
                    if self.vel.y < 0:
                        self.hit_rect.top = boss.hit_rect.bottom

    def move(self):  # di chuyển của xe
        self.hit_rect.centerx += self.vel.x * self.game.changing_time
        self.check_collide('x')
        self.hit_rect.centery += self.vel.y * self.game.changing_time
        self.check_collide('y')

        # Giới hạn di chuyển trong khung cửa sổ
        self.hit_rect.centerx = max(self.hit_rect.width / 2, min(self.hit_rect.centerx, WIDTH - self.hit_rect.width / 2))
        self.hit_rect.centery = max(self.hit_rect.height / 2, min(self.hit_rect.centery, HEIGHT - self.hit_rect.height / 2))

        self.rect.center = self.hit_rect.center
        self.position = vector(self.hit_rect.center)

    def update(self):  # hàm này quan trọng phải có vì liên tục được gọi lại
        self.collide_with_bullet()
        self.can_shoot()
        self.keys()
        self.auto_targeting()
        self.shoot()
        self.move()

# -----------------------------------------------------------------------------------

class Player1(Player):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, getImageTank(PLAYER_IMAGE1, WHITE))  # gọi class cha

    def keys(self):
        super().set_rotation_speed(0)
        super().set_vel(vector(0, 0))
        keys_state = pygame.key.get_pressed()  # lấy giá trị boolean của tất cả các phím
        if keys_state[pygame.K_a]:
            super().set_vel(vector(-playerSpeed, 0))
        if keys_state[pygame.K_d]:
            super().set_vel(vector(playerSpeed, 0))
        if keys_state[pygame.K_w]:
            super().set_vel(vector(0, -playerSpeed))
        if keys_state[pygame.K_s]:
            super().set_vel(vector(0, playerSpeed))
        if keys_state[pygame.K_a] and keys_state[pygame.K_w]:
            super().set_vel(vector(-playerSpeed * math.sqrt(0.5), -playerSpeed * math.sqrt(0.5)))
        if keys_state[pygame.K_a] and keys_state[pygame.K_s]:
            super().set_vel(vector(-playerSpeed * math.sqrt(0.5), playerSpeed * math.sqrt(0.5)))
        if keys_state[pygame.K_d] and keys_state[pygame.K_w]:
            super().set_vel(vector(playerSpeed * math.sqrt(0.5), -playerSpeed * math.sqrt(0.5)))
        if keys_state[pygame.K_d] and keys_state[pygame.K_s]:
            super().set_vel(vector(playerSpeed * math.sqrt(0.5), playerSpeed * math.sqrt(0.5)))

    def shoot(self):  # hàm bắn
        if super().get_is_shoot():
            now = pygame.time.get_ticks()  # lấy thời điểm hiện tại từ lúc game chạy
            if now - super().get_last_fire() > bullet_rate:  # cách 1 khoảng thời gian (bullet_rate)  mới được bắn
                super().set_last_fire(now)
                direction = vector(0, 1).rotate(-super().get_rot()).normalize()  # hướng đạn sẽ di chuyển
                position = super().get_position() + turret.rotate(-super().get_rot())  # vị trí đạn xuất hiện lúc đầu
                Bullet('player1', super().get_game(), position, direction)  # khởi tạo đạn

    def collide_with_bullet(self):  # va chạm với đạn sẽ cút
        for bullet in self.game.bullets:
            if bullet.rect.colliderect(self.hit_rect):
                if bullet.type != 'player1':
                    self.game.death_time.append(
                        time.time())  # lấy thời gian lúc cút để tính thời gian hồi sinh
                    Explosion(self.game, bullet.rect.center)  # khởi tạo vụ nổ
                    bullet.kill()
                    self.kill()
                    PLAYER.remove(self)  # remove chính nó khỏi list PLAYER

# -----------------------------------------------------------------------------------

class Bullet(pygame.sprite.Sprite):
    def __init__(self, type, game, position, direction):
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type  # loại để xác định được đạn của khứa nào bắn ra
        self.image = game.bullet_image
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = position
        self.vel = direction * bulletSpeed  # tính vận tốc của đạn= hướng * tốc độ

    def collide_with_walls(self):  # đạn va chạm với tường sẽ cút và tạo ra vụ nổ
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            Explosion(self.game, self.position)
            self.kill()

    def update(self):
        self.collide_with_walls()
        self.position += self.vel * self.game.changing_time
        self.rect.center = self.position


# -----------------------------------------------------------------------------------
class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, center):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.list_image = getListImage('regularExplosion0', 50, 50, BLACK, 9)  # lấy danh sách ảnh của cảnh động
        self.image = self.list_image[0]  # lấy ảnh xuất hiện đầu tiên
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_time_update = 0
        self.picture = 0  # index ảnh hiện tại
        self.frame_rate = 50  # khoảng cách thời gian (miligiay) của mỗi lần load ảnh

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_time_update > self.frame_rate:
            self.last_time_update = now
            self.picture += 1
            if self.picture == len(self.list_image):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.list_image[self.picture - 1]
                self.rect = self.image.get_rect()
                self.rect.center = center


# -----------------------------------------------------------------------------------
class wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        super().__init__(self.groups)
        self.image = game.wall_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * SQSIZE
        self.rect.y = y * SQSIZE


# -----------------------------------------------------------------------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.path = []  # list đường đi (enemy AI)
        self.velocity = vector(0, 0)
        self.image_enemy = getImageTank(ZOMBIE_IMAGE, WHITE)
        self.image = self.image_enemy
        self.rect = self.image.get_rect()
        self.position = vector(x, y) * SQSIZE + vector(SQSIZE / 2, SQSIZE / 2)
        self.rect.center = self.position
        self.hit_rect = self.rect.copy()
        self.last_move = 0
        self.target = None
        self.rot = 0
        ENEMY.append(self)

    def auto_targeting(self):
        magnitude_min = 10000
        for player in PLAYER:
            magnitude = math.sqrt(
                (player.position.x - self.position.x) ** 2 + (player.position.y - self.position.y) ** 2)
            if magnitude < magnitude_min:
                magnitude_min = magnitude
                self.target = player
            self.rot = self.calculate_rotation_angle(self.target)
        self.image = pygame.transform.rotate(self.image_enemy, self.rot)

    def calculate_rotation_angle(self, target):
        dx = target.position.x - self.position.x
        dy = target.position.y - self.position.y
        x, y = 0, 1
        dot_product = dx * x + dy * y
        magnitude1 = math.sqrt(x ** 2 + y ** 2)
        magnitude2 = math.sqrt(dx ** 2 + dy ** 2)
        cosin_angle = dot_product / (magnitude1 * magnitude2)
        angle_radian = math.acos(cosin_angle)
        angle_degrees = math.degrees(angle_radian)
        if dx < 0:
            angle_degrees = 360 - angle_degrees
        return angle_degrees

    def move(self):
        now = pygame.time.get_ticks()
        if now - self.last_move > 1500:
            self.last_move = now
            self.path = a_star(self.game.maze, (int(self.position.y / (SQSIZE)), int(self.position.x / (SQSIZE))), (
                int(self.game.player1.position.y / (SQSIZE)), int(self.game.player1.position.x / (SQSIZE))))
        if self.path and PLAYER:
            p = self.path[0]
            target = vector(p[1], p[0])
            self.velocity = vector(target.x * SQSIZE + 16 - self.position.x,
                                   target.y * SQSIZE + 16 - self.position.y)
            self.magnitude = math.sqrt(self.velocity.x ** 2 + self.velocity.y ** 2)
            if self.magnitude < 1:
                self.path.remove(p)
                if self.path:
                    target = vector(self.path[0][1], self.path[0][0])
                    self.velocity = vector(target.x * SQSIZE + 16 - self.position.x,
                                           target.y * SQSIZE + 16 - self.position.y)
                    self.magnitude = math.sqrt(self.velocity.x ** 2 + self.velocity.y ** 2)
            if self.magnitude != 0:
                speed = 2.5
                self.velocity = vector(self.velocity.x / self.magnitude * speed,
                                       self.velocity.y / self.magnitude * speed)
                self.hit_rect.centerx += self.velocity.x
                self.check_collide('x')
                self.hit_rect.centery += self.velocity.y
                self.check_collide('y')
                self.rect = self.image.get_rect()
                self.rect.center = vector(self.hit_rect.center)
                self.position = vector(self.hit_rect.center)

    def check_collide(self, direction):  # va chạm với người chơi
        for player in PLAYER:
            if player.hit_rect.colliderect(self.hit_rect):
                if direction == 'x':
                    if self.velocity.x > 0:
                        self.hit_rect.right = player.hit_rect.left
                    if self.velocity.x < 0:
                        self.hit_rect.left = player.hit_rect.right
                if direction == 'y':
                    if self.velocity.y > 0:
                        self.hit_rect.bottom = player.hit_rect.top
                    if self.velocity.y < 0:
                        self.hit_rect.top = player.hit_rect.bottom
                # Khi player va chạm với enemy
                if isinstance(player, Player):
                    global game_over
                    game_over = False
                    player.game.death_time.append(time.time())  # Lưu thời điểm player1 bị xóa
                    Explosion(player.game, player.hit_rect.center)  # Tạo vụ nổ
                    player.kill()  # Xóa player1
                    PLAYER.remove(player)  # Xóa player1 khỏi danh sách PLAYER
                    import event
                    event.main()

    def collide_with_bullet(self):
        for bullet in self.game.bullets:
            if bullet.rect.colliderect(self.rect):
                if bullet.type != 'enemy':
                    self.game.death_time.append(time.time())
                    Explosion(self.game, bullet.rect.center)
                    bullet.kill()
                    self.kill()
                    ENEMY.remove(self)
                    setting.number_kill += 1  # Tăng biến number_kill lên 1 khi enemy bị kill

    def update(self):
        self.collide_with_bullet()
        if PLAYER:
            self.move()
            self.auto_targeting()

# -----------------------------------------------------------------------------------
class Boss(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.path = []  # list đường đi (enemy AI)
        self.velocity = vector(0, 0)
        self.image_boss = getImageTank(BOSS_IMAGE, WHITE)
        self.image = self.image_boss
        self.rect = self.image.get_rect()
        self.position = vector(x, y) * SQSIZE + vector(SQSIZE / 2, SQSIZE / 2)
        self.rect.center = self.position
        self.hit_rect = self.rect.copy()
        self.last_move = 0
        self.target = None
        self.rot = 0
        self.hp = 3
        BOSS.append(self)

    def auto_targeting(self):
        magnitude_min = 10000
        for player in PLAYER:
            magnitude = math.sqrt(
                (player.position.x - self.position.x) ** 2 + (player.position.y - self.position.y) ** 2)
            if magnitude < magnitude_min:
                magnitude_min = magnitude
                self.target = player
            self.rot = self.calculate_rotation_angle(self.target)
        self.image = pygame.transform.rotate(self.image_boss, self.rot)

    def calculate_rotation_angle(self, target):
        dx = target.position.x - self.position.x
        dy = target.position.y - self.position.y
        x, y = 0, 1
        dot_product = dx * x + dy * y
        magnitude1 = math.sqrt(x ** 2 + y ** 2)
        magnitude2 = math.sqrt(dx ** 2 + dy ** 2)
        cosin_angle = dot_product / (magnitude1 * magnitude2)
        angle_radian = math.acos(cosin_angle)
        angle_degrees = math.degrees(angle_radian)
        if dx < 0:
            angle_degrees = 360 - angle_degrees
        return angle_degrees

    def move(self):
        now = pygame.time.get_ticks()
        if now - self.last_move > 1500:
            self.last_move = now
            self.path = a_star(self.game.maze, (int(self.position.y / (SQSIZE)), int(self.position.x / (SQSIZE))), (
                int(self.game.player1.position.y / (SQSIZE)), int(self.game.player1.position.x / (SQSIZE))))
        if self.path and PLAYER:
            p = self.path[0]
            target = vector(p[1], p[0])
            self.velocity = vector(target.x * SQSIZE + 16 - self.position.x,
                                   target.y * SQSIZE + 16 - self.position.y)
            self.magnitude = math.sqrt(self.velocity.x ** 2 + self.velocity.y ** 2)
            if self.magnitude < 1:
                self.path.remove(p)
                if self.path:
                    target = vector(self.path[0][1], self.path[0][0])
                    self.velocity = vector(target.x * SQSIZE + 16 - self.position.x,
                                           target.y * SQSIZE + 16 - self.position.y)
                    self.magnitude = math.sqrt(self.velocity.x ** 2 + self.velocity.y ** 2)
            if self.magnitude != 0:
                speed = 2.5
                self.velocity = vector(self.velocity.x / self.magnitude * speed,
                                       self.velocity.y / self.magnitude * speed)
                self.hit_rect.centerx += self.velocity.x
                self.check_collide('x')
                self.hit_rect.centery += self.velocity.y
                self.check_collide('y')
                self.rect = self.image.get_rect()
                self.rect.center = vector(self.hit_rect.center)
                self.position = vector(self.hit_rect.center)

    def check_collide(self, direction):  # va chạm với người chơi
        for player in PLAYER:
            if player.hit_rect.colliderect(self.hit_rect):
                if direction == 'x':
                    if self.velocity.x > 0:
                        self.hit_rect.right = player.hit_rect.left
                    if self.velocity.x < 0:
                        self.hit_rect.left = player.hit_rect.right
                if direction == 'y':
                    if self.velocity.y > 0:
                        self.hit_rect.bottom = player.hit_rect.top
                    if self.velocity.y < 0:
                        self.hit_rect.top = player.hit_rect.bottom
                # Khi player va chạm với enemy
                if isinstance(player, Player):
                    global game_over
                    game_over = False
                    player.game.death_time.append(time.time())  # Lưu thời điểm player bị xóa
                    Explosion(player.game, player.hit_rect.center)  # Tạo vụ nổ
                    player.kill()  # Xóa player
                    PLAYER.remove(player)  # Xóa player khỏi danh sách PLAYER
                    import event
                    event.main()

    def collide_with_bullet(self):
        for bullet in self.game.bullets:
            if bullet.rect.colliderect(self.rect):
                self.hp -= 1 # Giảm máu của boss
                bullet.kill()
                if bullet.type != 'enemy' and self.hp == 0:
                    self.game.death_time.append(time.time())
                    Explosion(self.game, bullet.rect.center)
                    self.kill()
                    BOSS.remove(self)
                    setting.number_kill += 1  # Tăng biến number_kill lên 1 khi boss bị kill

    def update(self):
        self.collide_with_bullet()
        if PLAYER:
            self.move()
            self.auto_targeting()