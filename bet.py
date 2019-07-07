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
  def __init__(self, bet_type, TableNumbers, chips):
    self.bet_type = bet_type
    self.TableNumbers = TableNumbers
    self.chips = chips


class BetBuilder():
  def __init__(self, table, wheel):
    self.table = table
    self.wheel = wheel

  def make_straight_bet(self, TableNumber, chips):
    if self.table.has_TableTableNumber(TableNumber):
      raise InvalidBetException('TableNumber {TableNumber} not on table.')
    if self.wheel.has_TableTableNumber(TableNumber):
      raise InvalidBetException('TableNumber {TableNumber} not on wheel.')
    return Bet(BetType.STRAIGHT, TableNumber)

  def make_split_bet(self, TableNumbers, chips):
    if len(TableNumbers) != 2:
      raise InvalidBetException('A split bet must have 2 TableNumbers')
    if not self.table.is_adjacent(TableNumbers[0], TableNumbers[1]):
      raise InvalidBetException('TableNumbers {num1} and {num2} are not adjacent.')
    return Bet(BetType.SPLIT, TableNumbers, chips)

  def make_top_bet(self, chips):
    TableNumbers = self.table.get_top_TableNumbers()
    return Bet(BetType.TOP, TableNumbers, chips)

  def make_street_bet(self, TableNumbers, chips):
    if not self.table.is_street(TableNumbers):
      raise InvalidBetException('TableNumbers {TableNumbers} are not a street.')
    return Bet(BetType.STREET, TableNumbers, chips)

  def make_line_bet(self, TableNumbers, chips):
    if not self.table.is_line(TableNumbers):
      raise InvalidBetException('TableNumbers {TableNumbers} are not a line.')
    return Bet(BetType.LINE, TableNumbers, chips)

  def make_corner_bet(self, TableNumbers, chips):
    if not self.table.is_corner(TableNumbers, chips):
      raise InvalidBetException('TableNumbers {TableNumbers} are not a corner.')
    return Bet(BetType.CORNER, TableNumbers, chips)

  def make_column_bet(self, num_column, chips):
    if not self.table.is_column(num_column):
      raise InvalidBetException('{num_column} is not a valid column.')
    TableNumbers = self.table.get_column_TableNumbers(num_column)
    return Bet(BetType.COLUMN, TableNumbers, chips)

  def make_even_bet(self, chips):
    TableNumbers = self.table.get_even_TableNumbers()
    return Bet(BetType.EVEN_ODD, TableNumbers, chips)

  def make_odd_bet(self, chips):
    TableNumbers = self.table.get_odd_TableNumbers()
    return Bet(BetType.EVEN_ODD, TableNumbers, chips)

  def make_red_bet(self, chips):
    TableNumbers = self.table.get_red_TableNumbers()
    return Bet(BetType.RED_BLACK, TableNumbers, chips)

  def make_black_bet(self, chips):
    TableNumbers = self.table.get_black_TableNumbers()
    return Bet(BetType.RED_BLACK, TableNumbers, chips)

  def make_low_bet(self, chips):
    TableNumbers = self.table.get_low_TableNumbers()
    return Bet(BetType.LOW_HIGH, TableNumbers, chips)

  def make_high_bet(self, chips):
    TableNumbers = self.table.get_high_TableNumbers()
    return Bet(BetType.LOW_HIGH, TableNumbers, chips)