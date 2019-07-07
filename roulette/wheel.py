import random
from enum import IntEnum

from roulette.common import NumberColor


class WheelBin():
  def __init__(self, number=None, color=None):
    self.number = number
    self.color = color


class RouletteWheel():
  def __init__(self):
    self.bins = {
      '0': WheelBin('0', NumberColor.GREEN),
      '00': WheelBin('00', NumberColor.GREEN),
    }
    for num in range(1, 37):
      color = NumberColor.RED if num % 2 == 0 else NumberColor.BLACK
      self.bins[str(num)] = WheelBin(number = str(num), color = color)

  def spin(self):
    return random.choice(list(self.bins.values()))

  def has_number(self, number):
    return number in self.bins