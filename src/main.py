from game import Game
from config import global_config
from src.app.physics.time_controller import TimeController


if __name__ == '__main__':
    game = Game(global_config)
    game.start()
