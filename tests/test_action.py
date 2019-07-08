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
  RouletteBet,
  RouletteDoneBetting,
  RouletteSpin,
  RoulettePayout,
  RouletteEnd,
)
from roulette.bet import BetBuilder
from roulette.wheel import RouletteWheel
from roulette.table import RouletteTable
from roulette.game import GamePlayer


class ActionTests(unittest.TestCase):
  def test_buy_in(self):
    before = RouletteInitialState()
    player = GamePlayer('1')
    chips = 500
    action = RouletteBuyIn(player, chips)
    after = action.accept(before)
    self.assertTrue(player in after.players)
    self.assertEqual(after.chips[player.name], chips)

  def test_bet(self):
    player = GamePlayer('1')
    balance = 500
    before = RouletteBetState(chips={player.name: balance})
    builder = BetBuilder(before.table, before.wheel)
    bet = builder.make_straight_bet('10', 50)
    action = RouletteBet(player, bet)
    after = action.accept(before)
    self.assertTrue(isinstance(after, RouletteBetState))
    self.assertEqual(before.table, after.table)
    self.assertEqual(before.wheel, after.wheel)
    self.assertEqual(before.players, after.players)
    self.assertEqual(before.done_betting, after.done_betting)
    self.assertEqual(after.chips[player.name], 450)
    self.assertTrue(bet in after.bets[player.name])

  def test_done_betting(self):
    player = GamePlayer('1')
    balance = 500
    before = RouletteBetState(chips={player.name: balance})
    action = RouletteDoneBetting(player)
    after = action.accept(before)
    self.assertTrue(isinstance(after, RouletteBetState))
    self.assertEqual(before.table, after.table)
    self.assertEqual(before.wheel, after.wheel)
    self.assertEqual(before.players, after.players)
    self.assertTrue(player.name in after.done_betting)


  def test_spin(self):
    player = GamePlayer('1')
    balance = 500
    before = RouletteBetState(chips={player.name: balance})
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
    player = GamePlayer('1')
    dealer = GamePlayer('2')
    balance = 450
    table = RouletteTable()
    wheel = RouletteWheel()
    builder = BetBuilder(table, wheel)
    bet = builder.make_straight_bet('10', 50)
    before = RouletteSpinState(
      table=table, wheel=wheel,
      chips={player.name: balance},
      bets={player.name: [bet]},
      spin='10')
    action = RoulettePayout(dealer)
    after = action.accept(before)
    self.assertTrue(isinstance(after, RouletteInitialState))
    self.assertEqual(before.table, after.table)
    self.assertEqual(before.wheel, after.wheel)
    self.assertEqual(before.players, after.players)
    self.assertEqual(after.chips[player.name], 50 + 50 * 35 + balance)

  def test_end(self):
    before = RouletteInitialState()
    player = GamePlayer('1')
    action = RouletteEnd(player)
    after = action.accept(before)
    self.assertTrue(isinstance(after, RouletteEndState))
    self.assertEqual(before.table, after.table)
    self.assertEqual(before.wheel, after.wheel)
    self.assertEqual(before.players, after.players)
    self.assertEqual(before.chips, after.chips)