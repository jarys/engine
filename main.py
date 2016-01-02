import game
from player import Player
import rule_eat
import rule_generate_food

Player().add()
rule_generate_food.add()
rule_eat.add()

game.run()