from sprite import *

class Weapon(Animationsprite):
	def __init__(self,game,path='img/spi/weapon/shotgun/0.png', scale=0.25, animation_time=90):
		super().__init__(game=game, path=path,scale=scale, animation_time=animation_time)
		self.images =deque(
			[pg.transform.smoothscale(img,(self.image.get_width()* scale, self.image.get_height()*scale))
			for img in self.images])
		self.weapon_pos = (half_width - self.images[0].get_width()//2,height - self.images[0].get_height())
		self.reloading = False
		self.num_images = len(self.images)
		self.frame_couter =0
		self.damage =50

	def animate_shot(self):
		if self.reloading:
			self.game.player.shot= False
			if self.animation_trigger:
				self.images.rotate(-1)
				self.image = self.images[0]
				self.frame_couter +=1
				if self.frame_couter == self.num_images:
					self.reloading = False
					self.frame_couter =0

	def draw(self):
		self.game.screen.blit(self.images[0],self.weapon_pos)

	def update(self):
		self.check_animation_time()
		self.animate_shot()