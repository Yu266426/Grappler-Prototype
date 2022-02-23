import json
import math
import os.path

import pygame

from data.modules.files import LEVELS_DIR
from data.modules.settings import TILE_SIZE
from data.modules.tile_map import TileMap


def load_from_json(json_name: str) -> dict:
	json_path = os.path.join(LEVELS_DIR, f"{json_name}.json")

	with open(json_path) as file:
		data = file.read()

	return json.loads(data)


def get_angle_to(pos1: tuple[int, int], pos2: tuple[int, int]) -> float:
	pos1_x = pos1[0]
	pos1_y = pos1[1]

	pos2_x = pos2[0]
	pos2_y = pos2[1]

	# Gets the relative angle
	return math.degrees(math.atan2(pos1_y - pos2_y, pos2_x - pos1_x))


def angle_to_mouse(pos: tuple[int, int], scroll: pygame.Vector2):
	mouse_pos = pygame.mouse.get_pos()
	mouse_pos += scroll

	return get_angle_to(pos, mouse_pos)


def get_angled_offset(angle: float, offset: float):
	return pygame.math.Vector2(math.cos(math.radians(angle)) * offset, -1 * math.sin(math.radians(angle)) * offset)


def move_angled_offset(pos: pygame.Vector2 | tuple[int, int], offset: pygame.Vector2):
	return pos + offset


def find_closest_collision(pos: tuple[int, int], angle: float, max_length: float, tile_map: TileMap) -> pygame.Vector2 | None:
	length = 0
	while length < max_length:
		length += TILE_SIZE / 3

		end_pos = move_angled_offset(pos, get_angled_offset(angle, length))
		tile = tile_map.get_tile((end_pos.x, end_pos.y))

		if tile is not None:
			while tile.rect.collidepoint(end_pos.x, end_pos.y):
				length -= 1
				end_pos = move_angled_offset(pos, get_angled_offset(angle, length))

			return move_angled_offset(pos, get_angled_offset(angle, length + 1))

	return None
