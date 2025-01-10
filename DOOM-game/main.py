import pygame as pg
import sys
from setting import *
from map import *
from player import *
from casting import *
from render import *
from sprite import *
from handler import *
from weapon import *
from sound import *
from finding import *

class Game:
	def __init__(self):
		pg.init()
		pg.mouse.set_visible(False)
		self.screen = pg.display.set_mode(res)
		self.clock = pg.time.Clock()
		self.delta_time =1
		self.global_trigger = False
		self.global_event = pg.USEREVENT + 0
		pg.time.set_timer(self.global_event,40)
		self.new_game()

	def new_game(self):
		self.map = Map(self)
		self.player = Player(self)
		self.obj_render = Obj(self)
		self.casting = Casting(self)
		self.handler = Handler(self)
		self.weapon = Weapon(self)
		self.sound = Sound(self)
		self.finding = Finding(self)
		# self.static_sprite = Sprite(self)
		# self.animation_sprite = Animationsprite(self)

	def update(self):
		self.player.update()
		self.casting.update()
		self.handler.update()
		self.weapon.update()
		# self.static_sprite.update()
		# self.animation_sprite.update()
		pg.display.flip()
		self.delta_time = self.clock.tick(fps)
		pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

	def draw(self):
		self.obj_render.draw()
		self.weapon.draw()
		# self.screen.fill('black')
		# self.map.draw()
		# self.player.draw()


	def check_event(self):
		self.global_trigger =False
		for event in pg.event.get():
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE): 
				pg.quit()
				sys.exit()
			elif event.type == self.global_event:
				self.global_trigger= True
			self.player.single_fire_event(event)

	def run(self):
		while True:
			self.check_event()
			self.update()
			self.draw()

if __name__ == '__main__' :
	game = Game()
	game.run()