from src.app.game_modes.multiplayer.multiplayer_mode import MultiPlayerMode


# TODO - TO BE IMPLEMENTED
class ClassicAttackMode(MultiPlayerMode):
    def __init__(self, game):
        MultiPlayerMode.__init__(self, game)

    def blit_items(self):
        pass

    def handle_collisions(self):
        pass

    def handle_out_of_bounds(self):
        pass
