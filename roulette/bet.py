from enum import IntEnum

from roulette.exceptions import InvalidBetException
from roulette.wheel import RouletteWheel
from roulette.table import RouletteTable


class Odds():
  def __init__(self, value, for_to=False):
    self.value = value
    # False = for, True = to
    # i.e. "2 for 1" vs "2 to 1".
    self.for_to = for_to 


class BetType(IntEnum):
  STRAIGHT = 0
  SPLIT = 1
  STREET = 2
  CORNER = 3
  LINE = 4
  TOP = 5
  COLUMN = 6
  RANGE = 7
  LOW_HIGH = 8
  RED_BLACK = 9
  EVEN_ODD = 10


class Bet():
  def __init__(self, bet_type, numbers, chips):
    self.bet_type = bet_type
    self.numbers = numbers
    self.chips = chips

  def __str__(self):
    return f"{self.bet_type.name} Bet of {self.chips} chips on numbers {self.numbers}"


class BetBuilder():
  def __init__(self, table, wheel):
    self.table = table
    self.wheel = wheel

  def make_straight_bet(self, number, chips):
    if not self.table.has_number(number):
      raise InvalidBetException('number {number} not on table.')
    if not self.wheel.has_number(number):
      raise InvalidBetException('number {number} not on wheel.')
    return Bet(BetType.STRAIGHT, [number], chips)

  def make_split_bet(self, num1, num2, chips):
    if not self.table.is_adjacent(num1, num2):
      raise InvalidBetException('numbers {num1} and {num2} are not adjacent.')
    return Bet(BetType.SPLIT, [num1, num2], chips)

  def make_top_bet(self, chips):
    numbers = self.table.get_top_numbers()
    numbers = list(map(lambda n: n.string(), numbers))
    return Bet(BetType.TOP, numbers, chips)

  def make_street_bet(self, num_street, chips):
    numbers = self.table.get_street_numbers(num_street)
    numbers = list(map(lambda n: n.string(), numbers))
    return Bet(BetType.STREET, numbers, chips)

  def make_line_bet(self, num_line, chips):
    numbers = self.table.get_line_numbers(num_line)
    numbers = list(map(lambda n: n.string(), [*numbers[0], *numbers[1]]))
    return Bet(BetType.LINE, numbers, chips)

  def make_corner_bet(self, num_corner, chips):
    numbers = self.table.get_corner_numbers(num_corner)
    numbers = list(map(lambda n: n.string(), [*numbers[0], *numbers[1]]))
    return Bet(BetType.CORNER, numbers, chips)

  def make_column_bet(self, num_column, chips):
    numbers = self.table.get_column_numbers(num_column)
    numbers = list(map(lambda n: n.string(), numbers))
    return Bet(BetType.COLUMN, numbers, chips)

  def make_even_bet(self, chips):
    numbers = self.table.get_even_numbers()
    numbers = list(map(lambda n: n.string(), numbers))
    return Bet(BetType.EVEN_ODD, numbers, chips)

  def make_odd_bet(self, chips):
    numbers = self.table.get_odd_numbers()
    numbers = list(map(lambda n: n.string(), numbers))
    return Bet(BetType.EVEN_ODD, numbers, chips)

  def make_red_bet(self, chips):
    numbers = self.table.get_red_numbers()
    numbers = list(map(lambda n: n.string(), numbers))
    return Bet(BetType.RED_BLACK, numbers, chips)

  def make_black_bet(self, chips):
    numbers = self.table.get_black_numbers()
    numbers = list(map(lambda n: n.string(), numbers))
    return Bet(BetType.RED_BLACK, numbers, chips)

  def make_low_bet(self, chips):
    numbers = self.table.get_low_numbers()
    numbers = list(map(lambda n: n.string(), numbers))
    return Bet(BetType.LOW_HIGH, numbers, chips)

  def make_high_bet(self, chips):
    numbers = self.table.get_high_numbers()
    numbers = list(map(lambda n: n.string(), numbers))
    return Bet(BetType.LOW_HIGH, numbers, chips)