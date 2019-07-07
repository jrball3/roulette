from wheel import RouletteWheel
from table import RouletteTable
from exceptions import InvalidBetException


class Odds():
  def __init__(self, value, for_to=False):
    self.value = value
    # False = for, True = to
    # i.e. "2 for 1" vs "2 to 1".
    self.for_to = for_to 


class BetType(Enum):
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


class BetBuilder():
  def __init__(self, table, wheel):
    self.table = table
    self.wheel = wheel

  def make_straight_bet(self, number, chips):
    if self.table.has_Tablenumber(number):
      raise InvalidBetException('number {number} not on table.')
    if self.wheel.has_Tablenumber(number):
      raise InvalidBetException('number {number} not on wheel.')
    return Bet(BetType.STRAIGHT, number)

  def make_split_bet(self, numbers, chips):
    if len(numbers) != 2:
      raise InvalidBetException('A split bet must have 2 numbers')
    if not self.table.is_adjacent(numbers[0], numbers[1]):
      raise InvalidBetException('numbers {num1} and {num2} are not adjacent.')
    return Bet(BetType.SPLIT, numbers, chips)

  def make_top_bet(self, chips):
    numbers = self.table.get_top_numbers()
    return Bet(BetType.TOP, numbers, chips)

  def make_street_bet(self, numbers, chips):
    if not self.table.is_street(numbers):
      raise InvalidBetException('numbers {numbers} are not a street.')
    return Bet(BetType.STREET, numbers, chips)

  def make_line_bet(self, numbers, chips):
    if not self.table.is_line(numbers):
      raise InvalidBetException('numbers {numbers} are not a line.')
    return Bet(BetType.LINE, numbers, chips)

  def make_corner_bet(self, numbers, chips):
    if not self.table.is_corner(numbers, chips):
      raise InvalidBetException('numbers {numbers} are not a corner.')
    return Bet(BetType.CORNER, numbers, chips)

  def make_column_bet(self, num_column, chips):
    if not self.table.is_column(num_column):
      raise InvalidBetException('{num_column} is not a valid column.')
    numbers = self.table.get_column_numbers(num_column)
    return Bet(BetType.COLUMN, numbers, chips)

  def make_even_bet(self, chips):
    numbers = self.table.get_even_numbers()
    return Bet(BetType.EVEN_ODD, numbers, chips)

  def make_odd_bet(self, chips):
    numbers = self.table.get_odd_numbers()
    return Bet(BetType.EVEN_ODD, numbers, chips)

  def make_red_bet(self, chips):
    numbers = self.table.get_red_numbers()
    return Bet(BetType.RED_BLACK, numbers, chips)

  def make_black_bet(self, chips):
    numbers = self.table.get_black_numbers()
    return Bet(BetType.RED_BLACK, numbers, chips)

  def make_low_bet(self, chips):
    numbers = self.table.get_low_numbers()
    return Bet(BetType.LOW_HIGH, numbers, chips)

  def make_high_bet(self, chips):
    numbers = self.table.get_high_numbers()
    return Bet(BetType.LOW_HIGH, numbers, chips)