from math import ceil
from copy import deepcopy

from common import NumberColor


class TableNumber():
  def __init__(self, number, color, above=None, below=None,
               left=None, right=None):
    self.color = color
    self.number = number
    self.above = None
    self.below = None
    self.left = None
    self.right = None

  def string(self):
    return self.number

  def value(self):
    return int(self.number)

  def even(self):
    return self.value() % 2 == 0

  def odd(self):
    return not self.even()

  def __str__(self):
    return f"{self.color.name} Number: {self.string()}"


def color_for_number(num_str):
  if num_str in ['0', '00']:
    return NumberColor.GREEN
  if int(num_str) % 2 == 0:
    return NumberColor.RED
  return NumberColor.BLACK


class RouletteTable():
  def __init__(self):
    self.row_count = 12
    self.row_length = 3
    self.line_height = 2
    self.corner_size = 2
    self.num_count = int(self.row_count * self.row_length)
    self.line_count = int(self.row_count / self.line_height)
    self.min_number = 0
    self.max_number = self.num_count + 1
    self.mid_number = (self.max_number - self.min_number) / 2.0

    # Build the main streets grid and inside map
    self.number_map = {}
    self.streets = []
    for row_num in range(self.row_count):
      street = []
      for col_num in range(self.row_length):
        value = int(self.row_length * row_num + col_num) + 1
        num = TableNumber(value, color_for_number(str(value)))
        street.append(num)
        self.number_map[value] = num
      self.streets.append(street)

    # Link all numbers together so we can easily
    # find adjacents
    for ci, row in enumerate(self.streets):
      for ni, num in enumerate(row):
        if ci > 0:
          num.above = self.streets[ci - 1][ni]
        if ci < len(self.streets) - 1:
          num.below = self.streets[ci + 1][ni]
        if ni > 0:
          num.left = self.streets[ci][ni - 1]
        if ni < len(row) - 1:
          num.right = row[ni + 1]

    self.number_map['0'] = TableNumber('0', color_for_number('0'))
    self.number_map['00'] = TableNumber('00', color_for_number('00'))

    self.top = [
      self.number_map['0'], self.number_map['00'],
      self.number_map['1'], self.number_map['2'],
      self.number_map['3']
    ]

    # Build all of the lines from the streets
    self.lines = []
    for line_num in range(self.line_count):
      line_start = self.line_height * line_num
      line_end = line_start + 2
      line = self.streets[line_start:line_end]
      self.lines.append(line)

    # Build all of the corners from the streets
    self.corners = []
    for row in range(self.row_count - self.corner_size + 1):
      for corner_start in range(self.row_length - self.corner_size + 1):
        corner = []
        for ri in range(row, row + self.corner_size):
          r = self.streets[ri]
          corner_row = r[corner_start:corner_start + self.corner_size]
          corner.append(corner_row)
        self.corners.append(corner)
    
    # Build all of the columns from the streets
    self.columns = []
    for col in range(self.row_length):
      column = []
      for row in self.streets:
        column.append(row[col])
      self.columns.append(column)

  def has_number(self, number):
    return number in self.number_map

  def is_adjacent(self, num1, num2):
    n1 = self.number_map.get(num1)
    n2 = self.number_map.get(num2)
    if n1 is not None and n2 is not None: 
      if n2 in [n1.left, n1.above, n1.below, n1.right]:
        return True
    return False

  def get_column_numbers(self, num_column):
    return deepcopy(self.columns[num_column])

  def get_line_numbers(self, num_line):
    return deepcopy(self.lines[num_line])

  def get_street_numbers(self, num_street):
    return deepcopy(self.streets[num_street])

  def get_corner_numbers(self, num_corner):
    return deepcopy(self.corners[num_corner])
  
  def get_top_numbers(self):
    return deepcopy(self.top)

  def get_columns_numbers(self, num_column):
    raise deepcopy(self.columns[num_column])

  def get_even_numbers(self):
    return deepcopy([x for x in self.number_map.values() if x.even()])
  
  def get_odd_numbers(self):
    return deepcopy([x for x in self.number_map.values() if x.odd()])

  def get_red_numbers(self):
    return deepcopy([x for x in self.number_map.values() if x.color == NumberColor.RED])
  
  def get_black_numbers(self):
    return deepcopy([x for x in self.number_map.values() if x.color == NumberColor.BLACK])

  def get_low_numbers(self):
    return deepcopy([x for x in self.number_map.values() if x.value() <= self.mid_number])

  def get_high_numbers(self):
    return deepcopy([x for x in self.number_map.values() if x.value() >= self.mid_number])