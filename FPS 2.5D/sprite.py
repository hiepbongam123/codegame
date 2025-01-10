import pygame as pg
from setting import *
import os
from collections import deque


class Sprite:
	def __init__(self,game,path='img/spi/static/candlebra.png',
				 pos=(10.5,3.5), scale=0.7,shift=0.27):
		self.game = game
		self.player =game.player
		self.x,self.y =pos
		self.image = pg.image.load(path).convert_alpha()
		self.img_width = self.image.get_width()
		self.img_half_width = self.image.get_width()//2
		self.img_ratio = self.img_width / self.image.get_height()
		self.dx,self.dy,self.theta,self.screen_x,self.dist,self.norm_dist= 0,0,0,0,1,1
		self.sprite_half_width=0
		self.sprite_scale= scale
		self.sprite_height_shift = shift

	def get_sprite_prj(self):
		prj = screen_dist /self.norm_dist * self.sprite_scale
		prj_width, prj_height = prj * self.img_ratio, prj

		image= pg.transform.scale(self.image,(prj_width,prj_height))

		self.sprite_half_width = prj//2
		height_shift = prj * self.sprite_height_shift
		pos = self.screen_x - self.sprite_half_width, half_height - prj_height//2 + height_shift

		self.game.casting.obj_to_render.append((self.norm_dist, image,pos))

	def get_sprite(self):
		dx = self.x - self.player.x
		dy = self.y - self.player.y
		self.dx,self.dy =dx,dy
		self.theta = math.atan2(dy,dx)

		delta = self.theta - self.player.angle
		if (dx> 0 and self.player.angle >math.pi) or (dx <0 and dy <0):
			delta += math.tau

		delta_rays = delta/ delta_angle
		self.screen_x = (half_num_rays + delta_rays)*scale

		self.dist = math.hypot(dx,dy)
		self.norm_dist = self.dist * math.cos(delta)
		if - self.img_half_width < self.screen_x < (width +self.img_half_width) and self.norm_dist> 0.5:
			self.get_sprite_prj()

	def update(self):
		self.get_sprite()


class Animationsprite(Sprite):
	def __init__(self,game,path='img/spi/animation/green_light/0.png',
				pos =(11.5,3.5),scale=0.8,shift=0.15,animation_time=120):
		super().__init__(game,path,pos,scale,shift)
		self.animation_time = animation_time
		self.path =path.rsplit('/',1)[0]
		self.images =self.get_img(self.path)
		self.animation_time_pre = pg.time.get_ticks()
		self.animation_trigger = False

	def update(self):
		super().update()
		self.check_animation_time()
		self.animate(self.images)

	def animate(self,images):
		if self.animation_trigger:
			images.rotate(-1)
			self.image = images[0]


	def check_animation_time(self):
		self.animation_trigger = False
		time_now =pg.time.get_ticks()
		if time_now - self.animation_time_pre > self.animation_time:
			self.animation_time_pre = time_now
			self.animation_trigger = True


	def get_img(self,path):
		image = deque()
		for file_name in os.listdir(path):
			if os.path.isfile(os.path.join(path,file_name)):
				img = pg.image.load(path+ '/' + file_name).convert_alpha()
				image.append(img)
		return image