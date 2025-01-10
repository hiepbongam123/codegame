from setting import *
import pygame as pg 
import math

class Player:
	"""docstring for ClassName"""
	def __init__(self, game):
		self.game =game
		self.x, self.y = player_pos
		self.angle = player_angle
		self.shot = False
		self.health = player_max_health
		self.rel =0
		self.rel_y=0
		self.health_recovery_delay =700
		self.time_pre = pg.time.get_ticks()
		self.pitch = 0

	def recover_health(self):
		if self.check_health_recovery_delay() and self.health < player_max_health:
			self.health +=1

	def check_health_recovery_delay(self):
		time_now = pg.time.get_ticks()
		if time_now - self.time_pre>self.health_recovery_delay:
			self.time_pre = time_now
			return True

	def check_game_over(self):
		if self.health<1:
			self.game.obj_render.game_over()
			pg.display.flip()
			pg.time.delay(1500)
			self.game.new_game()

	def get_damage(self,damage):
		self.health -= damage
		self.game.obj_render.player_damage()
		self.game.sound.player_pain.play()
		self.check_game_over()

	def single_fire_event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button ==1 and not self.shot and not self.game.weapon.reloading:
				self.game.sound.shotgun.play()
				self.shot =True
				self.game.weapon.reloading =True

	def movement(self):
		sin_a = math.sin(self.angle)
		cos_a = math.cos(self.angle)

		dx,dy = 0,0
		speed = player_speed * self.game.delta_time
		speed_sin = speed *sin_a
		speed_cos = speed *cos_a

		keys = pg.key.get_pressed()
		if keys[pg.K_w]:
			dx += speed_cos
			dy += speed_sin
		if keys[pg.K_s]:
			dx += -speed_cos
			dy += -speed_sin
		if keys[pg.K_a]:
			dx += speed_cos
			dy += -speed_sin
		if keys[pg.K_d]:
			dx += -speed_cos
			dy += speed_sin

		self.check_wall_collect(dx,dy)

		# if keys[pg.K_LEFT]:
		# 	self.angle -= player_rot_speed * self.game.delta_time
		# if keys[pg.K_RIGHT]:
		# 	self.angle += player_rot_speed * self.game.delta_time

		# if keys[pg.K_UP]:    # Phím lên để nhìn lên
		# 	self.pitch = min(self.pitch + 2, 100)  
		# elif keys[pg.K_DOWN]:  # Phím xuống để nhìn xuống
		# 	self.pitch = max(self.pitch - 2, -100)

		self.angle %= math.tau


	def check_wall(self,x,y):
		return (x,y) not in self.game.map.world_map

	def check_wall_collect(self,dx,dy):
		scale = player_size_scale / self.game.delta_time
		if self.check_wall(int(self.x+dx *scale),int(self.y)):
			self.x += dx
		if self.check_wall(int(self.x),int(self.y+dy*scale)):
			self.y += dy

	def draw(self):
		pg.draw.line(self.game.screen,'yellow',(self.x*60,self.y*60),
					(self.x *60 + width * math.cos(self.angle),
					self.y * 60 + width * math.sin(self.angle)),2)
		pg.draw.circle(self.game.screen,'green',(self.x *60, self.y *60),15)					

	def mouse_control(self):
		mx,my = pg.mouse.get_pos()
		if mx < mouse_border_left or mx> mouse_border_right :
			pg.mouse.set_pos([half_width, half_height])
		self.rel = pg.mouse.get_rel()[0]
		self.rel = max(- mouse_max_rel, min(mouse_max_rel, self.rel))
		self.angle += self.rel *mouse_sent * self.game.delta_time

		# Cập nhật sự di chuyển chuột theo trục Y để thay đổi góc nhìn lên/xuống
		self.rel_y = pg.mouse.get_rel()[1]
		self.rel_y = max(-mouse_max_rel, min(mouse_max_rel, self.rel_y))
		self.pitch = min(max(self.pitch - (my - 100) // 5, -100), 100)
		self.pitch += self.rel_y * mouse_sent * self.game.delta_time  # Chuyển theo hướng ngược lại

	def mouse_control2(self):
		mx,my = pg.mouse.get_pos()
		if mx < mouse_border_left or mx> mouse_border_right :
			pg.mouse.set_pos([half_width, half_height])
		# if my < mouse_border_top or my > mouse_border_bot:
		# 	pg.mouse.set_pos([half_width, half_height])
		self.rel = pg.mouse.get_rel()[0]
		self.rel = max(- mouse_max_rel, min(mouse_max_rel, self.rel))
		self.angle += self.rel *mouse_sent * self.game.delta_time

		# Cập nhật sự di chuyển chuột theo trục Y để thay đổi góc nhìn lên/xuống
		self.rel_y = pg.mouse.get_rel()[1]
		self.rel_y = max(-mouse_max_rel, min(mouse_max_rel, self.rel_y))
		self.pitch = min(max(self.pitch - (my - 100) // 5, -100), 100)
		self.pitch += self.rel_y * mouse_sent * self.game.delta_time  # Chuyển theo hướng ngược lại


	def update(self):
		self.movement()
		# self.mouse_control()
		self.mouse_control2()
		self.recover_health()


	@property
	def pos(self):
		return self.x,self.y

	@property
	def map_pos(self):
		return int(self.x), int(self.y)