import yaml

from src.game import Game
from src.gui import GUI

with open('cfg.yml', 'r') as f:
    cfg = yaml.safe_load(f)

game = Game(cfg['board'])
gui = GUI(game, 128)

gui.run()
