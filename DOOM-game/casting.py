import pygame as pg
import math
from setting import *


class Casting:
	def __init__(self, game):
		self.game = game
		self.ray_cast_result =[]
		self.obj_to_render =[]
		self.texts = self.game.obj_render.wall_text

	def get_obj_to_render(self):
		self.obj_to_render =[]
		for ray, values in enumerate(self.ray_cast_result):
			depth,proj_height,text,offset = values

			if proj_height< height:
				wall_column = self.texts[text].subsurface(
						offset * (text_size - scale), 0,scale,text_size
					)
				wall_column = pg.transform.scale(wall_column,(scale,proj_height))
				wall_pos = (ray * scale,half_height - proj_height//2)
			else:
				text_height = text_size *height / proj_height
				wall_column = self.texts[text].subsurface(
					offset * (text_size - scale), half_text_size - text_height//2,
					scale,text_height
				)
				wall_column = pg.transform.scale(wall_column, (scale , height))
				wall_pos = (ray*scale,0)

			self.obj_to_render.append((depth,wall_column,wall_pos))


	def ray_cast(self):
		self.ray_cast_result =[]
		ox,oy = self.game.player.pos
		x_map, y_map = self.game.player.map_pos
		text_vert, text_hor = 1,1


		ray_angle = self.game.player.angle - half_fov + 0.0001
		for ray in range(num_rays):
			sin_a = math.sin(ray_angle)
			cos_a = math.cos(ray_angle)

			#hori
			y_hor, dy = (y_map +1,1) if sin_a >0 else (y_map - 1e-6,-1)

			depth_hor = (y_hor -oy)/sin_a
			x_hor = ox + depth_hor * cos_a

			delta_depth = dy/sin_a
			dx = delta_depth *cos_a

			for i in range(max_depth):
				tile_hor = int(x_hor), int(y_hor)
				if tile_hor in self.game.map.world_map:
					text_hor = self.game.map.world_map[tile_hor]
					break
				x_hor += dx
				y_hor += dy
				depth_hor += delta_depth


			#vertical

			x_vert, dx = (x_map +1,1) if cos_a >0 else (x_map - 1e-6,-1)

			depth_vert = (x_vert -ox)/cos_a
			y_vert = oy + depth_vert * sin_a

			delta_depth = dx/cos_a
			dy = delta_depth *sin_a

			for i in range(max_depth):
				tile_vert = int(x_vert), int(y_vert)
				if tile_vert in self.game.map.world_map:
					text_vert = self.game.map.world_map[tile_vert]
					break
				x_vert += dx
				y_vert += dy
				depth_vert += delta_depth

			#depth
			if depth_vert< depth_hor:
				depth,text = depth_vert,text_vert
				y_vert %=1
				offset = y_vert if cos_a >0 else (1- y_vert)
			else:
				depth, text = depth_hor, text_hor
				x_hor %=1
				offset = (1- x_hor) if sin_a >0 else (1- x_hor)

			#remove fisbow
			depth *= math.cos(self.game.player.angle - ray_angle)

			#project
			proj_height = screen_dist /(depth + 0.0001)

			#ray casting result
			self.ray_cast_result.append((depth,proj_height,text,offset))

			ray_angle += delta_angle

	def update(self):
		self.ray_cast()
		self.get_obj_to_render()
