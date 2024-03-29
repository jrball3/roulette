from enum import IntEnum

from roulette.game import GameState, InvalidActionException
from roulette.common import RouletteActionType
from roulette.table import RouletteTable
from roulette.wheel import RouletteWheel
from roulette.bet import Odds, BetType


class RouletteBaseState(GameState):
  def __init__(self, table=None, wheel=None, players=None,
               chips=None, odds=None):
    self.table = table or RouletteTable()
    self.wheel = wheel or RouletteWheel()
    self.odds = odds or {
      BetType.STRAIGHT: Odds(35),
      BetType.SPLIT: Odds(17),
      BetType.STREET: Odds(11),
      BetType.CORNER: Odds(8),
      BetType.TOP: Odds(6),
      BetType.LINE: Odds(5),
      BetType.COLUMN: Odds(2),
      BetType.RANGE: Odds(2),
      BetType.LOW_HIGH: Odds(1),
      BetType.RED_BLACK: Odds(1),
      BetType.EVEN_ODD: Odds(1),
    }
    self.players = players or []
    self.chips = chips or {}

  def valid_actions(self):
    return [
      *super().valid_actions(),
      RouletteActionType.END
    ]


class RouletteInitialState(RouletteBaseState):
  def __init__(self, table=None, wheel=None, players=None,
               chips=None, odds=None):
    super().__init__(table=table, wheel=wheel, players=players,
                     chips=chips, odds=odds)

  def valid_actions(self):
    return [
      *super().valid_actions(),
      RouletteActionType.BUY_IN,
      RouletteActionType.START,
      RouletteActionType.BET,
    ]


class RouletteBetState(RouletteBaseState):
  def __init__(self, table=None, wheel=None, players=None,
               chips=None, odds=None, bets=None, done_betting=None):
    super().__init__(table=table, wheel=wheel, players=players,
                     chips=chips, odds=odds)
    self.bets = bets or {}
    self.done_betting = done_betting or set()

  def valid_actions(self):
    return [
      *super().valid_actions(),
      RouletteActionType.BET,
      RouletteActionType.DONE_BETTING,
      RouletteActionType.SPIN,
    ]


class RouletteSpinState(RouletteBaseState):
  def __init__(self, table=None, wheel=None, players=None,
               chips=None, odds=None, bets=None, spin=None):
    super().__init__(table=table, wheel=wheel, players=players,
                     chips=chips, odds=odds)
    self.players = players or []
    self.chips = chips or {}
    self.bets = bets or {}
    self.spin = spin

  def valid_actions(self):
    return [
      *super().valid_actions(),
      RouletteActionType.PAYOUT,
    ]


class RouletteEndState(RouletteBaseState):
  def __init__(self, table=None, wheel=None, players=None,
               chips=None):
    super().__init__(table=table, wheel=wheel, players=players,
                     chips=chips)
    self.players = players or []
    self.chips = chips or {}