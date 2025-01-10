import math
import pygame

#game setting
pygame.init()
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h  # Sử dụng độ phân giải hiện tại của màn hình
res = (width, height)
half_width = width //2
half_height = height //2
half_top = width //2
half_bot = height //2
fps = 0 

player_pos = 1.5,5
player_angle =0
player_speed = 0.004
player_rot_speed = 0.002
player_size_scale = 60
player_max_health = 100

mouse_sent=0.0003
mouse_sent2=0.00000002
mouse_max_rel=40
mouse_border_left=100
mouse_border_right =width- mouse_border_left
mouse_border_top=100
mouse_border_bot =height- mouse_border_top

floor_color = (30,30,30)

fov = math.pi /3
half_fov = fov/2
num_rays = width //2
half_num_rays = num_rays //2
delta_angle = fov / num_rays
max_depth = 20

screen_dist = half_width / math.tan(half_fov)
scale = width //num_rays

text_size = 256
half_text_size = text_size//2