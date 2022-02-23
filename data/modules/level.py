import pygame

from data.modules.helper import load_from_json
from data.modules.player import Player
from data.modules.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.tile_map import TileMap


class Level:
	def __init__(self) -> None:
		self.scroll: pygame.Vector2 = pygame.Vector2(0, 0)

		json_dict = load_from_json("test")

		self.tile_map: TileMap = TileMap(json_dict["tile_data"])

		self.player = Player((40, 400))

	def get_scroll(self) -> None:
		target_x = self.player.rect.center[0] - SCREEN_WIDTH / 2
		target_y = self.player.rect.center[1] - SCREEN_HEIGHT / 2

		self.scroll += pygame.Vector2(round((target_x - self.scroll.x) / 10, 3), round((target_y - self.scroll.y) / 10, 3))

		if self.scroll.x < 0:
			self.scroll.x = 0
		if self.scroll.y > 0:
			self.scroll.y = 0

	def update(self) -> None:
		self.get_scroll()

		self.player.update(self.tile_map, self.scroll)

	def draw(self, display: pygame.Surface) -> None:
		self.tile_map.draw(display, self.scroll)

		self.player.draw(display, self.scroll, self.tile_map)
