import pygame

from data.modules.helper import get_angled_offset, angle_to_mouse, get_angle_to, find_closest_collision
from data.modules.settings import TILE_SIZE
from data.modules.tile_map import TileMap


class Player:
	def __init__(self, pos: tuple[int, int]) -> None:
		self.image = pygame.Surface((TILE_SIZE * 0.8, TILE_SIZE * 1.8))

		# Inputs variables
		self.input: pygame.Vector2 = pygame.Vector2(0, 0)

		self.mouse_left: bool = False
		self.prev_mouse_left: bool = self.mouse_left

		self.mouse_right: bool = False
		self.prev_mouse_right: bool = self.mouse_right

		# * Movement
		# Movement variables
		self.pos: pygame.Vector2 = pygame.Vector2(pos[0], pos[1])
		self.movement: pygame.Vector2 = pygame.Vector2(0, 0)
		self.prev_movement: pygame.Vector2 = self.movement.copy()

		self.air_time: int = 0

		# Movement values
		self.drag_in_air: float = 0.94

		self.drag_x_on_ground: float = 0.7
		self.default_acceleration_x: float = 1.5
		self.turn_acceleration_x: float = 5
		self.acceleration_x_in_air: float = 0.3
		self.acceleration_x: float = 1.5

		self.gravity: float = 0.45
		self.jump: float = 15.0

		self.coyote_time: float = 7.0

		# * Grapple
		# Grapple values
		self.grapple_max_length = 300

		self.grapple_speed = 30

		# Grapple variables
		self.grapple_movement: float = 0
		self.grapple_length: float = 0

		self.grapple_end_length: float = 0

		self.grapple_fired_towards_point: tuple[int, int] | None = None

		self.grapple_end_point: tuple[float, float] | None = None
		self.grapple_hit_point: tuple[float, float] | None = None

		self.grapple_swing_movement = 1
		self.grapple_swing_speed = 1

	@property
	def rect(self) -> pygame.Rect:
		return self.image.get_rect(topleft=self.pos)

	def get_input(self) -> None:
		keys_pressed = pygame.key.get_pressed()
		mouse_pressed = pygame.mouse.get_pressed()

		if (keys_pressed[pygame.K_a] and keys_pressed[pygame.K_d]) or (keys_pressed[pygame.K_LEFT] and keys_pressed[pygame.K_RIGHT]):
			self.input.x = 0
		elif keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
			self.input.x = -1
		elif keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
			self.input.x = 1
		else:
			self.input.x = 0

		if (keys_pressed[pygame.K_w] and keys_pressed[pygame.K_s]) or (keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_DOWN]):
			self.input.y = 0
		elif keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
			self.input.y = 1
		elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
			self.input.y = -1
		else:
			self.input.y = 0

		self.mouse_left = mouse_pressed[0]
		self.mouse_right = mouse_pressed[2]

	def move_x(self) -> None:
		# For a more responsive direction change
		if self.input.x != 0:
			if self.movement.x / self.input.x < 0:
				self.acceleration_x = self.turn_acceleration_x
			else:
				self.acceleration_x = self.default_acceleration_x

		# Change movement
		if self.air_time > 0:
			self.movement.x += self.input.x * self.acceleration_x_in_air
			self.movement.x *= self.drag_in_air
		else:
			self.movement.x += self.input.x * self.acceleration_x
			self.movement.x *= self.drag_x_on_ground

		# Apply movement
		self.pos.x += self.movement.x

		if self.pos.x < 0:
			self.pos.x = 0
			self.movement.x = 0

	def handle_x_collisions(self, tile_map: TileMap) -> None:
		# Handle collisions
		if self.movement.x > 0:
			tile = tile_map.get_tile(self.rect.bottomright)
			if tile is not None:
				self.pos.x = tile.rect.left - self.image.get_width()
				self.movement.x = 0

			tile = tile_map.get_tile(self.rect.topright)
			if tile is not None:
				self.pos.x = tile.rect.left - self.image.get_width()
				self.movement.x = 0

			tile = tile_map.get_tile(self.rect.midright)
			if tile is not None:
				self.pos.x = tile.rect.left - self.image.get_width()
				self.movement.x = 0

		if self.movement.x < 0:
			tile = tile_map.get_tile(self.rect.bottomleft)
			if tile is not None:
				self.pos.x = tile.rect.right
				self.movement.x = 0

			tile = tile_map.get_tile(self.rect.topleft)
			if tile is not None:
				self.pos.x = tile.rect.right
				self.movement.x = 0

			tile = tile_map.get_tile(self.rect.midleft)
			if tile is not None:
				self.pos.x = tile.rect.right
				self.movement.x = 0

	def move_y(self) -> None:
		# Jump if on the ground and input suggests jumping
		if self.air_time < self.coyote_time and self.input.y == 1:
			self.movement.y = -self.jump

			self.air_time = self.coyote_time

		# Set on_ground to false, so that later on if colliding with the ground it can be set to true
		self.air_time += 1

		# Change movement
		self.movement.y += self.gravity
		self.movement.y *= self.drag_in_air

		# Apply movement
		self.pos.y += self.movement.y

	def handle_y_collisions(self, tile_map: TileMap) -> None:
		# Handle collisions
		if self.movement.y > 0:
			tile = tile_map.get_tile((self.rect.right - 2, self.rect.bottom))
			if tile is not None:
				self.pos.y = tile.rect.top - self.image.get_height()
				self.movement.y = 0

				self.air_time = 0

			tile = tile_map.get_tile((self.rect.left + 2, self.rect.bottom))
			if tile is not None:
				self.pos.y = tile.rect.top - self.image.get_height()
				self.movement.y = 0

				self.air_time = 0

		if self.movement.y < 0:
			tile = tile_map.get_tile((self.rect.right - 2, self.rect.top))
			if tile is not None:
				self.pos.y = tile.rect.bottom + 1
				self.movement.y = 0

			tile = tile_map.get_tile((self.rect.left + 2, self.rect.top))
			if tile is not None:
				self.pos.y = tile.rect.bottom + 1
				self.movement.y = 0

	def move(self, tile_map: TileMap) -> None:
		self.move_x()
		self.handle_x_collisions(tile_map)

		self.move_y()
		self.handle_y_collisions(tile_map)

	def shoot_grapple(self, scroll: pygame.Vector2, tile_map: TileMap) -> None:
		self.grapple_fired_towards_point = find_closest_collision(
			self.rect.center,
			angle_to_mouse(self.rect.center, scroll),
			self.grapple_max_length,
			tile_map
		)

		if self.grapple_fired_towards_point is not None:
			self.grapple_end_length = self.grapple_fired_towards_point.distance_to(self.rect.center)

		if self.grapple_fired_towards_point is None:
			# Sets the point you are firing to as just the max length
			self.grapple_fired_towards_point = self.rect.center + get_angled_offset(angle_to_mouse(self.rect.center, scroll), self.grapple_max_length)
			self.grapple_end_length = self.grapple_max_length * 2

		self.grapple_length = 1
		self.grapple_movement = 1

	# TODO: Make grapple behave more like rope than rubber band
	# TODO: Maintain velocity when swinging

	# TODO: Add a check for nearby blocks, so that it doesn't have to be a direct hit
	def update_grapple(self, tile_map) -> None:
		"""
		Handles the extension and retraction of the grapple
		"""

		# * If right button is clicked, retract grapple
		if not self.prev_mouse_right and self.mouse_right:
			self.grapple_hit_point = None
			self.grapple_movement = -1
			return

		# * Grapple going out
		if self.grapple_movement > 0:
			self.grapple_length += self.grapple_movement * self.grapple_speed

			if self.grapple_length > self.grapple_max_length:
				self.grapple_movement = -1
				return

			self.grapple_end_point = self.rect.center + get_angled_offset(get_angle_to(self.rect.center, self.grapple_fired_towards_point), self.grapple_length)

			if self.grapple_end_length - self.grapple_speed <= self.grapple_length:
				self.grapple_movement = -1
				self.grapple_hit_point = self.grapple_fired_towards_point
				self.grapple_end_point = self.grapple_hit_point

				self.grapple_length = pygame.Vector2(self.rect.center).distance_to(self.grapple_hit_point)

		# * Grapple reached end
		else:
			# Grapple retracting
			if self.grapple_hit_point is None:
				self.grapple_length += self.grapple_movement * self.grapple_speed

				self.grapple_end_point = self.rect.center + get_angled_offset(get_angle_to(self.rect.center, self.grapple_fired_towards_point), self.grapple_length)

			# Grapple attached to end point
			else:
				# Rubber band method?
				self.grapple_length = pygame.Vector2(self.rect.center).distance_to(self.grapple_hit_point) + self.grapple_movement * (self.grapple_length / (self.grapple_max_length * 0.4))
				self.grapple_length -= self.input.y * 0.5

				# self.grapple_length -= self.input.y * 3

				# Fix any offsets
				player_distance_to_hit_point = pygame.Vector2(self.rect.center).distance_to(self.grapple_hit_point)
				if player_distance_to_hit_point > self.grapple_length:
					# self.movement.y -= self.gravity
					#
					# self.movement += get_angled_offset(get_angle_to(self.rect.center, self.grapple_hit_point), 1).rotate(90 * -math.copysign(1, get_angle_to(self.rect.center, self.grapple_hit_point) - 90))

					offset = get_angled_offset(get_angle_to(self.rect.center, self.grapple_hit_point), player_distance_to_hit_point - self.grapple_length)
					self.movement += offset

			if self.grapple_length <= self.rect.height * 0.6:
				self.reset_grapple()

	def reset_grapple(self) -> None:
		self.grapple_length = 0
		self.grapple_movement = 0

		self.grapple_hit_point = None
		self.grapple_end_point = None
		self.grapple_fired_towards_point = None

	def update(self, tile_map: TileMap, scroll: pygame.Vector2) -> None:
		self.get_input()

		self.move(tile_map)

		if self.grapple_length == 0:
			# If the mouse wasn't previously down and currently is.
			if not self.prev_mouse_left and self.mouse_left:
				self.shoot_grapple(scroll, tile_map)
		else:
			self.update_grapple(tile_map)

		self.prev_mouse_left = self.mouse_left
		self.prev_mouse_right = self.mouse_right

		self.prev_movement = self.movement.copy()

	def draw(self, display: pygame.Surface, scroll: pygame.Vector2, tile_map) -> None:
		display.blit(self.image, self.pos - scroll)

		if self.grapple_fired_towards_point is not None:
			pygame.draw.circle(display, (20, 20, 200), self.grapple_fired_towards_point - scroll, 10, 4)

		if self.grapple_end_point is not None:
			pygame.draw.circle(display, (200, 20, 20), self.grapple_end_point - scroll, 10)

			pygame.draw.line(
				display,
				(150, 100, 100),
				self.rect.center - scroll,
				self.grapple_end_point - scroll,
				width=3
			)

		if self.grapple_hit_point is not None:
			pygame.draw.circle(display, (20, 200, 20), self.grapple_hit_point - scroll, 10)

			pygame.draw.line(
				display,
				(150, 100, 100),
				self.rect.center - scroll,
				self.grapple_hit_point - scroll,
				width=3
			)

		closest = find_closest_collision(
			self.rect.center,
			angle_to_mouse(self.rect.center, scroll),
			self.grapple_max_length,
			tile_map
		)

		closest_length = self.grapple_max_length

		if closest is not None:
			closest_length = closest.distance_to(self.rect.center)
			pygame.draw.line(display, (50, 50, 50), self.rect.center - scroll, closest - scroll)

		pygame.draw.circle(display, (200, 20, 20), self.rect.center + get_angled_offset(angle_to_mouse(self.rect.center, scroll), closest_length) - scroll, 10, width=1)
