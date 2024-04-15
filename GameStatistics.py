class GameStatistics:
    number_kill_player1 = 0 #số lần giết của player1
    number_kill_player2 = 0 #số lần giết của player2
    death_time_player1 = None #thời gian chết của player1
    death_time_player2 = None #thời gian chết của player2
    death_time_enemy = None #thời gian chết của enemy
    bulletSpeed = 500 #tốc độ của đạn
    bulletRate = 1 #tốc độ bắn

    def reset_kill(): #reset số lần giết
        GameStatistics.number_kill_player1 = 0 
        GameStatistics.number_kill_player2 = 0

    def reset_bullet(): #reset tốc độ đạn
        GameStatistics.bulletSpeed = 500
        GameStatistics.bulletRate = 1

    def reset_death_time(): #reset thời gian chết
        GameStatistics.death_time_player1 = None
        GameStatistics.death_time_player2 = None
        GameStatistics.death_time_enemy = None