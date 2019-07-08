import random
from enum import IntEnum

from roulette.common import NumberColor


class RouletteWheel():
  def __init__(self):
    self.bins = {'0', '00'}
    for num in range(1, 37):
      self.bins.add(str(num))

  def spin(self):
    return random.choice(list(self.bins))

  def has_number(self, number):
    return number in self.bins