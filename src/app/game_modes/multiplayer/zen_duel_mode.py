from src.app.game_modes.multiplayer.multiplayer_mode import MultiPlayerMode


# TODO - TO BE IMPLEMENTED
class ZenDuelMode(MultiPlayerMode):
    def __len__(self, game):
        MultiPlayerMode.__init__(self, game)

    def update(self):
        MultiPlayerMode.update(self)

    def blit_items(self):
        pass

    def handle_collisions(self):
        pass

    def handle_out_of_bounds(self):
        pass
