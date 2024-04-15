import math


class AutoTargeting: # class ngắm tự động
    def auto_target_player(obj,position,PLAYER): # tự động ngắm player
        for player in PLAYER:
            if player != obj:
                target = player
                return calculate_rotation_angle(target, position)

    def auto_target_enemy(position,ENEMY): # tự động ngắm enemy
        magnitude_min = 10000
        for enemy in ENEMY:
            magnitude = math.sqrt(
                (enemy.position.x - position.x) ** 2 + (enemy.position.y - position.y) ** 2)
            if magnitude < magnitude_min:
                magnitude_min = magnitude
                target = enemy
        return calculate_rotation_angle(target, position)

def calculate_rotation_angle(target, position): #tính góc quay
        dx = target.position.x - position.x
        dy = target.position.y - position.y
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