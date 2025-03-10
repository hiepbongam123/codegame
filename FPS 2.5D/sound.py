import pygame as pg


class Sound:
	"""docstring for ClassName"""
	def __init__(self, game):
		self.game= game
		pg.mixer.init()
		self.path ='img/sound/'
		self.shotgun = pg.mixer.Sound(self.path+ 'shotgun.wav')
		self.npc_pain = pg.mixer.Sound(self.path+ 'npc_pain.wav')
		self.npc_death = pg.mixer.Sound(self.path+ 'npc_death.wav')
		self.npc_shot = pg.mixer.Sound(self.path+ 'npc_attack.wav')
		self.player_pain = pg.mixer.Sound(self.path+ 'player_pain.wav')
		self.theme = pg.mixer.Sound(self.path+ 'theme.mp3')
		
