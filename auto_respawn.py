import random

from sprites import *


class auto_respawn: # respawn cho tank và zombie
    def __init__(self,game, respawn_time):
        self.pos_respawn = []
        self.game= game
        self.maze = self.game.maze
        self.respawn_time = respawn_time
        self.add_pos_respawn()
    def add_pos_respawn(self):
        for row, tiles in enumerate(self.maze):
                for col, tile in enumerate(tiles):
                    if tile == '?':  # nơi sinh ra
                        self.pos_respawn.append((col, row))
class auto_respawn_tank(auto_respawn): # respawn cho tank
    def __init__(self, game, respawn_time):
        super().__init__(game, respawn_time)

    def respawn_player1(self): # respawn cho player1
        if GameStatistics.death_time_player1 == None :
            return
        GameStatistics.death_time_player1 += self.game.changing_time
        if GameStatistics.death_time_player1 < self.respawn_time:
            return
        pos_respawn_random = random.choice(self.pos_respawn)
        self.game.player1 = Player1(self.game, pos_respawn_random[0], pos_respawn_random[1])
        GameStatistics.death_time_player1 = None
        
    def respawn_player2(self): # respawn cho player2
        if GameStatistics.death_time_player2 == None:
            return
        GameStatistics.death_time_player2 += self.game.changing_time
        if GameStatistics.death_time_player2 < self.respawn_time:
            return
        pos_respawn_random = random.choice(self.pos_respawn)
        self.game.player2 = Player2(self.game, pos_respawn_random[0], pos_respawn_random[1])
        GameStatistics.death_time_player2 = None

    def respawn_TankEnemy(self): # respawn cho enemy
        if GameStatistics.death_time_enemy == None:
            return
        GameStatistics.death_time_enemy += self.game.changing_time
        if GameStatistics.death_time_enemy < self.respawn_time:
            return
        pos_respawn_random = random.choice(self.pos_respawn)
        self.game.enemy = TankEnemy(self.game, pos_respawn_random[0], pos_respawn_random[1])
        GameStatistics.death_time_enemy = None

class auto_respawn_zombie(auto_respawn): # respawn cho zombie
    def __init__(self, game, respawn_time):
        super().__init__(game, respawn_time)
        self.last_enemy_spawn_time =0
    def respawn(self): # respawn cho zombie
        pos_respawn_random = random.choice(self.pos_respawn)
        self.last_enemy_spawn_time += self.game.changing_time
        if self.last_enemy_spawn_time < self.respawn_time:
            return
        self.last_enemy_spawn_time = 0
        Zombie(self.game, pos_respawn_random[0], pos_respawn_random[1])
