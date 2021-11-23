import math
from PIL import Image, ImageTk
import os
import pygame
import time
from tqdm import tqdm
import threading

WIDTH = 800
HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

intensity = 1
resolution = 10000
mouse = {'dx': 0, 'dy': 0, 'ux': 0, 'uy': 0, 'mx': 0, 'my': 0, 'down': False}

gradient = Image.open('grad_10.png')
colors = []
for i in range(gradient.width):
	colors.append(gradient.getpixel((i, 0)))

print('OK')


def get_infinity(num):
	global resolution
	z = 0
	for i in range(resolution):
		z = complex(z**2 + num)

		if z.real**2 + z.imag**2 > 4:
			return i

	return False
      
now_pos = [-2, -2]
size = 4

def calculation(start_x, start_y, end_x, end_y, position, rect_width):
	position[0] = position[0] + start_x/(WIDTH/rect_width)
	position[1] = position[1] + start_y/(WIDTH/rect_width)
	f_cat = (end_x - start_x)/(WIDTH/rect_width)
	s_cat = (end_y - start_y)/(WIDTH/rect_width)
	rect_width = max(f_cat, s_cat)

	return position, rect_width

def draw_img(position, rect_width, w=WIDTH, h=HEIGHT):
	img = Image.new('RGB', (w, h))
	z = tqdm(range(w), desc="Redraw...")

	for x in z:
		for y in range(h):
			n_x = position[0] + x/(w/rect_width)
			n_y = position[1] + y/(h/rect_width)
			num = get_infinity(complex(n_x, n_y))

			if num:
				r = colors[int(num*intensity)%(len(colors) - 1)][0]
				g = colors[int(num*intensity)%(len(colors) - 1)][1]
				b = colors[int(num*intensity)%(len(colors) - 1)][2]

				img.putpixel((x, y), (r, g, b))

	return img

def draw():
	global now_pos
	global size
	if mouse['ux'] < mouse['dx'] and mouse['uy'] < mouse['dy']:
		fin = calculation(mouse['ux'], mouse['uy'], mouse['dx'], mouse['dy'], now_pos, size)
		now_pos = fin[0]
		size = fin[1]
	elif mouse['ux'] < mouse['dx']:
		fin = calculation(mouse['ux'], mouse['dy'], mouse['dx'], mouse['uy'], now_pos, size)
		now_pos = fin[0]
		size = fin[1]
	elif mouse['uy'] < mouse['dy']:
		fin = calculation(mouse['dx'], mouse['uy'], mouse['ux'], mouse['dy'], now_pos, size)
		now_pos = fin[0]
		size = fin[1]
	else:
		fin = calculation(mouse['dx'], mouse['dy'], mouse['ux'], mouse['uy'], now_pos, size)
		now_pos = fin[0]
		size = fin[1]

	image_data = draw_img(now_pos, size)
	image_data.save('z/fractal.png')

def down(e):
	mouse['down'] = True
	mouse['dx'] = e.pos[0]
	mouse['dy'] = e.pos[1]

def up(e):
	mouse['down'] = False
	mouse['ux'] = e.pos[0]
	mouse['uy'] = e.pos[1]

a = ''
if a == '':
	image_data = draw_img(now_pos, size)
	image_data.save('z/fractal.png')
	img = pygame.image.load('z/fractal.png')

while 1:
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			exit()
		if i.type == pygame.MOUSEMOTION:
			mouse['mx'] = i.pos[0]
			mouse['my'] = i.pos[1]

		if i.type == pygame.MOUSEBUTTONDOWN:
			down(i)

		if i.type == pygame.MOUSEBUTTONUP:
			if mouse['dx'] != i.pos[0] and mouse['dy'] != i.pos[1]:
				up(i)
				draw()
			else:
				mouse['down'] = False

			img = pygame.image.load('z/fractal.png')
		if i.type == pygame.KEYDOWN:
			if i.key == 13:
				resolution = eval(input(f'Enter new resolution (old is {resolution}): '))
				image_data = draw_img(now_pos, size)
				image_data.save('z/fractal.png')
				img = pygame.image.load('z/fractal.png')
			if i.key == 1073741911:
				intensity = eval(input(f'Enter new intensity (old is {intensity}): '))
				image_data = draw_img(now_pos, size)
				image_data.save('z/fractal.png')
				img = pygame.image.load('z/fractal.png')

			if i.key == 115:
				image = draw_img(now_pos, size, 6144, 6144)
				image.save('6kimg.png')

	screen.fill((0, 0, 0))

	screen.blit(img, (0, 0))
	if mouse['down']:
		start_x = mouse['dx']
		start_y = mouse['dy']
		f_cat = (mouse['mx'] - start_x)
		s_cat = (mouse['my'] - start_y)
		
		rect_size = max(abs(f_cat), abs(s_cat))

		
		if f_cat < 0 and s_cat < 0:
			pygame.draw.rect(screen, (200, 200, 200), (start_x, start_y, -rect_size, -rect_size), 2)
		elif f_cat < 0:
			pygame.draw.rect(screen, (200, 200, 200), (start_x, start_y, -rect_size, rect_size), 2)
		elif s_cat < 0:
			pygame.draw.rect(screen, (200, 200, 200), (start_x, start_y, rect_size, -rect_size), 2)
		else:
			pygame.draw.rect(screen, (200, 200, 200), (start_x, start_y, rect_size, rect_size), 2)

	pygame.display.update()