import os
import sys

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(DIR_PATH)
sys.path.append(ROOT_PATH)

import unittest
from tests.test_game import (
  MockGameListener,
  MockGameAction,
  MockGameState,
)
from roulette.wheel import RouletteWheel
from roulette.table import RouletteTable
from roulette.game import Game
from roulette.bet import BetBuilder, BetType
from roulette.exceptions import InvalidBetException


class BetBuilderTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.table = RouletteTable()
    cls.wheel = RouletteWheel()
    cls.builder = BetBuilder(table=cls.table,
                             wheel=cls.wheel)
  
  def test_should_make_straight_bet(self):
    bet = self.builder.make_straight_bet('10', 50)
    self.assertEqual(bet.numbers, ['10'])
    self.assertEqual(bet.bet_type, BetType.STRAIGHT)
    self.assertEqual(bet.chips, 50)

  def test_should_not_make_straight_bet(self):
    try:
      bet = self.builder.make_straight_bet('100', 50)
    except InvalidBetException as e:
      return
    raise ValueError('Fail')

  def test_should_make_split_bet(self):
    bet = self.builder.make_split_bet('10', '11', 50)
    self.assertEqual(bet.bet_type, BetType.SPLIT)
    self.assertEqual(bet.chips, 50)
    self.assertEqual(bet.numbers, ['10', '11'])

  def test_should_not_make_straight_bet(self):
    try:
      bet = self.builder.make_split_bet('10', '12', 50)
    except InvalidBetException as e:
      return
    raise ValueError('Fail')

  def test_should_make_top_bet(self):
    bet = self.builder.make_top_bet(50)
    self.assertEqual(bet.bet_type, BetType.TOP)
    self.assertEqual(bet.chips, 50)
    exp_nums = list(map(lambda n: n.string(), self.table.get_top_numbers()))
    self.assertEqual(bet.numbers, exp_nums)

  def test_should_make_street_bet(self):
    bet = self.builder.make_street_bet(2, 50)
    self.assertEqual(bet.bet_type, BetType.STREET)
    self.assertEqual(bet.chips, 50)
    exp_nums = list(map(lambda n: n.string(), 
                        self.table.get_street_numbers(2)))
    self.assertEqual(bet.numbers, exp_nums)

  def test_should_make_line_bet(self):
    bet = self.builder.make_line_bet(2, 50)
    self.assertEqual(bet.bet_type, BetType.LINE)
    self.assertEqual(bet.chips, 50)
    nums = self.table.get_line_numbers(2)
    exp_nums = list(map(lambda n: n.string(), [*nums[0], *nums[1]]))
    self.assertEqual(bet.numbers, exp_nums)

  def test_should_make_corner_bet(self):
    bet = self.builder.make_corner_bet(2, 50)
    self.assertEqual(bet.bet_type, BetType.CORNER)
    self.assertEqual(bet.chips, 50)
    nums = self.table.get_corner_numbers(2)
    exp_nums = list(map(lambda n: n.string(), [*nums[0], *nums[1]]))
    self.assertEqual(bet.numbers, exp_nums)

  def test_should_make_column_bet(self):
    bet = self.builder.make_column_bet(2, 50)
    self.assertEqual(bet.bet_type, BetType.COLUMN)
    self.assertEqual(bet.chips, 50)
    exp_nums = list(map(lambda n: n.string(), self.table.get_column_numbers(2)))
    self.assertEqual(bet.numbers, exp_nums)

  def test_should_make_even_bet(self):
    bet = self.builder.make_even_bet(50)
    self.assertEqual(bet.bet_type, BetType.EVEN_ODD)
    self.assertEqual(bet.chips, 50)
    exp_nums = list(map(lambda n: n.string(), self.table.get_even_numbers()))
    self.assertEqual(bet.numbers, exp_nums)

  def test_should_make_odd_bet(self):
    bet = self.builder.make_odd_bet(50)
    self.assertEqual(bet.bet_type, BetType.EVEN_ODD)
    self.assertEqual(bet.chips, 50)
    exp_nums = list(map(lambda n: n.string(), self.table.get_odd_numbers()))
    self.assertEqual(bet.numbers, exp_nums)

  def test_should_make_red_bet(self):
    bet = self.builder.make_red_bet(50)
    self.assertEqual(bet.bet_type, BetType.RED_BLACK)
    self.assertEqual(bet.chips, 50)
    exp_nums = list(map(lambda n: n.string(), self.table.get_red_numbers()))
    self.assertEqual(bet.numbers, exp_nums)

  def test_should_make_black_bet(self):
    bet = self.builder.make_black_bet(50)
    self.assertEqual(bet.bet_type, BetType.RED_BLACK)
    self.assertEqual(bet.chips, 50)
    exp_nums = list(map(lambda n: n.string(), self.table.get_black_numbers()))
    self.assertEqual(bet.numbers, exp_nums)

  def test_should_make_low_bet(self):
    bet = self.builder.make_low_bet(50)
    self.assertEqual(bet.bet_type, BetType.LOW_HIGH)
    self.assertEqual(bet.chips, 50)
    exp_nums = list(map(lambda n: n.string(), self.table.get_low_numbers()))
    self.assertEqual(bet.numbers, exp_nums)

  def test_should_make_high_bet(self):
    bet = self.builder.make_high_bet(50)
    self.assertEqual(bet.bet_type, BetType.LOW_HIGH)
    self.assertEqual(bet.chips, 50)
    exp_nums = list(map(lambda n: n.string(), self.table.get_high_numbers()))
    self.assertEqual(bet.numbers, exp_nums)