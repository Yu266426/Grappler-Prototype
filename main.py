def main():
	from data.modules.game import Game

	game = Game()

	while game.running:
		game.handle_events()
		game.update()
		game.draw()

	game.quit()


if __name__ == '__main__':
	main()
