import pygame as pg
from setting import *

class Obj:
	def __init__(self,game):
		self.game = game
		self.screen = game.screen
		self.wall_text = self.load_wall_text()
		self.sky_image = self.get_text('img/text/sky2.png',(width, half_height))
		self.sky_offset =0
		self.blood_screen = self.get_text('img/text/blood_screen.png', res)
		self.digit_size =90
		self.digit_images = [self.get_text(f'img/text/digits/{i}.png',[self.digit_size]*2)
							for i in range(11)]
		self.digits = dict(zip(map(str, range(11)), self.digit_images))
		self.game_over_image = self.get_text('img/text/game_over.png',(960,540))

	def draw(self):
		self.draw_bgr()
		self.render_game_obj()
		self.draw_player_health()

	def game_over(self):
		self.screen.blit(self.game_over_image,(0,0))

	def draw_player_health(self):
		health =str(self.game.player.health)
		for i,char in enumerate(health):
			self.screen.blit(self.digits[char],(i*self.digit_size,0))
		self.screen.blit(self.digits['10'],((i+1)*self.digit_size,0))

	def player_damage(self):
		self.screen.blit(self.blood_screen,(0,0))

	def draw_bgr(self):
		self.sky_offset = (self.sky_offset +4.0 * self.game.player.rel)%width
		self.screen.blit(self.sky_image,(- self.sky_offset,0))
		self.screen.blit(self.sky_image,(- self.sky_offset + width,0))
		#floor
		pg.draw.rect(self.screen, floor_color,(0,half_height,width,height))

	def render_game_obj(self):
		list_obj = sorted(self.game.casting.obj_to_render, key=lambda t: t[0], reverse=True)
		for depth, image, pos in list_obj:
        	# Điều chỉnh vị trí render theo pitch
			adjusted_pos = (pos[0], pos[1] + self.game.player.pitch)
			self.screen.blit(image, adjusted_pos)

	def render_game_obj(self):
		list_obj = sorted(self.game.casting.obj_to_render, key=lambda t: t[0], reverse=True)
		for depth, image, pos in list_obj:
	        # Điều chỉnh vị trí render theo `pitch`
			adjusted_pos = (pos[0], pos[1] + self.game.player.pitch)
			self.screen.blit(image, adjusted_pos)

	@staticmethod
	def get_text(path, res=(text_size,text_size)):
		text = pg.image.load(path).convert_alpha()
		return pg.transform.scale(text, res)

	def load_wall_text(self):
		return{
			1: self.get_text(r'img/text/1.png'),
			2: self.get_text(r'img/text/2.png'),
			3: self.get_text(r'img/text/3.png'),
			4: self.get_text(r'img/text/4.png'),
			5: self.get_text(r'img/text/5.png')
		}