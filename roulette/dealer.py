from roulette.game import GamePlayer
from roulette.action import RoulettePayout, RouletteSpin
from roulette.state import RouletteBetState, RouletteSpinState


class RouletteDealer(GamePlayer):
  def __init__(self, name):
    return super().__init__(name)
    
  def on_state_changed(self, game, new_state, prev_state, action):
    state = game.state
    if isinstance(state, RouletteBetState):
      player_names = set(map(lambda p: p.name, state.players))
      done_players = set(state.done_betting)
      if player_names != done_players:
        return
      spin_action = RouletteSpin(self)
      game.handle_action(spin_action)
    elif isinstance(state, RouletteSpinState):
      pay_action = RoulettePayout(self)
      game.handle_action(pay_action)