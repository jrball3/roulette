from exceptions import InvalidActionException, UnhandledActionException


class GameState():
  def valid_actions(self):
    return []

  def check_action(self, action):
    if action.action_type not in self.valid_actions():
      raise InvalidActionException('{action} is invalid for {self}')


class GameAction():
  def __init__(self, action_type, player):
    self.action_type = action_type
    self.player = player

  def accept(self, game_state):
    return game_state


class GameStateListener():
  def on_state_changed(self, game):
    pass


class Game():
  def __init__(self, name=None, game_id=None, start_state=None):
    self.name = name or game_id
    self.game_id = game_id
    self.state = start_state or GameState()
    self.listeners = set()

  def register_listener(self, listener):
    self.listeners.add(listener)

  def handle_action(self, action):
    old_state = self.state
    old_state.check_action(action)
    new_state = action.accept(self.state)
    self.state = new_state
    if old_state is not self.state:
      for ls in self.listeners:
        ls.on_state_changed(self)