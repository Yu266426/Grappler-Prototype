import pygame

from data.modules.settings import TILE_SIZE, SCREEN_HEIGHT
from data.modules.tile import Tile


def generate_tile_map(tile_data: dict) -> list[list[Tile | None]]:
	tiles: list[list[Tile | None]] = []

	for row in range(tile_data["height"]):
		temp_list = []

		for column in range(tile_data["width"]):
			if row == 0:
				temp_list.append(Tile((column * TILE_SIZE, row * TILE_SIZE)))
			else:
				temp_list.append(None)

		tiles.append(temp_list)

	for tile in tile_data["tiles"]:
		tiles[tile["pos"][1]][tile["pos"][0]] = Tile((tile["pos"][0] * TILE_SIZE, tile["pos"][1] * TILE_SIZE))

	return tiles


class TileMap:
	def __init__(self, tile_data) -> None:
		self.tiles: list[list] = generate_tile_map(tile_data)

	def get_tile(self, pos: tuple[int, int] | tuple[float, float]) -> Tile | None:
		row = int((SCREEN_HEIGHT - pos[1]) / TILE_SIZE)
		column = int(pos[0] / TILE_SIZE)

		if 0 <= row < len(self.tiles):
			if 0 <= column < len(self.tiles[row]):
				return self.tiles[row][column]
		return None

	def draw(self, display: pygame.Surface, scroll: pygame.Vector2) -> None:
		for row in self.tiles:
			for column in row:
				cell: Tile = column
				if cell is not None:
					cell.draw(display, scroll)
