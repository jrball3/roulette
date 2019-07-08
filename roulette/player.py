from roulette.bet import BetBuilder
from roulette.game import GamePlayer
from roulette.common import RouletteActionType
from roulette.action import (
  RouletteBuyIn,
  RouletteBet,
  RouletteDoneBetting,
  RoulettePayout
)


class RoulettePlayer(GamePlayer):
  def __init__(self, name):
    super().__init__(name)

  def on_state_changed(self, game, new_state, prev_state, action):
    if action.action_type == RouletteActionType.SPIN:
      print(f'Wheel spun, result is {new_state.spin}!')
    if action.action_type == RouletteActionType.PAYOUT:
      print(f'Game Chips: {new_state.chips}')

  def buy_in(self, game):
    buyin_action = RouletteBuyIn(self, 500)
    game.handle_action(buyin_action)

  def generate_bet(self, game):
    builder = BetBuilder(game.state.table, game.state.wheel)
    bet = builder.make_corner_bet(4, 100)
    return bet

  def place_bet(self, game):
    bet = self.generate_bet(game)
    bet_action = RouletteBet(self, bet)
    print(f'Placing bet {bet}')
    game.handle_action(bet_action)

  def done_betting(self, game):
    done_action = RouletteDoneBetting(self)
    game.handle_action(done_action)

  def play(self, game):
    self.buy_in(game)
    self.place_bet(game)
    self.done_betting(game)