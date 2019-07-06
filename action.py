from copy import deepcopy
from enum import IntEnum
from game import GameAction
from state import (
  RouletteInitialState,
  RouletteBetState, 
  RouletteSpinState,
  RouletteEndState,
)


class RouletteActionType(IntEnum):
  BUY_IN = 0
  START = 1
  BET = 2
  SPIN = 3
  PAYOUT = 4
  END = 5


class RouletteBuyIn(GameAction):
  def __init__(self, player, chips):
    super().__init__(RouletteActionType.BUY_IN, player)
    self.chips = chips

  def accept(self, state):
    return RouletteInitialState(
      table=state.table, wheel=state.wheel,
      players=[*state.players, self.player],
      chips={**state.chips, self.player: self.chips}
    )


class RouletteStart(GameAction):
  def __init__(self, player):
    super().__init__(RouletteActionType.START, player)

  def accept(self, state):
    return RouletteBetState(
      table=state.table, wheel=state.wheel,
      players=state.players, chips=state.chips
    )


class RouletteBet(GameAction):
  def __init__(self, player, bet):
    super().__init__(RouletteActionType.BET, player)
    self.bet = bet

  def accept(self, state):
    new_chips = deepcopy(state.chips)
    new_bets = deepcopy(state.bets)
    bet_list = new_bets.setdefault(self.player, [])
    bet_list.append(self.bet)
    new_chips[self.player] -= self.bet.chips

    return RouletteBetState(
      table=state.table, wheel=state.wheel,
      players=state.players, chips=new_chips,
      bets=new_bets
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
    spin_result = state.spin_result
    new_chips = deepcopy(state.chips)

    # Assign chips to players based on bets.
    for player, bets in state.bets.items():
      for bet in bets:
        if spin_result in bet.numbers:
          odds = bet.odds
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