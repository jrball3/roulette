from copy import deepcopy
from enum import IntEnum

from roulette.common import RouletteActionType
from roulette.game import GameAction
from roulette.state import (
  RouletteInitialState,
  RouletteBetState, 
  RouletteSpinState,
  RouletteEndState,
)


class RouletteBuyIn(GameAction):
  def __init__(self, player, chips):
    super().__init__(RouletteActionType.BUY_IN, player)
    self.chips = chips

  def accept(self, state):
    return RouletteInitialState(
      table=state.table, wheel=state.wheel,
      players=[*state.players, self.player],
      chips={**state.chips, self.player.name: self.chips}
    )


class RouletteBet(GameAction):
  def __init__(self, player, bet):
    super().__init__(RouletteActionType.BET, player)
    self.bet = bet

  def accept(self, state):
    new_chips = deepcopy(state.chips)
    if hasattr(state, 'bets'):
      new_bets = deepcopy(state.bets)
    else:
      new_bets = {}
    bet_list = new_bets.setdefault(self.player.name, [])
    bet_list.append(self.bet)
    new_chips[self.player.name] -= self.bet.chips

    return RouletteBetState(
      table=state.table, wheel=state.wheel,
      players=state.players, chips=new_chips,
      bets=new_bets
    )


class RouletteDoneBetting(GameAction):
  def __init__(self, player):
    super().__init__(RouletteActionType.DONE_BETTING, player)

  def accept(self, state):
    new_done = deepcopy(state.done_betting)
    new_done.add(self.player.name)

    return RouletteBetState(
      table=state.table, wheel=state.wheel,
      players=state.players, chips=state.chips,
      bets=state.bets, done_betting=new_done,
    )


class RouletteSpin(GameAction):
  def __init__(self, player):
    super().__init__(RouletteActionType.SPIN, player)

  def accept(self, state):
    spin_result = state.wheel.spin()
    return RouletteSpinState(
        table=state.table, wheel=state.wheel,
        players=state.players, chips=state.chips,
        bets=state.bets, spin=spin_result,
      )


class RoulettePayout(GameAction):
  def __init__(self, dealer):
    super().__init__(RouletteActionType.PAYOUT, dealer)

  def accept(self, state):
    spin_result = state.spin
    new_chips = deepcopy(state.chips)

    # Assign chips to players based on bets.
    for player, bets in state.bets.items():
      for bet in bets:
        if spin_result in bet.numbers:
          odds = state.odds[bet.bet_type]
          payout = bet.chips * odds.value
          if not odds.for_to:
            payout += bet.chips
          new_chips[player] += payout

    # Return to initial state.
    return RouletteInitialState(
      table=state.table, wheel=state.wheel, 
      players=state.players, chips=new_chips,
    )


class RouletteEnd(GameAction):
  def __init__(self, player):
    super().__init__(RouletteActionType.END, player)

  def accept(self, state):
    return RouletteEndState(
      table=state.table,
      wheel=state.wheel
    )