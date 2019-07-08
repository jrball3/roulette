from enum import IntEnum

class NumberColor(IntEnum):
  RED = 0
  BLACK = 1
  GREEN = 2


class RouletteActionType(IntEnum):
  BUY_IN = 0
  START = 1
  BET = 2
  DONE_BETTING = 3
  SPIN = 4
  PAYOUT = 5
  END = 6