from .singleplayer_mode import SinglePlayerMode


class ZenMode(SinglePlayerMode):
    def __init__(self, game):
        SinglePlayerMode.__init__(self, game)
        pass

    def start_game(self):
        print("comming soon!")

    def handle_out_of_bounds(self):
        pass
