from roulette.factory import RouletteFactory
from roulette.dealer import RouletteDealer
from roulette.player import RoulettePlayer


def main():
  dealer = RouletteDealer('dealer')
  player = RoulettePlayer('player')
  game = RouletteFactory() \
    .with_name('Roulette') \
    .with_game_id(1) \
    .with_dealer(dealer) \
    .with_players([player]) \
    .build()
  player.play(game)


if __name__ == '__main__':
  main()