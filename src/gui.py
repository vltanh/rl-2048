from typing import Tuple

import pygame

from .game import Game


class GUI:
    def __init__(self, game: Game, tile_size: int) -> None:
        pygame.init()

        self.game = game
        self.tile_size = tile_size
        self.screen = pygame.display.set_mode(
            (self.game.ncols * self.tile_size,
             self.game.nrows * self.tile_size + 50)
        )
        self.font = pygame.font.Font(None, 32)
        self.score_label = pygame.Surface((0, 0))
        # Make score label background transparent
        self.score_label.fill((0, 0, 0))

    def move(self, action) -> None:
        return self.game.update(action)

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move = 'L'
                    elif event.key == pygame.K_RIGHT:
                        move = 'R'
                    elif event.key == pygame.K_UP:
                        move = 'U'
                    elif event.key == pygame.K_DOWN:
                        move = 'D'
                    env = self.game.update(move)
                    print('[INFO] Player: {} | Gain: {:4d}'.format(
                        move, env['reward']))
            self.update()
        pygame.quit()

    def render_score(self) -> None:
        # Create score label surface
        score_label = pygame.Surface((self.game.ncols * self.tile_size, 50))
        score_label.fill((0, 0, 0))  # Make score label background transparent

        # Render score text on score label surface
        score_text = self.font.render(
            "Score: {}".format(self.game.score),
            True, (255, 255, 255)
        )
        score_rect = score_text.get_rect()
        score_rect.center = (75, 25)  # Center text in score label surface
        score_label.blit(score_text, score_rect)

        # Blit score label surface onto screen surface
        self.screen.blit(
            score_label,
            (0, self.game.nrows * self.tile_size)
        )

    def update(self) -> None:
        self.screen.fill((0, 0, 0))
        for r in range(self.game.nrows):
            for c in range(self.game.ncols):
                value = self.game.board[r][c]
                if value == 0:
                    color = (0, 0, 0)
                else:
                    color = self.get_tile_color(value)
                rect = pygame.Rect(c * self.tile_size, r * self.tile_size,
                                   self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, color, rect)
                if value != 0:
                    text_surface = self.font.render(
                        str(value), True, (255, 255, 255))
                    text_rect = text_surface.get_rect()
                    text_rect.center = rect.center
                    self.screen.blit(text_surface, text_rect)

        self.render_score()

        pygame.display.flip()

    def get_tile_color(self, value: int) -> Tuple[int, int, int]:
        colors = {
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46)
        }
        return colors.get(value, (60, 58, 50))
