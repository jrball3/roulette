from game import Game
from state import RouletteInitialState


class NumberColor(IntEnum):
  RED = 0
  BLACK = 1
  GREEN = 2


class RouletteFactory():
  def __init__(self):
    self.name = None
    self.game_id = None
    self.dealer = None
    self.players = []

  def with_name(self, name):
    self.name = name
    return self

  def with_game_id(self, game_id):
    self.game_id = game_id
    return self

  def with_dealer(self, dealer):
    self.dealer = dealer

  def with_players(self, players):
    self.players = players

  def build(self):
    game = Game(name=self.name, game_id=self.game_id, 
                start_state=RouletteInitialState())
    if self.dealer is not None:
      game.register_listener(self.dealer)
    for ply in (self.players or []):
      game.register_listener(ply)
    return game