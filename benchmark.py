import yaml
import numpy as np

from src.game import Game
from src.agent import RandomAgent

with open('cfg.yml', 'r') as f:
    cfg = yaml.safe_load(f)

player = RandomAgent()

N = 100000

report = {
    'win': np.zeros(N),
    'score': np.zeros(N),
    'n_invalid_moves': np.zeros(N),
    'n_steps': np.zeros(N),
}

for i in range(N):
    board = Game(cfg['board'])
    env = board.get_env()
    while True:
        move = player.move(env)
        env = board.update(move)
        if env['lost']:
            break
    report['win'][i] = env['won']
    report['score'][i] = env['score']
    report['n_invalid_moves'][i] = env['n_invalid_moves']
    report['n_steps'][i] = env['n_steps']

print(
    '[INFO] Win rate: {:.04f} +/- {:.04f}'.format(
        report['win'].mean(),
        report['win'].std(),
    )
)
print(
    '[INFO] Avg score: {:.02f} +/- {:.02f}'.format(
        report['score'].mean(),
        report['score'].std(),
    )
)
print(
    '[INFO] Avg length: {:.02f} +/- {:.02f}'.format(
        report['n_steps'].mean(),
        report['n_steps'].std(),
    )
)
print(
    '[INFO] Avg length (w/o invalid moves): {:.04f} +/- {:.04f}'.format(
        (report['n_steps'] - report['n_invalid_moves']).mean(),
        (report['n_steps'] - report['n_invalid_moves']).std(),
    )
)
