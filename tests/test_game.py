import os
import sys

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(DIR_PATH)
sys.path.append(ROOT_PATH)

import unittest
from copy import deepcopy

from roulette.game import Game, GameAction, GameState, GameStateListener
from roulette.exceptions import InvalidActionException


class MockGameListener(GameStateListener):
  def __init__(self):
    self.last_event = None

  def on_state_changed(self, game):
    self.last_event = game


class MockGameAction(GameAction):
  def __init__(self, modify_state, action_type, player):
    super().__init__(action_type, player)
    self.modify_state = modify_state
    
  def accept(self, game_state):
    if self.modify_state:
      return deepcopy(game_state)
    return super().accept(game_state)


class MockGameState(GameState):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def valid_actions(self):
    return [
      *super().valid_actions(),
      'test',
    ] 


class GameTests(unittest.TestCase):
  def test_should_create_game(self):
    game = Game()

  def test_should_register_listener(self):
    lst = MockGameListener()
    game = Game()
    game.register_listener(lst)
    self.assertTrue(lst in game.listeners)

  def test_should_accept_action(self):
    game = Game(start_state=MockGameState())
    player = MockGameListener()
    game.register_listener(player)
    action = MockGameAction(False, 'test', player)
    game.handle_action(action)

  def test_should_reject_action(self):
    game = Game(start_state=MockGameState())
    player = MockGameListener()
    game.register_listener(player)
    action = MockGameAction(False, 'badtest', player)
    try:
      game.handle_action(action)
    except InvalidActionException as e:
      return
    raise ValueError('FAIL')

  def test_should_not_notify_listener(self):
    game = Game(start_state=MockGameState())
    player = MockGameListener()
    game.register_listener(player)
    action = MockGameAction(False, 'test', player)
    game.handle_action(action)
    self.assertTrue(player.last_event is None)

  def test_should_notify_listener(self):
    game = Game(start_state=MockGameState())
    player = MockGameListener()
    game.register_listener(player)
    action = MockGameAction(True, 'test', player)
    game.handle_action(action)
    self.assertTrue(player.last_event is not None)