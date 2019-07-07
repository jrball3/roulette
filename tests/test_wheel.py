import os
import sys

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(DIR_PATH)
sys.path.append(ROOT_PATH)

import unittest
from roulette.wheel import RouletteWheel

class WheelTests(unittest.TestCase):
  
  def test_should_create_wheel(self):
    wheel = RouletteWheel()

  def test_should_spin_wheel(self):
    wheel = RouletteWheel()
    result = wheel.spin()
    self.assertTrue(result is not None)
    self.assertTrue(isinstance(result.number, str))
    self.assertTrue(result.color is not None)