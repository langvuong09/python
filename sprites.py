import math
import pygame
from GameStatistics import GameStatistics
from astar import a_star
from auto_target import AutoTargeting
from setting import *
from sprites import *

vector = pygame.math.Vector2  # tạo biến vector2

PLAYER = []
ENEMY = []

# trong pygame độ xoay dương vector quay theo chiều kim đồng hồ
# trong pygame độ xoay dương hình quay ngược chiều kim đồng hồ


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites  # nhóm các hình ảnh
        # super().__init__(self.groups)
        pygame.sprite.Sprite.__init__(self,
                                      self.groups)  # gọi constructor của class cha để thêm sprite của class này vào group sprites
        self.game = game
        self.image_player = image  # ảnh xe
        self.image = self.image_player

        self.vel = vector(0, 0)  # vận tốc của xe
        self.position = vector(x, y) * (SQSIZE) + vector(16, 16)  # vị trí chính giữa rect
        self.hit_rect = self.image.get_rect()  # lấy rect của image
        self.hit_rect.center = self.position  # lấy vị trí chính giữa rect
        self.rect = self.hit_rect.copy()  # copy hit_rect qua rect

        self.is_shoot = False  # kiểm tra xem có được bắn hay không
        self.rot = 0  # độ xoay của xe
        
        self.last_fire = 0 # thời gian cuối cùng bắn
        self.rotation_speed = 0  # tốc độ xoay của xe
        PLAYER.append(self)  # thêm chính nó vào list PLAYER

    def keys(self): # hàm kiểm tra xem người chơi ấn nút nào và gán cho vel 1 vector tương ứng với hướng đó
        self.rotation_speed = 0
        self.vel = vector(0, 0)

    def collide_with_bullet(self): # va chạm với đạn
        pass

    def change_rot(self): # hàm xoay hình ảnh của xe theo hướng của target
        self.auto_targeting()
        if self.rot == None:
            return
        self.image = pygame.transform.rotate(self.image_player, self.rot)
        self.rect = self.image.get_rect()  # xoay xong thì get_rect lại để hiển thị

    def auto_targeting(self):
        pass

    def shoot(self):  # hàm bắn
        if self.is_shoot:
            self.last_fire += self.game.changing_time
            # cách 1 khoảng thời gian (bullet_rate)  mới được bắn
            if self.last_fire > GameStatistics.bulletRate:
                self.last_fire = 0
                # hướng đạn sẽ di chuyển
                direction = vector(0, 1).rotate(-self.rot).normalize()
                position = self.position + turret.rotate(-self.rot
                                                         )  # vị trí đạn xuất hiện lúc đầu
                self.respawn_bullet(direction, position)  # khởi tạo đạn

    def respawn_bullet(self, direction, position):
        pass

    def can_shoot(self):  # kiểm tra xem có được bắn hay không
        if len(PLAYER) < 2 and  not ENEMY:
            self.is_shoot = False
            return
        self.is_shoot = True

    def collide_with_walls(self, direction):  # kiểm tra va chạm với tường
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

    


    def move(self):  # di chuyển của xe
        # cộng vận tốc vô hit_rect.center trước để kiểm tra va chạm
        self.hit_rect.centerx += self.vel.x * self.game.changing_time
        self.collide_with_walls('x')
        self.hit_rect.centery += self.vel.y * self.game.changing_time
        self.collide_with_walls('y')
        
        self.hit_rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT)) # giới hạn hit_rect trong màn hình để không ra khỏi màn hình
        # sau đó cập nhật rect và position để hình ảnh được cập nhật lại vị trí
        self.rect.center = self.hit_rect.center
        self.position = vector(self.hit_rect.center)

    def update(self):  # hàm update của sprite
        self.collide_with_bullet()
        self.can_shoot()
        self.keys()
        self.change_rot()
        self.shoot()
        self.move()


# -----------------------------------------------------------------------------------
class Player1(Player):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, getImage(PLAYER_IMAGE1, WHITE))  # gọi class cha

    def keys(self): 
        super().keys()
        keys_state = pygame.key.get_pressed()  # lấy giá trị boolean của tất cả các phím
        if keys_state[pygame.K_LEFT]:
            self.vel = vector(-playerSpeed, 0)
        if keys_state[pygame.K_RIGHT]:
            self.vel = vector(playerSpeed, 0)
        if keys_state[pygame.K_UP]:
            self.vel = vector(0, -playerSpeed)
        if keys_state[pygame.K_DOWN]:
            self.vel = vector(0, playerSpeed)
        if keys_state[pygame.K_LEFT] and keys_state[pygame.K_UP]:
            self.vel = vector(-playerSpeed * math.sqrt(0.5), -
                              playerSpeed * math.sqrt(0.5))
        if keys_state[pygame.K_LEFT] and keys_state[pygame.K_DOWN]:
            self.vel = vector(-playerSpeed * math.sqrt(0.5),
                              playerSpeed * math.sqrt(0.5))
        if keys_state[pygame.K_RIGHT] and keys_state[pygame.K_UP]:
            self.vel = vector(playerSpeed * math.sqrt(0.5), -
                              playerSpeed * math.sqrt(0.5))
        if keys_state[pygame.K_RIGHT] and keys_state[pygame.K_DOWN]:
            self.vel = vector(playerSpeed * math.sqrt(0.5),
                              playerSpeed * math.sqrt(0.5))

    def auto_targeting(self): # hàm tự động nhắm mục tiêu
        if not ENEMY and not PLAYER:
            return
        if ENEMY:
            self.rot = AutoTargeting.auto_target_enemy(self.position, ENEMY)
            return
        self.rot = AutoTargeting.auto_target_player(
            self, self.position, PLAYER)

    def respawn_bullet(self, direction, position): # hàm khởi tạo đạn
        Bullet('player1', self.game, position, direction)

    def collide_with_player(self): # va chạm với người chơi
        for player in PLAYER:
            if player != self and player.hit_rect.colliderect(self.hit_rect):
                Explosion(self.game, player.hit_rect.center)  # Tạo vụ nổ
                Explosion(self.game, self.hit_rect.center)  # Tạo vụ nổ
                player.kill()  
                self.kill()  
                PLAYER.remove(player)  
                PLAYER.remove(self)
                GameStatistics.death_time_player1 = 0
                GameStatistics.death_time_player2 = 0

    def collide_with_bullet(self):  # va chạm với đạn
        for bullet in self.game.bullets:
            if bullet.rect.colliderect(self.hit_rect):
                if bullet.type != 'player1':
                    GameStatistics.death_time_player1 = 0
                    GameStatistics.number_kill_player2 += 1
                    Explosion(self.game, bullet.rect.center)  # khởi tạo vụ nổ
                    bullet.kill()
                    self.kill()
                    PLAYER.remove(self)  # remove chính nó khỏi list PLAYER

    def update(self): # hàm update của sprite
        self.collide_with_player()
        super().update()

# -----------------------------------------------------------------------------------


class Player2(Player):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, getImage(PLAYER_IMAGE2, WHITE))

    def keys(self):
        super().keys()
        keys_state = pygame.key.get_pressed()  # lấy giá trị boolean của tất cả các phím
        if keys_state[pygame.K_a]:
            self.vel = vector(-playerSpeed, 0)
        if keys_state[pygame.K_d]:
            self.vel = vector(playerSpeed, 0)
        if keys_state[pygame.K_w]:
            self.vel = vector(0, -playerSpeed)
        if keys_state[pygame.K_s]:
            self.vel = vector(0, playerSpeed)
        if keys_state[pygame.K_a] and keys_state[pygame.K_w]:
            self.vel = vector(-playerSpeed * math.sqrt(0.5), -
                              playerSpeed * math.sqrt(0.5))
        if keys_state[pygame.K_a] and keys_state[pygame.K_s]:
            self.vel = vector(-playerSpeed * math.sqrt(0.5),
                              playerSpeed * math.sqrt(0.5))
        if keys_state[pygame.K_d] and keys_state[pygame.K_w]:
            self.vel = vector(playerSpeed * math.sqrt(0.5), -
                              playerSpeed * math.sqrt(0.5))
        if keys_state[pygame.K_d] and keys_state[pygame.K_s]:
            self.vel = vector(playerSpeed * math.sqrt(0.5),
                              playerSpeed * math.sqrt(0.5))

    def auto_targeting(self):
        if not PLAYER:
            return
        self.rot = AutoTargeting.auto_target_player(
            self, self.position, PLAYER)

    def respawn_bullet(self, direction, position):
        Bullet('player2', self.game, position, direction)

    def collide_with_bullet(self):
        for bullet in self.game.bullets:
            if bullet.rect.colliderect(self.hit_rect):
                if bullet.type != 'player2':
                    GameStatistics.death_time_player2 = 0
                    GameStatistics.number_kill_player1 += 1
                    Explosion(self.game, bullet.rect.center)
                    bullet.kill()
                    self.kill()
                    PLAYER.remove(self)

# -----------------------------------------------------------------------------------


class Bullet(pygame.sprite.Sprite):
    def __init__(self, type, game, position, direction):
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type  # loại để xác định được đạn của ai
        self.image = getImage(BULLET_IMAGE, WHITE)
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = position
        self.vel = direction * GameStatistics.bulletSpeed  # tính vận tốc của đạn= hướng * tốc độ

    def collide_with_walls(self):  # đạn va chạm với tường sẽ tạo ra vụ nổ
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            Explosion(self.game, self.position)
            self.kill()

    def despawn(self):  # hàm này để xóa đạn khi nó đi ra khỏi màn hình
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.kill()

    def move(self):  # hàm di chuyển của đạn
        self.position += self.vel * self.game.changing_time
        self.rect.center = self.position

    def update(self):
        self.collide_with_walls()
        self.move()
        self.despawn()


# -----------------------------------------------------------------------------------
class Explosion(pygame.sprite.Sprite): # class vụ nổ
    def __init__(self, game, center):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.list_image = getListImage('regularExplosion0', 50, 50, BLACK, 9)  # lấy danh sách ảnh của cảnh động vụ nổ
        self.image = self.list_image[0]  # lấy ảnh xuất hiện đầu tiên
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_time_update = 0
        self.picture = 0  # index ảnh hiện tại
        # khoảng cách thời gian (giây) của mỗi lần load ảnh
        self.frame_rate = 0.05

    def update(self):
        self.last_time_update += self.game.changing_time
        if self.last_time_update > self.frame_rate:
            self.last_time_update = 0
            self.picture += 1
            if self.picture == len(self.list_image):
                self.kill()
                return
            center = self.rect.center
            self.image = self.list_image[self.picture - 1]
            self.rect = self.image.get_rect()
            self.rect.center = center


# -----------------------------------------------------------------------------------
class wall(pygame.sprite.Sprite): # class tường
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        super().__init__(self.groups)
        self.image = getImage(WALL_IMAGE, WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * SQSIZE
        self.rect.y = y * SQSIZE


# -----------------------------------------------------------------------------------
class enemy(pygame.sprite.Sprite): # class enemy
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.image_enemy = image
        self.image = self.image_enemy
        self.velocity = vector(0, 0)  # vận tốc của xe
        self.position = vector(x, y) * (SQSIZE) + vector(16, 16)  # vị trí chính giữa rect
        self.hit_rect = self.image.get_rect()  # lấy rect của image
        self.hit_rect.center = self.position    
        self.rect = self.hit_rect.copy()  # copy hit_rect qua rect
        self.path = []  # list đường đi (enemy AI)
        
        
        self.target = None
        self.rot = 0
        ENEMY.append(self)

    def auto_targeting(self):
        if not PLAYER:
            return
        self.rot = AutoTargeting.auto_target_player(self, self.position, PLAYER)

    def change_rot(self):
        self.auto_targeting()
        if self.rot == None:
            return
        self.image = pygame.transform.rotate(self.image_enemy, self.rot)
        self.rect = self.image.get_rect()

    def ability(self):
        self.change_rot()
        self.move()

    def calculate_positions(self): # tính toán vị trí của enemy và player
        current_position = (int(self.position.y / SQSIZE), int(self.position.x / SQSIZE))
        player_position = (int(self.game.player1.position.y / SQSIZE), int(self.game.player1.position.x / SQSIZE))
        return current_position, player_position

    def update_path(self): # cập nhật đường đi
            current_position, player_position = self.calculate_positions()
            self.path = a_star(self.game.maze, current_position, player_position)

    def update_position(self,magnitude): # cập nhật vị trí
        speed = 2.5
        self.velocity = vector(self.velocity.x / magnitude * speed,
                                       self.velocity.y / magnitude * speed)
        self.hit_rect.centerx += self.velocity.x
        self.hit_rect.centery += self.velocity.y
        self.rect.center = self.hit_rect.center
        self.position = vector(self.hit_rect.center)

    def move(self): # di chuyển của enemy
        self.update_path()
        if self.path and PLAYER:
            p = self.path[0]
            target = vector(p[1], p[0])
            self.velocity = vector(
                target.x * SQSIZE + 16 - self.position.x, target.y * SQSIZE + 16 - self.position.y)
            self.magnitude = math.sqrt(
                self.velocity.x ** 2 + self.velocity.y ** 2)
            if self.magnitude != 0:
                self.update_position(self.magnitude)    

    def collide_with_player(self):  # va chạm với người chơi
        for player in PLAYER:
            if player.hit_rect.colliderect(self.hit_rect):
                Explosion(self.game, player.hit_rect.center)  # Tạo vụ nổ
                Explosion(self.game, self.hit_rect.center)  # Tạo vụ nổ
                player.kill()  # Xóa player1
                self.kill()  # Xóa enemy
                PLAYER.remove(player)  # Xóa player1 khỏi danh sách PLAYER
                ENEMY.remove(self)  # Xóa enemy khỏi danh sách ENEMY
                GameStatistics.death_time_player1 = 0
                GameStatistics.death_time_enemy = 0

    def collide_with_bullet(self):
        for bullet in self.game.bullets:
            if bullet.rect.colliderect(self.rect):
                if bullet.type != 'enemy':
                    GameStatistics.death_time_enemy = 0
                    GameStatistics.number_kill_player1 += 1
                    Explosion(self.game, bullet.rect.center)
                    bullet.kill()
                    self.kill()
                    ENEMY.remove(self)

    def update(self):
        self.collide_with_player()
        self.collide_with_bullet()
        if PLAYER:
            self.ability()


class TankEnemy(enemy): # class TankEnemy
    def __init__(self, game, x, y):
        super().__init__(game, x, y, getImage(PLAYER_IMAGE2, WHITE))
        self.last_fire = 0

    def shoot(self):
        self.last_fire += self.game.changing_time
        if self.last_fire >= GameStatistics.bulletRate:
            direction = vector(0, 1).rotate(-self.rot).normalize()
            position = self.position + turret.rotate(-self.rot)
            Bullet('enemy', self.game, position, direction)
            self.last_fire = 0

    def ability(self): # khả năng của enemy
        super().ability()
        self.shoot()

class Zombie(enemy): # class Zombie
    def __init__(self, game, x, y):
        super().__init__(game, x, y, getImage(ZOMBIE_IMAGE, WHITE))

    def collide_with_bullet(self):
        for bullet in self.game.bullets:
            if bullet.rect.colliderect(self.hit_rect):
                bullet.kill()
                Explosion(self.game, bullet.rect.center)
                self.kill()
                ENEMY.remove(self)
                GameStatistics.number_kill_player1 += 1
