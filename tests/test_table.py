import os
import sys

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(DIR_PATH)
sys.path.append(ROOT_PATH)

import unittest
from roulette.table import RouletteTable


class TableTests(unittest.TestCase):
  
  @classmethod
  def setUpClass(cls):
    cls.table = RouletteTable()

  def test_should_create_table(self):
    self.assertTrue(self.table is not None)

  def test_should_create_all_numbers(self):
    nums = ['0', '00', *[str(x) for x in range(1, 37)]]

    for n in nums[:3]:
      self.assertTrue(self.table.has_number(n))
      self.assertTrue(n in [x.string() for x in self.table.get_top_numbers()])

    for n in nums[2:]:
      self.assertTrue(self.table.has_number(n))

      found = False
      for row in self.table.streets:
        for col in row:
          if col.string() == n:
            found = True
            break

      self.assertTrue(found)

  def test_should_create_all_lines(self):
    self.assertEqual(len(self.table.lines), 6)
    for line in self.table.lines:
      self.assertTrue(len(line[0]) == 3 and len(line[1]) == 3)

  def test_should_create_all_corners(self):
    self.assertEqual(len(self.table.corners), 22)
    for corner in self.table.corners:
      self.assertTrue(len(corner[0]) == 2 and len(corner[1]) == 2)
  
  def test_should_create_all_columns(self):
    self.assertEqual(len(self.table.columns), 3)
    for column in self.table.columns:
      self.assertEqual(len(column), 12)

  def test_should_show_adjacent(self):
    self.assertTrue(self.table.is_adjacent('1', '2'))
    self.assertTrue(self.table.is_adjacent('20', '23'))

  def test_should_show_not_adjacent(self):
    self.assertFalse(self.table.is_adjacent('20', '22'))
    self.assertFalse(self.table.is_adjacent('1', '3'))

  def test_should_get_columns_numbers(self):
    self.assertEqual(len(self.table.get_column_numbers(0)), 12)
    self.assertEqual(len(self.table.get_column_numbers(1)), 12)
    self.assertEqual(len(self.table.get_column_numbers(2)), 12)

  def test_should_get_even_numbers(self):
    evens = self.table.get_even_numbers()
    self.assertEqual(len(evens), 18)
    self.assertTrue(12 in map(lambda x: x.value(), evens))

  def test_should_get_odd_numbers(self):
    odds = self.table.get_odd_numbers()
    self.assertEqual(len(odds), 18)
    self.assertTrue(15 in map(lambda x: x.value(), odds))

  def test_should_get_red_numbers(self):
    reds = self.table.get_red_numbers()
    self.assertEqual(len(reds), 18)
    self.assertTrue(16 in map(lambda x: x.value(), reds))

  def test_should_get_black_numbers(self):
    blacks = self.table.get_black_numbers()
    self.assertEqual(len(blacks), 18)
    self.assertTrue(15 in map(lambda x: x.value(), blacks))

  def test_should_get_low_numbers(self):
    lows = self.table.get_low_numbers()
    self.assertEqual(len(lows), 18)
    self.assertTrue(11 in map(lambda x: x.value(), lows))

  def test_should_get_high_numbers(self):
    highs = self.table.get_high_numbers()
    self.assertEqual(len(highs), 18)
    self.assertTrue(27 in map(lambda x: x.value(), highs))