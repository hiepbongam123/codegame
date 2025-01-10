from sprite import *
from npc import *


class Handler:
	def __init__(self,game):
		self.game=game
		self.sprite_list= []
		self.npc_list=[]
		self.npc_sprite_path ='img/spi/npc/'
		self.static_sprite_path = 'img/spi/static_sprite/'
		self.anim_sprite_path ='img/spi/animation/'
		add_sprite = self.add_sprite
		add_npc =self.add_npc
		self.npc_positions ={}

		#sprite map
		add_sprite(Sprite(game))
		add_sprite(Animationsprite(game))
		add_sprite(Animationsprite(game, pos=(1.5,1.5)))
		add_sprite(Animationsprite(game, pos= (1.5,7.5)))
		add_sprite(Animationsprite(game, pos= (5.5,3.25)))
		add_sprite(Animationsprite(game, pos= (1.5,4.75)))
		add_sprite(Animationsprite(game, pos= (14.5,1.5)))
		add_sprite(Animationsprite(game, path=self.anim_sprite_path+ 'red_light/0.png',pos=(14.5,7.5)))
		add_sprite(Animationsprite(game, path=self.anim_sprite_path+ 'red_light/0.png',pos=(12.5,7.5)))
		add_sprite(Animationsprite(game, path=self.anim_sprite_path+ 'red_light/0.png',pos=(9.5,7.5)))

		#npc map
		add_npc(NPC(game))
		add_npc(SoldierNPC(game, pos=(11.5,4.5)))
		add_npc(GirlNPC(game, pos=(9.5,4.5)))
		add_npc(CyberNPC(game, pos=(12.5,16.5)))
		add_npc(CacoNPC(game, pos=(4.5,16.5)))
		add_npc(GirlNPC(game, pos=(1.5,16.5)))
		# add_npc(CacoNPC(game, pos=(9.5,11.5)))
		# add_npc(CyberNPC(game, pos=(3.5,12.5)))


	def update(self):
		self. npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
		[sprite.update() for sprite in self.sprite_list]
		[npc.update() for npc in self.npc_list]

	def add_npc(self,npc):
		self.npc_list.append(npc)



	def add_sprite(self,sprite):
		self.sprite_list.append(sprite)
