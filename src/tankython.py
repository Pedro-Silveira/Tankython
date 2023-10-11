# DESENVOLVIDO POR: PEDRO HENRIQUE FERREIRA DA SILVEIRA (202010311)

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import pygame as pg
import numpy as np
from object_3d import Object3D

# VARIÁVEIS DO JOGO
movimento1 = 0
movimento2 = 0
click = 0
torreta = 0
tempo = 0
tempo2 = 0
recargaMC = 300
vidaInimigo = 0
vidaMC = 100
inimigoPerto = "A"
moveSom = 0
turretSom = 0
tiroSom = 0
movSom = 0
fireSom = 0
xMC = 0
yMC = 0
inicio = 0
velocidade = 0.9

class Game:
	def __init__(self):
		self.caption = 'Tankython'
		self.screen_width = 1280
		self.screen_height = 720
		self.fps = 60
	
	def run(self):
		global moveSom, turretSom, tiroSom, vidaMC, vidaInimigo, inicio, recargaMC, velocidade, click

		# FUNÇÃO PARA FILTRO PRETO E BRANCO
		def greyscale(surface: pg.Surface):
			arr = pg.surfarray.pixels3d(surface)
			mean_arr = np.dot(arr[:,:,:], [0.216, 0.587, 0.144])
			mean_arr3d = mean_arr[..., np.newaxis]
			new_arr = np.repeat(mean_arr3d[:, :, :], 3, axis=2)
			return pg.surfarray.make_surface(new_arr)

		pg.init()
		screen = pg.display.set_mode((self.screen_width, self.screen_height))
		pg.display.set_caption(self.caption)

		# DEFINIÇÃO DOS SONS DO JOGO
		pg.mixer.init()
		pg.mixer.music.load("res/sound/theme.mp3")
		pg.mixer.music.play(-1)
		fire = pg.mixer.Sound("res/sound/fire.mp3")
		fire.set_volume(0.5)
		efire = pg.mixer.Sound("res/sound/enemyFire.mp3")
		efire.set_volume(0.5)
		turre = pg.mixer.Sound("res/sound/turret.mp3")
		turre.set_volume(0.5)
		move = pg.mixer.Sound("res/sound/move.mp3")
		move.set_volume(0.5)
		emove = pg.mixer.Sound("res/sound/enemyMove.mp3")
		emove.set_volume(0.5)
		hit = pg.mixer.Sound("res/sound/hit.mp3")
		hit.set_volume(0.5)
		ehit = pg.mixer.Sound("res/sound/enemyHit.mp3")
		ehit.set_volume(0.5)
		miss = pg.mixer.Sound("res/sound/miss.mp3")
		miss.set_volume(0.5)
		reload = pg.mixer.Sound("res/sound/reload.mp3")
		reload.set_volume(0.5)
		explosion = pg.mixer.Sound("res/sound/explosion.mp3")
		explosion.set_volume(0.5)

		clock = pg.time.Clock()

		# CRIAÇÃO DOS OBJETOS 3D
		mc = Object3D(self.screen_width//1.8, self.screen_height//1.8, 'res/sprite/tank/', 4, screen)
		mc.turn_counterclockwise = True
		mc.angle = 45

		turret = Object3D(self.screen_width//1.8, self.screen_height//1.9, 'res/sprite/turret/', 3, screen)
		turret.turn_counterclockwise = True
		turret.angle = 45

		lama = Object3D(self.screen_width - self.screen_width//2, self.screen_height//2, 'res/sprite/mud/', 1, screen)
		lama.turn_counterclockwise = True

		arvore = Object3D(self.screen_width - self.screen_width//2, self.screen_height//2, 'res/sprite/birch/', 29, screen)
		arvore.turn_counterclockwise = True

		inimigo = Object3D(-50, -50, 'res/sprite/enemy/', 7, screen)
		inimigo.turn_counterclockwise = True

		# CRIAÇÃO DE FONTES E TEXTOS
		titulo = pg.font.Font("res/font/Tank.ttf", 72).render("TANKYTHON", True, [250, 250, 250])
		titulo_rect = titulo.get_rect(center=(self.screen_width/2, self.screen_height/6))

		start = pg.font.SysFont('Arial', 20, bold=True).render('PRESS \"SPACEBAR\" TO START THE GAME!', True, [250, 250, 250])
		start_rect = start.get_rect(center=(self.screen_width/2, self.screen_height - self.screen_height/6))

		death = pg.font.Font("res/font/Tank.ttf", 48).render("YOU\'RE DEAD!", True, [136, 0, 21])
		death_rect = death.get_rect(center=(self.screen_width/2, self.screen_height - self.screen_height/4))

		restart = pg.font.SysFont('Arial', 20, bold=True).render('PRESS \"SPACEBAR\" TO RESTART!', True, [250, 250, 250])
		restart_rect = restart.get_rect(center=(self.screen_width/2, self.screen_height - self.screen_height/6))

		# FUNÇÃO PARA CRIAR O INIMIGO
		def gerarInimigo():
			global vidaInimigo, movimento1, movimento2, torreta, velocidade, tempo, tempo2, fireSom, inimigoPerto, movSom

			local = random.randint(0, 3)

			if vidaInimigo <= 0:
				movimento1 = 0
				movimento2 = 0
				torreta = 0
				inimigoPerto = "A"
				movSom = 0
				fireSom = 0
				tempo = 0
				tempo2 = 0

				if tempo + (velocidade * 20) <= 100:
					tempo += velocidade * 20
				else:
					tempo = 100
				
				if tempo2 + (velocidade * 20) <= 300:
					tempo2 += velocidade * 20
				else:
					tempo2 = 300

				velocidade += 0.1

				emove.stop()
				explosion.play()

				if local == 0:
					x = random.randint(100, self.screen_width - 100)
					y = -100
				elif local == 1:
					x = random.randint(100, self.screen_width - 100)
					y = self.screen_height + 100
				elif local == 2:
					x = -100
					y = random.randint(100, self.screen_height - 100)
				else:
					x = self.screen_width + 100
					y = random.randint(100, self.screen_height - 100)

				inimigo.pos[0] = x
				inimigo.pos[1] = y

				vidaInimigo = 100

		# FUNÇÃO PARA ATIVAR O INIMIGO
		def ativaInimigo():
			global movimento1, movimento2, torreta, tempo, tempo2, inimigoPerto, movSom, fireSom, xMC, yMC, vidaMC, velocidade

			if inimigo.angle >= 360:
				inimigo.angle -= 360
			elif inimigo.angle < 0:
				inimigo.angle += 360

			if movimento1 == 0:
				if movSom == 0:
					emove.play(-1)
					movSom = 1

				if inimigo.pos[0] < 100:
					inimigo.pos[0] += 1 * velocidade
					if inimigo.angle > 180:
						inimigo.angle -= 1 * velocidade
					else:
						inimigo.angle += 1 * velocidade
				elif inimigo.pos[0] > (self.screen_width - 100):
					inimigo.pos[0] -= 1 * velocidade
					if inimigo.angle != 0:
						if inimigo.angle >= 180:
							inimigo.angle += 1 * velocidade
						else:
							inimigo.angle -= 1 * velocidade
				elif inimigo.pos[1] < 100:
					inimigo.pos[1] += 1 * velocidade
					if inimigo.angle >= 0 and inimigo.angle < 90:
						inimigo.angle += 1 * velocidade
					elif inimigo.angle <= 360 and inimigo.angle > 90:
						inimigo.angle -= 1 * velocidade
				elif inimigo.pos[1] > (self.screen_height - 100):
					inimigo.pos[1] -= 1 * velocidade
					if inimigo.angle > 270 or inimigo.angle <= 90:
						inimigo.angle -= 1 * velocidade
					else:
						inimigo.angle += 1 * velocidade
				else:
					movimento1 = 1
			elif movimento2 == 0:
				if inimigoPerto != "X" and inimigoPerto != "Y":
					if (inimigo.pos[0] - mc.pos[0]) > (inimigo.pos[1] - mc.pos[1]):
						inimigoPerto = "X"
					else:
						inimigoPerto = "Y"
				if inimigoPerto == "Y":
					if inimigo.pos[0] > mc.pos[0] and inimigo.pos[0] > mc.pos[0] + velocidade:
						inimigo.pos[0] -= 1 * velocidade
						if inimigo.angle != 0:
							if inimigo.angle >= 180:
								inimigo.angle += 1 * velocidade
							else:
								inimigo.angle -= 1 * velocidade
					elif inimigo.pos[0] < mc.pos[0] and inimigo.pos[0] < mc.pos[0] - velocidade:
						inimigo.pos[0] += 1 * velocidade
						if inimigo.angle > 180:
							inimigo.angle -= 1 * velocidade
						else:
							inimigo.angle += 1 * velocidade
					else:
						movimento2 = 1
				else:
					if inimigo.pos[1] > mc.pos[1] and inimigo.pos[1] > mc.pos[1] + velocidade:
						inimigo.pos[1] -= 1 * velocidade
						if inimigo.angle > 270 or inimigo.angle <= 90:
							inimigo.angle -= 1 * velocidade
						else:
							inimigo.angle += 1 * velocidade
					elif inimigo.pos[1] < mc.pos[1] and inimigo.pos[1] < mc.pos[1] - velocidade:
						inimigo.pos[1] += 1 * velocidade
						if inimigo.angle >= 0 and inimigo.angle < 90:
							inimigo.angle += 1 * velocidade
						elif inimigo.angle <= 360 and inimigo.angle > 90:
							inimigo.angle -= 1 * velocidade
					else:
						movimento2 = 1
			elif torreta == 0:
				inimigo.angle = round(inimigo.angle)
				if inimigoPerto == "Y":
					if inimigo.pos[1] > mc.pos[1]:
						if inimigo.angle != 270:
							if inimigo.angle > 270 or inimigo.angle <= 90:
								inimigo.angle -= 1
							else:
								inimigo.angle += 1
						else:
							xMC = mc.pos[0]
							yMC = mc.pos[1]
							torreta = 1
					else:
						if inimigo.angle != 90:
							if inimigo.angle >= 0 and inimigo.angle < 90:
								inimigo.angle += 1
							elif inimigo.angle <= 360 and inimigo.angle > 90:
								inimigo.angle -= 1
						else:
							xMC = mc.pos[0]
							yMC = mc.pos[1]
							torreta = 1
				else:
					if inimigo.pos[0] > mc.pos[0]:
						if inimigo.angle != 0:
							if inimigo.angle >= 180:
								inimigo.angle += 1
							else:
								inimigo.angle -= 1
						else:
							xMC = mc.pos[0]
							yMC = mc.pos[1]
							torreta = 1
					else:
						if inimigo.angle != 180:
							if inimigo.angle > 180:
								inimigo.angle -= 1
							else:
								inimigo.angle += 1
						else:
							xMC = mc.pos[0]
							yMC = mc.pos[1]
							torreta = 1
			else:
				emove.stop()
				if tempo >= 100:
					if fireSom == 0:	
						efire.play()
						fireSom = 1
						vida = vidaMC

						if mc.pos[0] > xMC:
							if mc.pos[1] > yMC:
								if mc.pos[0] - xMC <= 25 and mc.pos[1] - yMC <= 25:
									vidaMC -= 34
							else:
								if mc.pos[0] - xMC <= 25 and yMC - mc.pos[1] <= 25:
									vidaMC -= 34
						else:
							if mc.pos[1] > yMC:
								if xMC - mc.pos[0] <= 25 and mc.pos[1] - yMC <= 25:
									vidaMC -= 34
							else:
								if xMC - mc.pos[0] <= 25 and yMC - mc.pos[1] <= 25:
									vidaMC -= 34

						if vida != vidaMC:
							if vidaMC <= 0:
								explosion.play()
							ehit.play()
						else:
							miss.play()

					if tempo2 >= 300:
						movimento1 = 0
						movimento2 = 0
						torreta = 0
						inimigoPerto = "A"
						movSom = 0
						fireSom = 0
						tempo = 0
						tempo2 = 0
					else:
						tempo2 += 1
				else:
					tempo += 1

		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit()
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						quit()
				if event.type == pg.MOUSEBUTTONDOWN:
					if inicio == 0:
						if click == 0:
							click = 1
						else:
							click = 0

			# RENDERIZAÇÃO DOS OBJETOS
			screen.fill((101, 115, 82))
			lama.blit_me_3d()
			bar = pg.Rect(0, 0, 70, 20)
			bar.center = (inimigo.pos[0], inimigo.pos[1] - 75)
		
			red = pg.Rect(0, 0, 68, 18)
			red.center = (inimigo.pos[0], inimigo.pos[1] - 75)
		
			life = pg.Rect(0, 0, (68/100) * vidaInimigo, 18)
			life.center = (inimigo.pos[0], inimigo.pos[1] - 75)

			if mc.pos[1] > arvore.pos[1]:
				if inimigo.pos[1] > arvore.pos[1]:
					arvore.blit_me_3d()
					pg.draw.rect(screen, (0, 0, 0), bar)
					pg.draw.rect(screen, (136, 0, 21), red)
					pg.draw.rect(screen, (0, 206, 110), life)
					inimigo.blit_me_3d()
					mc.blit_me_3d()
					turret.blit_me_3d()
				else:
					pg.draw.rect(screen, (0, 0, 0), bar)
					pg.draw.rect(screen, (136, 0, 21), red)
					pg.draw.rect(screen, (0, 206, 110), life)
					inimigo.blit_me_3d()
					arvore.blit_me_3d()
					mc.blit_me_3d()
					turret.blit_me_3d()
			else:
				if inimigo.pos[1] > arvore.pos[1]:
					mc.blit_me_3d()
					turret.blit_me_3d()
					arvore.blit_me_3d()
					pg.draw.rect(screen, (0, 0, 0), bar)
					pg.draw.rect(screen, (136, 0, 21), red)
					pg.draw.rect(screen, (0, 206, 110), life)
					inimigo.blit_me_3d()
				else:
					pg.draw.rect(screen, (0, 0, 0), bar)
					pg.draw.rect(screen, (136, 0, 21), red)
					pg.draw.rect(screen, (0, 206, 110), life)
					inimigo.blit_me_3d()
					mc.blit_me_3d()
					turret.blit_me_3d()
					arvore.blit_me_3d()

			# MOVIMENTAÇÃO DO MC
			keys = pg.key.get_pressed()
			if mc.angle >= 360:
				mc.angle -= 360
			elif mc.angle < 0:
				mc.angle += 360

			if turret.angle >= 360:
				turret.angle -= 360
			elif turret.angle < 0:
				turret.angle += 360

			if vidaMC > 0 and inicio != 0:
				if keys[pg.K_LEFT]:
					if mc.pos[0] >= 50:
						if moveSom == 0:
							move.play(-1)
							moveSom = 1

						mc.pos[0] -= 1
						turret.pos[0] -= 1
						if mc.angle != 0:
							if mc.angle >= 180:
								mc.angle += 2
								turret.angle += 2
							else:
								mc.angle -= 2
								turret.angle -= 2
				elif keys[pg.K_RIGHT]:
					if mc.pos[0] <= self.screen_width - 50:
						if moveSom == 0:
							move.play(-1)
							moveSom = 1

						mc.pos[0] += 1
						turret.pos[0] += 1
						if mc.angle > 180:
							mc.angle -= 2
							turret.angle -= 2
						else:
							mc.angle += 2
							turret.angle += 2
				elif keys[pg.K_UP]:
					if mc.pos[1] >= 50:
						if moveSom == 0:
							move.play(-1)
							moveSom = 1
							
						mc.pos[1] -= 1
						turret.pos[1] -= 1
						if mc.angle > 270 or mc.angle <= 90:
							mc.angle -= 2
							turret.angle -= 2
						else:
							mc.angle += 2
							turret.angle += 2
				elif keys[pg.K_DOWN]:
					if mc.pos[1] <= self.screen_height - 50:
						if moveSom == 0:
							move.play(-1)
							moveSom = 1
							
						mc.pos[1] += 1
						turret.pos[1] += 1
						if mc.angle >= 0 and mc.angle < 90:
							mc.angle += 2
							turret.angle += 2
						elif mc.angle <= 360 and mc.angle > 90:
							mc.angle -= 2
							turret.angle -= 2
				else:
					moveSom = 0
					move.stop()

				if keys[pg.K_q]:
					if turretSom == 0:
						turre.play(-1)
						turretSom = 1
						
					turret.angle += 1
				elif keys[pg.K_e]:
					if turretSom == 0:
						turre.play(-1)
						turretSom = 1
						
					turret.angle -= 1
				else:
					turretSom = 0
					turre.stop()
				
				if recargaMC != 300:
					recargaMC += 1

				if keys[pg.K_SPACE]:
					if recargaMC == 300:
						fire.play()
						tiroSom = 0

						if pg.Rect(inimigo.pos[0] - 50, inimigo.pos[1] - 50, 100, 100).clipline((turret.pos[0], turret.pos[1]), (turret.pos[0] - math.cos(math.radians(-turret.angle)) * self.screen_width, turret.pos[1] - math.sin(math.radians(-turret.angle)) * self.screen_height)):
							hit.play()
							vidaInimigo -= 34
						else:
							miss.play()

						recargaMC = 0
					else:
						if tiroSom == 0:
							reload.play()
							tiroSom = 1

				fase = pg.font.SysFont('Arial', 20, bold=True).render('LEVEL: ' + str(round(velocidade)), True, [250, 250, 250])
				fase_rect = fase.get_rect(center=(self.screen_width - self.screen_width/8, self.screen_height/8))
				screen.blit(fase, fase_rect)

				heart = pg.image.load("res/img/heart.png")
				heart = pg.transform.scale(heart, (25, 25))

				heartFill = pg.image.load("res/img/heart-fill.png")
				heartFill = pg.transform.scale(heartFill, (25, 25))

				if vidaMC <= 32:
					screen.blit(heartFill, (self.screen_width/10, self.screen_height/9))
					screen.blit(heart, (self.screen_width/10 + 50, self.screen_height/9))
					screen.blit(heart, (self.screen_width/10 + 100, self.screen_height/9))
				elif vidaMC <= 66:
					screen.blit(heartFill, (self.screen_width/10, self.screen_height/9))
					screen.blit(heartFill, (self.screen_width/10 + 50, self.screen_height/9))
					screen.blit(heart, (self.screen_width/10 + 100, self.screen_height/9))
				else:
					screen.blit(heartFill, (self.screen_width/10, self.screen_height/9))
					screen.blit(heartFill, (self.screen_width/10 + 50, self.screen_height/9))
					screen.blit(heartFill, (self.screen_width/10 + 100, self.screen_height/9))

				gerarInimigo()
				ativaInimigo()
			else:
				if inicio == 0:
					screen.blit(titulo, titulo_rect)
					screen.blit(start, start_rect)

					lama.angle += 0.25
					arvore.angle += 0.25

					if click == 1:
						if pg.mouse.get_pos()[0] >= self.screen_width/2:
							if pg.mouse.get_pos()[1] >= (self.screen_height/3) * 2:
								if mc.angle != 135:
									if mc.angle > 135:
										mc.angle -= 1
										turret.angle -= 1
									else:
										mc.angle += 1
										turret.angle += 1
							elif pg.mouse.get_pos()[1] >= (self.screen_height/3):
								if mc.angle != 180:
									if mc.angle > 180:
										mc.angle -= 1
										turret.angle -= 1
									else:
										mc.angle += 1
										turret.angle += 1
							else:
								if mc.angle != 225:
									if mc.angle > 225:
										mc.angle -= 1
										turret.angle -= 1
									else:
										mc.angle += 1
										turret.angle += 1
						else:
							if pg.mouse.get_pos()[1] >= (self.screen_height/3) * 2:
								if mc.angle != 45:
									if mc.angle > 45:
										mc.angle -= 1
										turret.angle -= 1
									else:
										mc.angle += 1
										turret.angle += 1
							elif pg.mouse.get_pos()[1] >= (self.screen_height/3):
								if mc.angle >= 180:
									if mc.angle != 360:
										mc.angle += 1
										turret.angle += 1
								else:
									if mc.angle != 0:
										mc.angle -= 1
										turret.angle -= 1
							else:
								if mc.angle >= 225:
									if mc.angle < 315:
										mc.angle += 1
										turret.angle += 1
									else:
										mc.angle -= 1
										turret.angle -= 1
								else:
									if mc.angle != 315:
										mc.angle -= 1
										turret.angle -= 1
					else:
						if mc.angle != 45:
							if mc.angle > 45:
								mc.angle -= 1
								turret.angle -= 1
							else:
								mc.angle += 1
								turret.angle += 1
				else:
					pg.mixer.music.stop()
					screen.blit(greyscale(screen), (0, 0))
					screen.blit(death, death_rect)
					screen.blit(restart, restart_rect)

				if keys[pg.K_SPACE]:
					pg.mixer.music.play(-1)
					inicio = 1
					lama.angle = 180
					arvore.angle = 180
					mc.pos[0] = self.screen_width//1.8
					mc.pos[1] = self.screen_height//1.8
					mc.angle = 45
					turret.angle = 45
					turret.pos[0] = self.screen_width//1.8
					turret.pos[1] = self.screen_height//1.9
					velocidade = 0.9
					vidaInimigo = 0
					vidaMC = 100

			pg.display.flip()
			clock.tick(self.fps)

if __name__ == '__main__':
	game = Game()
	game.run()