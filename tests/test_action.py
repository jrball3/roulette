import os
import sys

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(DIR_PATH)
sys.path.append(ROOT_PATH)

import unittest
from roulette.state import (
  RouletteInitialState,
  RouletteBetState,
  RouletteSpinState,
  RouletteEndState
)
from roulette.action import (
  RouletteBuyIn,
  RouletteStart,
  RouletteBet,
  RouletteSpin,
  RoulettePayout,
  RouletteEnd,
)
from roulette.bet import BetBuilder
from roulette.wheel import RouletteWheel
from roulette.table import RouletteTable


class ActionTests(unittest.TestCase):
  def test_buy_in(self):
    before = RouletteInitialState()
    player = 1
    chips = 500
    action = RouletteBuyIn(player, chips)
    after = action.accept(before)
    self.assertTrue(player in after.players)
    self.assertEqual(after.chips[player], chips)

  def test_start(self):
    before = RouletteInitialState()
    player = 1
    action = RouletteStart(player)
    after = action.accept(before)
    self.assertTrue(isinstance(after, RouletteBetState))
    self.assertEqual(before.table, after.table)
    self.assertEqual(before.wheel, after.wheel)
    self.assertEqual(before.players, after.players)
    self.assertEqual(before.chips, after.chips)

  def test_bet(self):
    player = 1
    balance = 500
    before = RouletteBetState(chips={player: balance})
    builder = BetBuilder(before.table, before.wheel)
    bet = builder.make_straight_bet('10', 50)
    action = RouletteBet(player, bet)
    after = action.accept(before)
    self.assertTrue(isinstance(after, RouletteBetState))
    self.assertEqual(before.table, after.table)
    self.assertEqual(before.wheel, after.wheel)
    self.assertEqual(before.players, after.players)
    self.assertEqual(after.chips[player], 450)
    self.assertTrue(bet in after.bets[player])

  def test_spin(self):
    player = 1
    balance = 500
    before = RouletteBetState(chips={player: balance})
    action = RouletteSpin(player)
    after = action.accept(before)
    self.assertTrue(isinstance(after, RouletteSpinState))
    self.assertEqual(before.table, after.table)
    self.assertEqual(before.wheel, after.wheel)
    self.assertEqual(before.players, after.players)
    self.assertEqual(before.chips, after.chips)
    self.assertEqual(before.bets, after.bets)
    self.assertIsNotNone(after.spin)

  def test_payout(self):
    player = 1
    dealer = 2
    balance = 450
    table = RouletteTable()
    wheel = RouletteWheel()
    builder = BetBuilder(table, wheel)
    bet = builder.make_straight_bet('10', 50)
    before = RouletteSpinState(
      table=table, wheel=wheel,
      chips={player: balance},
      bets={player: [bet]},
      spin='10')
    action = RoulettePayout(dealer)
    after = action.accept(before)
    self.assertTrue(isinstance(after, RouletteInitialState))
    self.assertEqual(before.table, after.table)
    self.assertEqual(before.wheel, after.wheel)
    self.assertEqual(before.players, after.players)
    self.assertEqual(after.chips[player], 50 + 50 * 35 + balance)

  def test_end(self):
    before = RouletteInitialState()
    player = 1
    action = RouletteEnd(player)
    after = action.accept(before)
    self.assertTrue(isinstance(after, RouletteEndState))
    self.assertEqual(before.table, after.table)
    self.assertEqual(before.wheel, after.wheel)
    self.assertEqual(before.players, after.players)
    self.assertEqual(before.chips, after.chips)