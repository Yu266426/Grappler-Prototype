import pygame.sprite

from data.modules.settings import SCREEN_HEIGHT, TILE_SIZE


class Tile:
	def __init__(self, pos):
		super().__init__()

		self.image: pygame.Surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
		self.image.fill((36, 130, 93))

		self.rect: pygame.Rect = self.image.get_rect(topleft=(pos[0], SCREEN_HEIGHT - pos[1] - TILE_SIZE))

	def draw(self, display: pygame.Surface, scroll: pygame.Vector2):
		display.blit(self.image, self.rect.topleft - scroll)
		pygame.draw.rect(display, (0, 0, 0), (self.rect.topleft - scroll, self.rect.size), width=1)
