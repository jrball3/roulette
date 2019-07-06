from game import NumberColor


class Number():
  def __init__(self, color, number):
    self.color = color
    self.number = number


class RouletteTable():
  def __init__(self):
    self.bins = {
      '0': Number('0', NumberColor.GREEN),
      '00': Number('00', NumberColor.GREEN),
    }
    for num in range(1, 37):
      color = NumberColor.RED if num % 2 == 0 else NumberColor.BLACK
      self.bins[str(num)] = Number(number = str(num), color = color)

  def has_number(self, number):
    return number in self.numbers

  def is_adjacent(self, num1, num2):
    raise NotImplementedError

  def is_column(self, num_column):
    raise NotImplementedError

  def is_street(self, numbers):
    raise NotImplementedError

  def is_line(self, numbers):
    raise NotImplementedError

  def is_corner(self, numbers):
    raise NotImplementedError
  
  def get_top_numbers(self):
    raise NotImplementedError

  def get_columns_numbers(self, column):
    raise NotImplementedError

  def get_even_numbers(self):
    raise NotImplementedError
  
  def get_odd_numbers(self):
    raise NotImplementedError

  def get_red_numbers(self):
    raise NotImplementedError
  
  def get_black_numbers(self):
    raise NotImplementedError

  def get_low_numbers(self):
    raise NotImplementedError

  def get_high_numbers(self):
    raise NotImplementedError