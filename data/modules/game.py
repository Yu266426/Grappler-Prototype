import pygame.display

from data.modules.level import Level
from data.modules.settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Game:
	def __init__(self) -> None:
		pygame.init()

		self.running: bool = True

		self.clock: pygame.time.Clock = pygame.time.Clock()

		self.display: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
		self.display_caption = "Grappler Prototype"
		pygame.display.set_caption(self.display_caption)

		self.level = Level()

	def handle_events(self) -> None:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False

	def update(self) -> None:
		self.clock.tick(60)
		pygame.display.set_caption(f"{self.display_caption}: {round(self.clock.get_fps())}")

		self.level.update()

	def draw(self) -> None:
		self.display.fill((200, 200, 200))

		self.level.draw(self.display)

		pygame.display.update()

	def quit(self) -> None:
		pygame.quit()
