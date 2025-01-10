import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow
import pygame
import random
import math
import sys
import os
import cv2
# Initialize Pygame mixer and load a random background music
pygame.mixer.init()
pygame.mixer.music.set_endevent(pygame.USEREVENT)
game_duration = 150  # in seconds

# Your existing game classes (RogerAInv, LuffyAinv,rogernv, Luffynv, Bullet) here


class RogerAInv(pygame.sprite.Sprite):
    def __init__(self, x, y, images, speed, jump_height, health,level=1):
        super().__init__()
        self.images = images
        self.image = self.images['idle']
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.health = health
        self.max_health = health  # Khởi tạo max_health
        self.level = level  # Thêm thuộc tính level

        self.move_left = False
        self.move_right = False
        self.is_dodging = False
        self.dodge_distance = 150  # Khoảng cách né đòn tăng lên
        self.dodge_speed = 800  # Tốc độ né đòn nhanh hơn
        self.dodge_direction = 0
        self.current_image_index = 0
        self.running_timer = 0
        self.bullets = pygame.sprite.Group()

        self.skill_sound1 = pygame.mixer.Sound(r"sound\skill1.mp3")
        self.skill_sound2 = pygame.mixer.Sound(r"sound\skill2.mp3")
        self.collision_sound = pygame.mixer.Sound(r"sound\rogerdinh.mp3")
        self.skill_animation_duration = 0.4
        self.skill_animation_duration2 = 0.6
        # Thời gian hồi chiêu cho mỗi kỹ năng (trong giây)
        self.skill1_cooldown_default = 10
        self.skill2_cooldown_default = 10
        self.dodge_cooldown_default = 10
        self.skill1_cooldown = 0
        self.skill2_cooldown = 0
        self.dodge_cooldown = 0

        self.skill1_timer = 0 
        self.skill2_timer = 0  
        self.hit_timer = 0

    def check_collision(self, enemy_bullets):
        if self.skill1_timer <= 0 and self.skill2_timer <= 0:  
            for bullet in enemy_bullets:
                if pygame.sprite.collide_rect(self, bullet) and not bullet.has_hit:
                    self.health -= bullet.damage 
                    self.collision_sound.play()  
                    self.rect.x += bullet.direction[0] * 50
                    bullet.has_hit = True  
                    self.image = self.images['hit']  
                    self.hit_timer = 0.7

    def update(self, dt, enemy_bullets):
        self.check_collision(enemy_bullets)

        if self.hit_timer > 0:
            self.hit_timer -= dt
            if self.hit_timer <= 0:
                self.image = self.images['idle']
        elif self.skill1_timer > 0:
            self.skill1_timer -= dt
            if self.skill1_timer <= 0.25:
                self.image = self.images['skill1_end']  # Hình ảnh kết thúc tung chiêu
            elif self.skill1_timer <= 0:
                self.image = self.images['idle']
        elif self.skill2_timer > 0:
            self.skill2_timer -= dt
            if self.skill2_timer <= 0.45:
                self.image = self.images['skill2_end']  # Hình ảnh kết thúc tung chiêu
            elif self.skill2_timer <= 0:
                self.image = self.images['idle']
        elif self.is_dodging:
            dodge_step = self.dodge_speed * dt
            self.rect.x += self.dodge_direction * dodge_step
            self.dodge_distance -= dodge_step
            self.image = self.images['dodge']
            if self.dodge_distance <= 0:
                self.is_dodging = False
                self.dodge_distance = 200

            if self.rect.left < 80:
                self.rect.left = 80
                self.is_dodging = False
            elif self.rect.right > 880:
                self.rect.right = 880
                self.is_dodging = False

        elif self.move_left and self.rect.left > 80:
            self.rect.x -= self.speed * dt
            self.image = self.images['run_left'][self.current_image_index // 10]
            self.current_image_index += 1
            if self.current_image_index >= len(self.images['run_left']) * 10:
                self.current_image_index = 0

        elif self.move_right and self.rect.right < 880:
            self.rect.x += self.speed * dt
            self.image = self.images['run_right'][self.current_image_index // 10]
            self.current_image_index += 1
            if self.current_image_index >= len(self.images['run_right']) * 10:
                self.current_image_index = 0
        else:
            self.image = self.images['idle']

        self.bullets.update(dt)
        for bullet in self.bullets:
            if bullet.range_limit:
                distance_traveled = math.hypot(bullet.rect.centerx - bullet.start_x, bullet.rect.centery - bullet.start_y)
                if distance_traveled >= bullet.range_limit:
                    bullet.kill()

        self.skill1_cooldown = max(0, self.skill1_cooldown - dt)
        self.skill2_cooldown = max(0, self.skill2_cooldown - dt)
        self.dodge_cooldown = max(0, self.dodge_cooldown - dt)



    def dodge(self):
        if not self.is_dodging:
            self.is_dodging = True
            self.dodge_direction = random.choice([-1, 1])
            self.dodge_cooldown = self.dodge_cooldown_default 


    def fire_skill1(self):
        bullet_image = pygame.image.load(r"assets\anhskill1ai.png").convert_alpha()
        direction = self.get_bullet_direction()
        angle = self.get_bullet_angle(direction)
        rotated_image = pygame.transform.rotate(bullet_image, angle)
        bullet = Bullet(self.rect.centerx, self.rect.top, direction, rotated_image, damage=22)
        self.bullets.add(bullet)
        self.skill_sound1.play()
        bullet.range_limit = 900
        self.skill1_cooldown = self.skill1_cooldown_default
        self.image = self.images['skill1_start'] 
        self.skill1_timer = self.skill_animation_duration

    def fire_skill2(self):
        bullet_image = pygame.image.load(r"assets\skill44.png").convert_alpha()
        direction = self.get_bullet_direction()
        angle = math.degrees(math.atan2(-direction[1], direction[0]))
        rotated_image = pygame.transform.rotate(bullet_image, angle)
        bullet = Bullet(self.rect.centerx, self.rect.top, direction, rotated_image, damage=14)
        self.bullets.add(bullet)
        self.skill_sound2.play()
        bullet.range_limit = 250
        self.skill2_cooldown = self.skill2_cooldown_default
        self.image = self.images['skill2_start']
        self.skill2_timer = self.skill_animation_duration2

    def get_bullet_direction(self):
        angle = random.uniform(math.radians(210), math.radians(330))
        return math.cos(angle), -math.sin(angle)

    def get_bullet_angle(self, direction):
        # direction là tuple chứa hướng của viên đạn (dx, dy)
        return math.degrees(math.atan2(-direction[1], direction[0]))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        self.bullets.draw(screen)
        self.draw_health_bar(screen)  # Thêm dòng này để vẽ thanh máu

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 15
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 20, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)
        
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
        level_text = font.render(f"{self.level}", True, (255, 255, 0))  # Hiển thị cấp độ
        text_rect = health_text.get_rect(center=(self.rect.x + bar_width // 2, self.rect.y - 12))
        level_rect = level_text.get_rect(center=(self.rect.x + bar_width - 114, self.rect.y - 15))  # Điều chỉnh vị trí hiển thị cấp độ
        screen.blit(health_text, text_rect)
        screen.blit(level_text, level_rect)

        pygame.draw.circle(screen, (255, 255, 0), (level_rect.centerx, level_rect.centery), 14, 2)

    def ai(self, target_x=None):
        # Tự động thực hiện hành động
        if random.random() < 0.04 and self.skill1_cooldown <= 0:
            self.fire_skill1()  # Có xác suất rất nhỏ sẽ sử dụng skill 1
        elif random.random() < 0.03 and self.skill2_cooldown <= 0:
            self.fire_skill2()  # Có xác suất rất nhỏ sẽ sử dụng skill 2
        elif random.random() < 0.05:
            self.dodge()  # Có xác suất nhất định sẽ tránh đòn

        # Tự động di chuyển
        if target_x is not None:
            if self.rect.centerx < target_x - 50:
                self.move_right = True
                self.move_left = False
            elif self.rect.centerx > target_x + 50:
                self.move_left = True
                self.move_right = False
            else:
                self.move_left = False
                self.move_right = False

class LuffyAInv(pygame.sprite.Sprite):
    def __init__(self, x, y, images, speed, jump_height, health, level=1):
        super().__init__()
        self.images = images
        self.image = self.images['idle']
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.health = health
        self.max_health = health
        self.level = level  # Thêm thuộc tính level

        self.move_left = False
        self.move_right = False
        self.is_dodging = False
        self.dodge_distance = 100
        self.dodge_speed = 500
        self.dodge_direction = 0
        self.current_image_index = 0
        self.running_timer = 0
        self.bullets = pygame.sprite.Group()

        self.skill_sound1 = pygame.mixer.Sound(r"sound\luffyskill1.mp3")
        self.skill_sound2 = pygame.mixer.Sound(r"sound\luffyskill2.mp3")
        self.collision_sound = pygame.mixer.Sound(r"sound\luffydinh.mp3") 
        self.arrow_angle = math.radians(30)
        self.arrow_angle_change = math.radians(1)
        self.arrow_direction = 1
        self.skill1_timer = 0
        self.skill2_timer = 0
        self.skill_animation_duration1 = 0.8
        self.skill_animation_duration2 = 0.8
        self.hit_timer = 0
        self.is_skill1_active = False  
        self.is_skill2_active = False
        self.skill1_cooldown = 0
        self.skill2_cooldown = 0
        self.dodge_cooldown = 0
        self.skill1_cooldown_default = 10
        self.skill2_cooldown_default = 10
        self.dodge_cooldown_default = 10

    def check_collision(self, enemy_bullets):
        for bullet in enemy_bullets:
            if pygame.sprite.collide_rect(self, bullet) and not bullet.has_hit:
                self.health -= bullet.damage 
                self.collision_sound.play()  
                self.rect.x += bullet.direction[0] * 50
                bullet.has_hit = True  
                self.image = self.images['hit']  
                self.hit_timer = 0.5

    def update(self, dt,enemy_bullets):
        # Kiểm tra va chạm giữa nhân vật và các viên đạn
        self.check_collision(enemy_bullets)
            
        if self.hit_timer > 0:
            self.hit_timer -= dt
            if self.hit_timer <= 0:
                self.image = self.images['idle']
        elif self.skill1_timer > 0:
            self.skill1_timer -= dt
            if self.skill1_timer <= 0.65:
                self.image = self.images['skill1_end']  
            elif self.skill1_timer <= 0:
                self.image = self.images['idle']
        elif self.skill2_timer > 0:
            self.skill2_timer -= dt
            if self.skill2_timer <= 0.65:
                self.image = self.images['skill2_end']  
            elif self.skill2_timer <= 0:
                self.image = self.images['idle']
        elif self.is_dodging:
            dodge_step = self.dodge_speed * dt
            self.rect.x += self.dodge_direction * dodge_step
            self.dodge_distance -= dodge_step
            self.image = self.images['dodge']
            if self.dodge_distance <= 0:
                self.is_dodging = False
                self.dodge_distance = 150

            if self.rect.left < 80:
                self.rect.left = 80
                self.is_dodging = False
            elif self.rect.right > 880:
                self.rect.right = 880
                self.is_dodging = False

        elif self.move_left and self.rect.left > 80:
            self.rect.x -= self.speed * dt
            self.image = self.images['run_left'][self.current_image_index // 10]
            self.current_image_index += 1
            if self.current_image_index >= len(self.images['run_left']) * 10:
                self.current_image_index = 0

        elif self.move_right and self.rect.right < 880:
            self.rect.x += self.speed * dt
            self.image = self.images['run_right'][self.current_image_index // 10]
            self.current_image_index += 1
            if self.current_image_index >= len(self.images['run_right']) * 10:
                self.current_image_index = 0
        else:
            self.image = self.images['idle']

        self.bullets.update(dt)
        for bullet in self.bullets:
            if bullet.range_limit:
                distance_traveled = math.hypot(bullet.rect.centerx - bullet.start_x, bullet.rect.centery - bullet.start_y)
                if distance_traveled >= bullet.range_limit:
                    bullet.kill()

        self.skill1_cooldown = max(0, self.skill1_cooldown - dt)
        self.skill2_cooldown = max(0, self.skill2_cooldown - dt)
        self.dodge_cooldown = max(0, self.dodge_cooldown - dt)

    def dodge(self):
        if not self.is_dodging:
            self.is_dodging = True
            self.dodge_direction = random.choice([-1, 1])

    def fire_skill1(self):
        bullet_image = pygame.image.load(r"assets\anhluffyskill.png").convert_alpha()
        trail_image = pygame.image.load(r"assets\anhluffyskill111.png").convert_alpha()  # Hình ảnh vệt đạn
        direction = self.get_bullet_direction()
        angle = self.get_bullet_angle(direction)
        rotated_image = pygame.transform.rotate(bullet_image, angle)
        rotated_trail_image = pygame.transform.rotate(trail_image, angle)  # Quay hình ảnh vệt đạn theo hướng viên đạn
        bullet = TrailBullet(self.rect.centerx, self.rect.top, direction, rotated_image, damage=34, trail_image=rotated_trail_image)
        self.bullets.add(bullet)
        self.skill_sound1.play()
        bullet.range_limit = 500
        self.image = self.images['skill1_start']
        self.skill1_timer = self.skill_animation_duration1

    def fire_skill2(self):
        bullet_image = pygame.image.load(r"assets\anhluffyskill.png").convert_alpha()
        trail_image = pygame.image.load(r"assets\anhluffyskill222.png").convert_alpha()  # Hình ảnh vệt đạn
        direction = self.get_bullet_direction()
        angle = self.get_bullet_angle(direction)
        rotated_image = pygame.transform.rotate(bullet_image, angle)
        rotated_trail_image = pygame.transform.rotate(trail_image, angle)  # Quay hình ảnh vệt đạn theo hướng viên đạn
        bullet = TrailBullet(self.rect.centerx, self.rect.top, direction, rotated_image, damage=46, trail_image=rotated_trail_image)
        self.bullets.add(bullet)
        self.skill_sound2.play()
        bullet.range_limit = 400
        self.image = self.images['skill2_start']
        self.skill2_timer = self.skill_animation_duration2

    def get_bullet_angle(self, direction):
        return math.degrees(math.atan2(-direction[1], direction[0]))

    def get_bullet_direction(self):
        angle = random.uniform(math.radians(210), math.radians(330))
        return math.cos(angle), -math.sin(angle)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        self.bullets.draw(screen)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 15
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 20, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)
        
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
        level_text = font.render(f"{self.level}", True, (255, 255, 0))  # Hiển thị cấp độ
        text_rect = health_text.get_rect(center=(self.rect.x + bar_width // 2, self.rect.y - 12))
        level_rect = level_text.get_rect(center=(self.rect.x + bar_width - 114, self.rect.y - 15))  # Điều chỉnh vị trí hiển thị cấp độ
        screen.blit(health_text, text_rect)
        screen.blit(level_text, level_rect)

        pygame.draw.circle(screen, (255, 255, 0), (level_rect.centerx, level_rect.centery), 14, 2)

    def ai(self, target_x=None):
        # Tự động thực hiện hành động
        if random.random() < 0.005 :
            self.fire_skill1() 
        elif random.random() < 0.004 :
            self.fire_skill2() 
        elif random.random() < 0.05:
            self.dodge()  # Có xác suất nhất định sẽ tránh đòn

        # Tự động di chuyển
        if target_x is not None:
            if self.rect.centerx < target_x - 50:
                self.move_right = True
                self.move_left = False
            elif self.rect.centerx > target_x + 50:
                self.move_left = True
                self.move_right = False
            else:
                self.move_left = False
                self.move_right = False

class Rogernv(pygame.sprite.Sprite):
    def __init__(self, x, y, images, speed, jump_height, health, level=1):
        super().__init__()
        self.images = images
        self.image = self.images['idle']
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.health = health
        self.max_health = health
        self.level = level  # Thêm thuộc tính level

        self.move_left = False
        self.move_right = False
        self.is_dodging = False
        self.dodge_distance = 150
        self.dodge_speed = 800
        self.dodge_direction = 0
        self.current_image_index = 0
        self.running_timer = 0
        self.bullets = pygame.sprite.Group()

        self.skill_sound1 = pygame.mixer.Sound(r"sound\skill1.mp3")
        self.skill_sound2 = pygame.mixer.Sound(r"sound\skill2.mp3")
        self.collision_sound = pygame.mixer.Sound(r"sound\rogerdinh.mp3")
        self.skill_animation_duration = 0.6
        self.skill_animation_duration2 = 0.9

        self.arrow_angle = math.radians(30)
        self.arrow_angle_change = math.radians(1)
        self.arrow_direction = 1
        self.skill1_timer = 0
        self.skill2_timer = 0
        self.hit_timer = 0

    def check_collision(self, enemy_bullets):
        if self.skill1_timer <= 0 and self.skill2_timer <= 0:  
            for bullet in enemy_bullets:
                if pygame.sprite.collide_rect(self, bullet) and not bullet.has_hit:
                    self.health -= bullet.damage 
                    self.collision_sound.play()  
                    self.rect.x += bullet.direction[0] * 50
                    bullet.has_hit = True  
                    self.image = self.images['hit']  
                    self.hit_timer = 0.5

    def update(self, dt,enemy_bullets):
        # Kiểm tra va chạm giữa nhân vật và các viên đạn
        self.check_collision(enemy_bullets)
        if self.hit_timer > 0:
            self.hit_timer -= dt
            if self.hit_timer <= 0:
                self.image = self.images['idle']
        elif self.skill1_timer > 0:
            self.skill1_timer -= dt
            if self.skill1_timer <= 0.25:
                self.image = self.images['skill1_end']  # Hình ảnh kết thúc tung chiêu
            elif self.skill1_timer <= 0:
                self.image = self.images['idle']
        elif self.skill2_timer > 0:
            self.skill2_timer -= dt
            if self.skill2_timer <= 0.45:
                self.image = self.images['skill2_end']  # Hình ảnh kết thúc tung chiêu
            elif self.skill2_timer <= 0:
                self.image = self.images['idle']
        elif self.is_dodging:
            dodge_step = self.dodge_speed * dt
            self.rect.x += self.dodge_direction * dodge_step
            self.dodge_distance -= dodge_step
            self.image = self.images['dodge']
            if self.dodge_distance <= 0:
                self.is_dodging = False
                self.dodge_distance = 150

            if self.rect.left < 80:
                self.rect.left = 80
                self.is_dodging = False
            elif self.rect.right > 880:
                self.rect.right = 880
                self.is_dodging = False

        elif self.move_left and self.rect.left > 80:
            self.rect.x -= self.speed * dt
            self.image = self.images['run_left'][self.current_image_index // 10]
            self.current_image_index += 1
            if self.current_image_index >= len(self.images['run_left']) * 10:
                self.current_image_index = 0

        elif self.move_right and self.rect.right < 880:
            self.rect.x += self.speed * dt
            self.image = self.images['run_right'][self.current_image_index // 10]
            self.current_image_index += 1
            if self.current_image_index >= len(self.images['run_right']) * 10:
                self.current_image_index = 0
        else:
            self.image = self.images['idle']

        self.bullets.update(dt)
        for bullet in self.bullets:
            if bullet.range_limit:
                distance_traveled = math.hypot(bullet.rect.centerx - bullet.start_x, bullet.rect.centery - bullet.start_y)
                if distance_traveled >= bullet.range_limit:
                    bullet.kill()

        self.update_arrow_angle()

    def dodge(self):
        if not self.is_dodging:
            self.is_dodging = True
            self.dodge_direction = random.choice([-1, 1])

    def fire_skill1(self):
        bullet_image = pygame.image.load(r"assets\anhskill1ai.png").convert_alpha()
        direction = (math.cos(self.arrow_angle), -math.sin(self.arrow_angle))
        angle = self.get_bullet_angle(direction)
        rotated_image = pygame.transform.rotate(bullet_image, angle)
        bullet = Bullet(self.rect.centerx, self.rect.top, direction, rotated_image, damage=6)
        self.bullets.add(bullet)
        self.skill_sound1.play()
        bullet.range_limit = 700
        self.image = self.images['skill1_start']
        self.skill1_timer = self.skill_animation_duration

    def fire_skill2(self):
        bullet_image = pygame.image.load(r"assets\skill44.png").convert_alpha()
        direction = (math.cos(self.arrow_angle), -math.sin(self.arrow_angle))
        angle = self.get_bullet_angle(direction)
        rotated_image = pygame.transform.rotate(bullet_image, angle)
        bullet = Bullet(self.rect.centerx, self.rect.top, direction, rotated_image, damage=6)
        self.bullets.add(bullet)
        self.skill_sound2.play()
        bullet.range_limit = 250
        self.image = self.images['skill2_start']
        self.skill2_timer = self.skill_animation_duration

    def get_bullet_angle(self, direction):
        return math.degrees(math.atan2(-direction[1], direction[0]))

    def get_bullet_direction(self):
        # direction là tuple chứa hướng của viên đạn (dx, dy)
        # Chọn một góc ngẫu nhiên trong khoảng từ 190 độ đến 330 độ
        angle = random.uniform(math.radians(30), math.radians(150))
        return math.cos(angle), -math.sin(angle)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        self.bullets.draw(screen)
        self.draw_health_bar(screen)
        self.draw_direction_arrow(screen)

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 15
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 20, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)
        
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
        level_text = font.render(f"{self.level}", True, (255, 255, 0))  # Hiển thị cấp độ
        text_rect = health_text.get_rect(center=(self.rect.x + bar_width // 2, self.rect.y - 12))
        level_rect = level_text.get_rect(center=(self.rect.x + bar_width - 114, self.rect.y - 15))  # Điều chỉnh vị trí hiển thị cấp độ
        screen.blit(health_text, text_rect)
        screen.blit(level_text, level_rect)

        pygame.draw.circle(screen, (255, 255, 0), (level_rect.centerx, level_rect.centery), 14, 2)

    def draw_direction_arrow(self, screen):
        start_pos = (self.rect.centerx, self.rect.top)  # Đỉnh đầu của nhân vật
        end_pos = (
            self.rect.centerx + 50 * math.cos(self.arrow_angle), 
            self.rect.top - 50 * math.sin(self.arrow_angle)  # Điều chỉnh để mũi tên đi lên
        )
        pygame.draw.line(screen, (0, 255, 0), start_pos, end_pos, 3)

        arrow_length = 10
        arrow_angle = math.pi / 6
        arrow_points = [
            (
                end_pos[0] - arrow_length * math.cos(self.arrow_angle - arrow_angle), 
                end_pos[1] + arrow_length * math.sin(self.arrow_angle - arrow_angle)
            ),
            (
                end_pos[0] - arrow_length * math.cos(self.arrow_angle + arrow_angle), 
                end_pos[1] + arrow_length * math.sin(self.arrow_angle + arrow_angle)
            )
        ]
        pygame.draw.polygon(screen, (0, 255, 0), [end_pos, *arrow_points])

    def update_arrow_angle(self):
        self.arrow_angle += self.arrow_direction * self.arrow_angle_change
        if self.arrow_angle > math.radians(150) or self.arrow_angle < math.radians(30):
            self.arrow_direction *= -1

class Yamatonv(pygame.sprite.Sprite):
    def __init__(self, x, y, images, speed, jump_height, health, level=1):
        super().__init__()
        self.images = images
        self.image = self.images['idle']
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.health = health
        self.max_health = health
        self.level = level  # Thêm thuộc tính level

        self.move_left = False
        self.move_right = False
        self.is_dodging = False
        self.dodge_distance = 150
        self.dodge_speed = 800
        self.dodge_direction = 0
        self.current_image_index = 0
        self.running_timer = 0
        self.bullets = pygame.sprite.Group()

        self.skill_sound1 = pygame.mixer.Sound(r"sound\yamato1.mp3")
        self.skill_sound2 = pygame.mixer.Sound(r"sound\yamato2.mp3")
        self.collision_sound = pygame.mixer.Sound(r"sound\yamatodinh.mp3")
        self.skill_animation_duration = 0.6
        self.skill_animation_duration2 = 0.9

        self.arrow_angle = math.radians(30)
        self.arrow_angle_change = math.radians(1)
        self.arrow_direction = 1
        self.skill1_timer = 0
        self.skill2_timer = 0
        self.hit_timer = 0

    def check_collision(self, enemy_bullets):
        if self.skill1_timer <= 0 and self.skill2_timer <= 0:  
            for bullet in enemy_bullets:
                if pygame.sprite.collide_rect(self, bullet) and not bullet.has_hit:
                    self.health -= bullet.damage 
                    self.collision_sound.play()  
                    self.rect.x += bullet.direction[0] * 50
                    bullet.has_hit = True  
                    self.image = self.images['hit']  
                    self.hit_timer = 0.7

    def update(self, dt,enemy_bullets):
        # Kiểm tra va chạm giữa nhân vật và các viên đạn
        self.check_collision(enemy_bullets)
            
        if self.skill1_timer > 0:
            self.skill1_timer -= dt
            if self.skill1_timer <= 0:
                self.image = self.images['idle']
        elif self.skill2_timer > 0:
            self.skill2_timer -= dt
            if self.skill2_timer <= 0:
                self.image = self.images['idle']
        elif self.is_dodging:
            dodge_step = self.dodge_speed * dt
            self.rect.x += self.dodge_direction * dodge_step
            self.dodge_distance -= dodge_step
            self.image = self.images['dodge']
            if self.dodge_distance <= 0:
                self.is_dodging = False
                self.dodge_distance = 150

            if self.rect.left < 80:
                self.rect.left = 80
                self.is_dodging = False
            elif self.rect.right > 880:
                self.rect.right = 880
                self.is_dodging = False

        elif self.move_left and self.rect.left > 80:
            self.rect.x -= self.speed * dt
            self.image = self.images['run_left'][self.current_image_index // 10]
            self.current_image_index += 1
            if self.current_image_index >= len(self.images['run_left']) * 10:
                self.current_image_index = 0

        elif self.move_right and self.rect.right < 880:
            self.rect.x += self.speed * dt
            self.image = self.images['run_right'][self.current_image_index // 10]
            self.current_image_index += 1
            if self.current_image_index >= len(self.images['run_right']) * 10:
                self.current_image_index = 0
        else:
            self.image = self.images['idle']

        self.bullets.update(dt)
        for bullet in self.bullets:
            if bullet.range_limit:
                distance_traveled = math.hypot(bullet.rect.centerx - bullet.start_x, bullet.rect.centery - bullet.start_y)
                if distance_traveled >= bullet.range_limit:
                    bullet.kill()

        self.update_arrow_angle()

    def dodge(self):
        if not self.is_dodging:
            self.is_dodging = True
            self.dodge_direction = random.choice([-1, 1])

    def fire_skill1(self):
        bullet_image = pygame.image.load(r"assets\skill1yamato.png").convert_alpha()
        direction = (math.cos(self.arrow_angle), -math.sin(self.arrow_angle))
        angle = self.get_bullet_angle(direction)
        rotated_image = pygame.transform.rotate(bullet_image, angle)
        bullet = Bullet(self.rect.centerx, self.rect.top, direction, rotated_image, damage=2)
        self.bullets.add(bullet)
        self.skill_sound1.play()
        bullet.range_limit = 100
        self.image = self.images['skill1']
        self.skill1_timer = self.skill_animation_duration

    def fire_skill2(self):
        bullet_image = pygame.image.load(r"assets\skill2yamato.png").convert_alpha()
        direction = (math.cos(self.arrow_angle), -math.sin(self.arrow_angle))
        angle = self.get_bullet_angle(direction)
        rotated_image = pygame.transform.rotate(bullet_image, angle)
        bullet = Bullet(self.rect.centerx, self.rect.top, direction, rotated_image, damage=12)
        self.bullets.add(bullet)
        self.skill_sound2.play()
        bullet.range_limit = 400
        self.image = self.images['skill2']
        self.skill2_timer = self.skill_animation_duration

    def get_bullet_angle(self, direction):
        return math.degrees(math.atan2(-direction[1], direction[0]))

    def get_bullet_direction(self):
        # direction là tuple chứa hướng của viên đạn (dx, dy)
        # Chọn một góc ngẫu nhiên trong khoảng từ 190 độ đến 330 độ
        angle = random.uniform(math.radians(30), math.radians(150))
        return math.cos(angle), -math.sin(angle)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        self.bullets.draw(screen)
        self.draw_health_bar(screen)
        self.draw_direction_arrow(screen)

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 15
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 20, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)
        
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
        level_text = font.render(f"{self.level}", True, (255, 255, 0))  # Hiển thị cấp độ
        text_rect = health_text.get_rect(center=(self.rect.x + bar_width // 2, self.rect.y - 12))
        level_rect = level_text.get_rect(center=(self.rect.x + bar_width - 114, self.rect.y - 15))  # Điều chỉnh vị trí hiển thị cấp độ
        screen.blit(health_text, text_rect)
        screen.blit(level_text, level_rect)

        pygame.draw.circle(screen, (255, 255, 0), (level_rect.centerx, level_rect.centery), 14, 2)

    def draw_direction_arrow(self, screen):
        start_pos = (self.rect.centerx, self.rect.top)  # Đỉnh đầu của nhân vật
        end_pos = (
            self.rect.centerx + 50 * math.cos(self.arrow_angle), 
            self.rect.top - 50 * math.sin(self.arrow_angle)  # Điều chỉnh để mũi tên đi lên
        )
        pygame.draw.line(screen, (0, 255, 0), start_pos, end_pos, 3)

        arrow_length = 10
        arrow_angle = math.pi / 6
        arrow_points = [
            (
                end_pos[0] - arrow_length * math.cos(self.arrow_angle - arrow_angle), 
                end_pos[1] + arrow_length * math.sin(self.arrow_angle - arrow_angle)
            ),
            (
                end_pos[0] - arrow_length * math.cos(self.arrow_angle + arrow_angle), 
                end_pos[1] + arrow_length * math.sin(self.arrow_angle + arrow_angle)
            )
        ]
        pygame.draw.polygon(screen, (0, 255, 0), [end_pos, *arrow_points])

    def update_arrow_angle(self):
        self.arrow_angle += self.arrow_direction * self.arrow_angle_change
        if self.arrow_angle > math.radians(150) or self.arrow_angle < math.radians(30):
            self.arrow_direction *= -1

class Luffynv(pygame.sprite.Sprite):
    def __init__(self, x, y, images, speed, jump_height, health, level=1):
        super().__init__()
        self.images = images
        self.image = self.images['idle']
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.health = health
        self.max_health = health
        self.level = level  # Thêm thuộc tính level

        self.move_left = False
        self.move_right = False
        self.is_dodging = False
        self.dodge_distance = 150
        self.dodge_speed = 800
        self.dodge_direction = 0
        self.current_image_index = 0
        self.running_timer = 0
        self.bullets = pygame.sprite.Group()

        self.skill_sound1 = pygame.mixer.Sound(r"sound\luffyskill1.mp3")
        self.skill_sound2 = pygame.mixer.Sound(r"sound\luffyskill2.mp3")
        self.collision_sound = pygame.mixer.Sound(r"sound\luffydinh.mp3") 
        self.arrow_angle = math.radians(30)
        self.arrow_angle_change = math.radians(1)
        self.arrow_direction = 1
        self.skill1_timer = 0
        self.skill2_timer = 0
        self.skill_animation_duration1 = 0.8
        self.skill_animation_duration2 = 0.8
        self.hit_timer = 0
        self.is_skill1_active = False  
        self.is_skill2_active = False

    def check_collision(self, enemy_bullets):
        for bullet in enemy_bullets:
            if pygame.sprite.collide_rect(self, bullet) and not bullet.has_hit:
                self.health -= bullet.damage 
                self.collision_sound.play()  
                self.rect.x += bullet.direction[0] * 50
                bullet.has_hit = True  
                self.image = self.images['hit']  
                self.hit_timer = 0.5

    def update(self, dt,enemy_bullets):
        # Kiểm tra va chạm giữa nhân vật và các viên đạn
        self.check_collision(enemy_bullets)
            
        if self.hit_timer > 0:
            self.hit_timer -= dt
            if self.hit_timer <= 0:
                self.image = self.images['idle']
        elif self.skill1_timer > 0:
            self.skill1_timer -= dt
            if self.skill1_timer <= 0.65:
                self.image = self.images['skill1_end']  
            elif self.skill1_timer <= 0:
                self.image = self.images['idle']
        elif self.skill2_timer > 0:
            self.skill2_timer -= dt
            if self.skill2_timer <= 0.65:
                self.image = self.images['skill2_end']  
            elif self.skill2_timer <= 0:
                self.image = self.images['idle']
        elif self.is_dodging:
            dodge_step = self.dodge_speed * dt
            self.rect.x += self.dodge_direction * dodge_step
            self.dodge_distance -= dodge_step
            self.image = self.images['dodge']
            if self.dodge_distance <= 0:
                self.is_dodging = False
                self.dodge_distance = 150

            if self.rect.left < 80:
                self.rect.left = 80
                self.is_dodging = False
            elif self.rect.right > 880:
                self.rect.right = 880
                self.is_dodging = False

        elif self.move_left and self.rect.left > 80:
            self.rect.x -= self.speed * dt
            self.image = self.images['run_left'][self.current_image_index // 10]
            self.current_image_index += 1
            if self.current_image_index >= len(self.images['run_left']) * 10:
                self.current_image_index = 0

        elif self.move_right and self.rect.right < 880:
            self.rect.x += self.speed * dt
            self.image = self.images['run_right'][self.current_image_index // 10]
            self.current_image_index += 1
            if self.current_image_index >= len(self.images['run_right']) * 10:
                self.current_image_index = 0
        else:
            self.image = self.images['idle']

        self.bullets.update(dt)
        for bullet in self.bullets:
            if bullet.range_limit:
                distance_traveled = math.hypot(bullet.rect.centerx - bullet.start_x, bullet.rect.centery - bullet.start_y)
                if distance_traveled >= bullet.range_limit:
                    bullet.kill()

        self.update_arrow_angle()

    def dodge(self):
        if not self.is_dodging:
            self.is_dodging = True
            self.dodge_direction = random.choice([-1, 1])

    def fire_skill1(self):
        bullet_image = pygame.image.load(r"assets\anhluffyskill.png").convert_alpha()
        trail_image = pygame.image.load(r"assets\anhluffyskill111.png").convert_alpha()  # Hình ảnh vệt đạn
        direction = (math.cos(self.arrow_angle), -math.sin(self.arrow_angle))
        angle = self.get_bullet_angle(direction)
        rotated_image = pygame.transform.rotate(bullet_image, angle)
        rotated_trail_image = pygame.transform.rotate(trail_image, angle)  # Quay hình ảnh vệt đạn theo hướng viên đạn
        bullet = TrailBullet(self.rect.centerx, self.rect.top, direction, rotated_image, damage=8, trail_image=rotated_trail_image)
        self.bullets.add(bullet)
        self.skill_sound1.play()
        bullet.range_limit = 500
        self.image = self.images['skill1_start']
        self.skill1_timer = self.skill_animation_duration1

    def fire_skill2(self):
        bullet_image = pygame.image.load(r"assets\anhluffyskill.png").convert_alpha()
        trail_image = pygame.image.load(r"assets\anhluffyskill222.png").convert_alpha()  # Hình ảnh vệt đạn
        direction = (math.cos(self.arrow_angle), -math.sin(self.arrow_angle))
        angle = self.get_bullet_angle(direction)
        rotated_image = pygame.transform.rotate(bullet_image, angle)
        rotated_trail_image = pygame.transform.rotate(trail_image, angle)  # Quay hình ảnh vệt đạn theo hướng viên đạn
        bullet = TrailBullet(self.rect.centerx, self.rect.top, direction, rotated_image, damage=10, trail_image=rotated_trail_image)
        self.bullets.add(bullet)
        self.skill_sound2.play()
        bullet.range_limit = 400
        self.image = self.images['skill2_start']
        self.skill2_timer = self.skill_animation_duration2

    def get_bullet_angle(self, direction):
        return math.degrees(math.atan2(-direction[1], direction[0]))

    def get_bullet_direction(self):
        angle = random.uniform(math.radians(30), math.radians(150))
        return math.cos(angle), -math.sin(angle)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        self.bullets.draw(screen)
        self.draw_health_bar(screen)
        self.draw_direction_arrow(screen)

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 15
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 20, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)
        
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
        level_text = font.render(f"{self.level}", True, (255, 255, 0))  # Hiển thị cấp độ
        text_rect = health_text.get_rect(center=(self.rect.x + bar_width // 2, self.rect.y - 12))
        level_rect = level_text.get_rect(center=(self.rect.x + bar_width - 114, self.rect.y - 15))  # Điều chỉnh vị trí hiển thị cấp độ
        screen.blit(health_text, text_rect)
        screen.blit(level_text, level_rect)

        pygame.draw.circle(screen, (255, 255, 0), (level_rect.centerx, level_rect.centery), 14, 2)

    def draw_direction_arrow(self, screen):
        start_pos = (self.rect.centerx, self.rect.top)  # Đỉnh đầu của nhân vật
        end_pos = (
            self.rect.centerx + 50 * math.cos(self.arrow_angle), 
            self.rect.top - 50 * math.sin(self.arrow_angle)  # Điều chỉnh để mũi tên đi lên
        )
        pygame.draw.line(screen, (0, 255, 0), start_pos, end_pos, 3)

        arrow_length = 10
        arrow_angle = math.pi / 6
        arrow_points = [
            (
                end_pos[0] - arrow_length * math.cos(self.arrow_angle - arrow_angle), 
                end_pos[1] + arrow_length * math.sin(self.arrow_angle - arrow_angle)
            ),
            (
                end_pos[0] - arrow_length * math.cos(self.arrow_angle + arrow_angle), 
                end_pos[1] + arrow_length * math.sin(self.arrow_angle + arrow_angle)
            )
        ]
        pygame.draw.polygon(screen, (0, 255, 0), [end_pos, *arrow_points])

    def update_arrow_angle(self):
        self.arrow_angle += self.arrow_direction * self.arrow_angle_change
        if self.arrow_angle > math.radians(150) or self.arrow_angle < math.radians(30):
            self.arrow_direction *= -1

class Monter(pygame.sprite.Sprite):
    def __init__(self, x, y, images, speed):
        super().__init__()
        self.images = images
        self.image = self.images['idle']
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.is_dodging = False
        self.dodge_distance = 50  # Khoảng cách né đòn tăng lên
        self.dodge_speed = 300  # Tốc độ né đòn nhanh hơn
        self.dodge_direction = 0
        self.move_left = False
        self.move_right = False
        self.current_image_index = 0
        self.running_timer = 0
        self.bullets = pygame.sprite.Group()

        self.skill_sound1 = pygame.mixer.Sound(r"sound\rek3.mp3")
        self.collision_sound = pygame.mixer.Sound(r"sound\bo1skill1.mp3")
        self.skill_animation_duration = 2.1
        # Thời gian hồi chiêu cho mỗi kỹ năng (trong giây)
        self.skill1_cooldown_default = 10
        self.dodge_cooldown_default = 10
        self.skill1_cooldown = 0
        self.skill1_timer = 0  
        self.hit_timer = 0
        self.dodge_cooldown_default = 10
        self.dodge_cooldown = 0

    def update(self, dt, enemy_bullets):

        if self.hit_timer > 0:
            self.hit_timer -= dt
            if self.hit_timer <= 0:
                self.image = self.images['idle']
        elif self.skill1_timer > 0:
            self.skill1_timer -= dt
            if self.skill1_timer <= 0.3:
                self.image = self.images['skill1_end']  # Hình ảnh kết thúc tung chiêu
            elif self.skill1_timer <= 0:
                self.image = self.images['idle']

            if self.rect.left < 80:
                self.rect.left = 80
                self.is_dodging = False
            elif self.rect.right > 880:
                self.rect.right = 880
                self.is_dodging = False
        elif self.is_dodging:
            dodge_step = self.dodge_speed * dt
            self.rect.x += self.dodge_direction * dodge_step
            self.dodge_distance -= dodge_step
            self.image = self.images['dodge']
            if self.dodge_distance <= 0:
                self.is_dodging = False
                self.dodge_distance = 200

            if self.rect.left < 80:
                self.rect.left = 80
                self.is_dodging = False
            elif self.rect.right > 880:
                self.rect.right = 880
                self.is_dodging = False

        elif self.move_left and self.rect.left > 80:
            self.rect.x -= self.speed * dt
            self.image = self.images['run_left'][self.current_image_index // 10]
            self.current_image_index += 1
            if self.current_image_index >= len(self.images['run_left']) * 10:
                self.current_image_index = 0

        elif self.move_right and self.rect.right < 880:
            self.rect.x += self.speed * dt
            self.image = self.images['run_right'][self.current_image_index // 10]
            self.current_image_index += 1
            if self.current_image_index >= len(self.images['run_right']) * 10:
                self.current_image_index = 0
        else:
            self.image = self.images['idle']

        self.bullets.update(dt)
        for bullet in self.bullets:
            if bullet.range_limit:
                distance_traveled = math.hypot(bullet.rect.centerx - bullet.start_x, bullet.rect.centery - bullet.start_y)
                if distance_traveled >= bullet.range_limit:
                    bullet.kill()

        self.skill1_cooldown = max(0, self.skill1_cooldown - dt)
        self.dodge_cooldown = max(0, self.dodge_cooldown - dt)

    def dodge(self):
        if not self.is_dodging:
            self.is_dodging = True
            self.dodge_direction = random.choice([-1, 1])
            self.dodge_cooldown = self.dodge_cooldown_default 

    def fire_skill1(self):
        bullet_image = pygame.image.load(r"bgon\mmm.png")
        direction = self.get_bullet_direction()
        angle = self.get_bullet_angle(direction)
        rotated_image = pygame.transform.rotate(bullet_image, angle)
        bullet = Bulletmonter(self.rect.centerx, self.rect.top, direction, rotated_image, damage=2)
        self.bullets.add(bullet)
        self.skill_sound1.play()
        bullet.range_limit = 150
        self.skill1_cooldown = self.skill1_cooldown_default
        self.image = self.images['skill1_start'] 
        self.skill1_timer = self.skill_animation_duration

    def get_bullet_direction(self):
        angle = random.uniform(math.radians(0), math.radians(3))
        return math.cos(angle), -math.sin(angle)

    def get_bullet_angle(self, direction):
        # direction là tuple chứa hướng của viên đạn (dx, dy)
        return math.degrees(math.atan2(-direction[1], direction[0]))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        self.bullets.draw(screen)

    def ai(self, target_x=None):
        # Tự động thực hiện hành động
        if random.random() < 0.005:
            self.fire_skill1()  # Có xác suất rất nhỏ sẽ sử dụng skill 1
        elif random.random() < 0.02:
            self.dodge()  # Có xác suất nhất định sẽ tránh đòn
        # Tự động di chuyển
        if target_x is not None:
            if self.rect.centerx < target_x - 50:
                self.move_right = True
                self.move_left = False
            elif self.rect.centerx > target_x + 50:
                self.move_left = True
                self.move_right = False
            else:
                self.move_left = False
                self.move_right = False

class Bulletmonter(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image, damage):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 100
        self.direction = direction
        self.damage = damage
        self.start_x = x
        self.start_y = y
        self.range_limit = None
        self.has_hit = False  # Thêm thuộc tính này

    def update(self, dt):
        self.rect.x += self.speed * self.direction[0] * dt
        self.rect.y += self.speed * self.direction[1] * dt + 140
        if self.range_limit:
            distance_traveled = math.hypot(self.rect.centerx - self.start_x, self.rect.centery - (self.start_y ))
            if distance_traveled >= self.range_limit:
                self.kill()
        else:
            if self.rect.bottom < 0 or self.rect.top > 540 or self.rect.right < 0 or self.rect.left > 960:
                self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image, damage):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 450
        self.direction = direction
        self.damage = damage
        self.start_x = x
        self.start_y = y
        self.range_limit = None
        self.has_hit = False  # Thêm thuộc tính này

    def update(self, dt):
        self.rect.x += self.speed * self.direction[0] * dt
        self.rect.y += self.speed * self.direction[1] * dt
        if self.range_limit:
            distance_traveled = math.hypot(self.rect.centerx - self.start_x, self.rect.centery - self.start_y)
            if distance_traveled >= self.range_limit:
                self.kill()
        else:
            if self.rect.bottom < 0 or self.rect.top > 540 or self.rect.right < 0 or self.rect.left > 960:
                self.kill()

class TrailBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image, damage, trail_image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 400
        self.direction = direction
        self.damage = damage
        self.rect.center = (x, y)
        self.start_x = x
        self.start_y = y
        self.range_limit = None
        self.has_hit = False
        self.trail_image = trail_image
        self.trail = []

    def update(self, dt):
        self.rect.x += self.speed * self.direction[0] * dt
        self.rect.y += self.speed * self.direction[1] * dt
        self.trail.append((self.rect.centerx, self.rect.centery))
        
        if len(self.trail) > 100:  # Giới hạn số lượng vệt đạn
            self.trail.pop(0)

        if self.range_limit:
            distance_traveled = math.hypot(self.rect.centerx - self.start_x, self.rect.centery - self.start_y )
            if distance_traveled >= self.range_limit:
                self.kill()
        else:
            if self.rect.bottom < 0 or self.rect.top > 540 or self.rect.right < 0 or self.rect.left > 960:
                self.kill()

    def get_bullet_angle(self):
        return math.degrees(math.atan2(-self.direction[1], self.direction[0]))

    def get_bullet_direction(self):
        angle = random.uniform(math.radians(30), math.radians(150))
        return math.cos(angle), -math.sin(angle)

    def draw(self, screen):
        for pos in self.trail:
            screen.blit(self.trail_image, pos)
        screen.blit(self.image, self.rect.topleft)

class CharacterSelection(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WORLD OR WAR")
        icon_image = Image.open(r'assets\avt3.png')
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.iconphoto(False, icon_photo)

        # Dictionary to map backgrounds to their corresponding music files
        self.background_music_map = {
            "xola.png": "gf.mp3",
            "p3.png": "themekafka.mp3",
            "eve2.png": "themeshank.mp3",
        }

        # Select a random background and its corresponding music
        self.selected_background = random.choice(list(self.background_music_map.keys()))

        # Open the image and resize it
        bg_image_original = Image.open(f'bg/{self.selected_background}')
        bg_image_resized = bg_image_original.resize((960, 540))  # Set the desired width and height here

        # Create a PhotoImage object from the resized image
        self.bg_image = ImageTk.PhotoImage(bg_image_resized)

        # Create a label for the background image and place it
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # self.label = tk.Label(self, text="Choose your character:")
        # self.label.place(x=400, y=20)  

        self.characters = ["Luffynv", "Rogernv", "Yamatonv"]
        self.character_names = {
            "Luffynv": "Monkey D. Luffy",
            "Rogernv": "Gol D. Roger",
            "Yamatonv": "Yamato"
        }
        self.selected_character = tk.StringVar(value=self.characters[0])

        # Load and resize character images
        self.character_images = {
            "Luffynv": ImageTk.PhotoImage(Image.open(r'assets/avtluffy.png').resize((100, 100))),
            "Rogernv": ImageTk.PhotoImage(Image.open(r'assets/avtroger2.png').resize((100, 100))),
            "Yamatonv": ImageTk.PhotoImage(Image.open(r'assets/yamatoavt.png').resize((100, 100)))
        }

        self.character_labels = {}
        self.character_buttons = {}

        # Set initial positions for characters
        positions = {
            "Luffynv": (30, 140),  
            "Rogernv": (140, 140),
            "Yamatonv": (30, 280)
        }

        for character in self.characters:
            x, y = positions[character]
            character_button = tk.Button(self, image=self.character_images[character], command=lambda c=character: self.select_character(c))
            character_button.place(x=x, y=y)
            self.character_buttons[character] = character_button

            label = tk.Label(self, text=self.character_names[character])
            label.place(x=x, y=y + 110)  # Position label below the button
            self.character_labels[character] = label

        # Load the start game 
        self.start_image = ImageTk.PhotoImage(Image.open(r'assets/startgame.png').resize((120, 107)))
        self.start_button = tk.Button(self, image=self.start_image, command=self.confirm_start)
        self.start_button.place(x=826, y=420) 

        # Load the start game 
        self.info_image = ImageTk.PhotoImage(Image.open(r'btn/info.png').resize((266, 115)))
        self.info_button = tk.Button(self, image=self.info_image, command=self.confirm_reset)
        self.info_button.place(x=0, y=0) 

        # Load the rank 
        self.rank_image = ImageTk.PhotoImage(Image.open(r'btn/rank.png').resize((270, 107)))
        self.rank_button = tk.Button(self, image=self.rank_image)
        self.rank_button.place(x=536, y=420) 

        # Load the other
        self.other_image = ImageTk.PhotoImage(Image.open(r'btn/btnother.png').resize((30, 28)))
        self.other_button = tk.Button(self, image=self.other_image)
        self.other_button.place(x=900, y=10) 

        # Load the gift
        self.gift_image = ImageTk.PhotoImage(Image.open(r'btn/btngift.png').resize((30, 28)))
        self.gift_button = tk.Button(self, image=self.gift_image)
        self.gift_button.place(x=850, y=10) 

        # Load the shop
        self.shop_image = ImageTk.PhotoImage(Image.open(r'btn/btnshop.png').resize((30, 28)))
        self.shop_button = tk.Button(self, image=self.shop_image, command= self.start_shop)
        self.shop_button.place(x=800, y=10) 

        # Load 
        self.vach_image = ImageTk.PhotoImage(Image.open(r'btn/vach.png').resize((2, 300)))
        self.vach_button = tk.Button(self, image=self.vach_image)
        self.vach_button.place(x=265, y=140) 

        self.vach_image2 = ImageTk.PhotoImage(Image.open(r'btn/vach.png').resize((160, 2)))
        self.vach_button = tk.Button(self, image=self.vach_image2)
        self.vach_button.place(x=0, y=533) 

        self.vach_image3 = ImageTk.PhotoImage(Image.open(r'btn/vach.png').resize((440, 2)))
        self.vach_button = tk.Button(self, image=self.vach_image3)
        self.vach_button.place(x=536, y=407) 

        self.geometry("960x540")  
        self.update_label_colors()
        pygame.mixer.init()
        self.play_random_music()
        # play_background_music()
        self.playing_game = False

    def select_character(self, character):
        self.selected_character.set(character)
        self.update_label_colors()

    def update_label_colors(self):
        for character in self.characters:
            if self.selected_character.get() == character:
                self.character_labels[character].config(fg="red")
            else:
                self.character_labels[character].config(fg="black")

    def play_random_music(self):
        music_files = [self.background_music_map[bg] for bg in self.background_music_map]
        if music_files:
            random_music = random.choice(music_files)
            music_path = os.path.join('music', random_music)
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1) 

    def start_game(self):
        self.playing_game = True
        character = self.selected_character.get()
        self.destroy()
        start_game_with_character(character)
        self.play_background_music()  

    def start_shop(self):
        self.running =True
        self.destroy()
        shop()
        self.play_random_music()

    def restart_game(self):
        # pygame.mixer.music.stop()  
        self.playing_game = False  
        self.play_random_music()  # Select new background music
        self.destroy()
        app = CharacterSelection()
        app.mainloop()

    def confirm_reset(self):
        confirm = messagebox.askyesno("Reset Game", "Are you sure you want to reset the game?")
        if confirm:
            self.restart_game()

    def confirm_start(self):
        confirm = messagebox.askyesno("Run Game", "Are you ready?")
        if confirm:
            self.start_game()


def play_background_music():
    music_dir = 'music'
    music_files = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
    if music_files:
        random_music = random.choice(music_files)
        music_path = os.path.join(music_dir, random_music)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()  # Play once

# Hàm xử lý sự kiện khi một bài nhạc kết thúc
def handle_music_end_event():
    pygame.mixer.music.stop()  # Stop current music
    play_background_music()    # Play next music

class WinnerScreen(tk.Tk):
    def __init__(self, winner):
        super().__init__()
        self.title("Game Over")
        self.geometry("960x540")

        # Background
        bg_image_original = Image.open(f'shop/bg3.png')  
        self.bg_image = ImageTk.PhotoImage(bg_image_original)
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Winner label
        self.winner_label = tk.Label(self, text=f"{winner} !", font=("Arial", 24), fg="blue")
        self.winner_label.place(x=400, y=200)

        # Restart button
        self.restart_image = ImageTk.PhotoImage(Image.open(r'shop/home.png'))
        self.restart_button = tk.Button(self, image=self.restart_image, command=self.restart_game)
        self.restart_button.place(x=420, y=300)

    def restart_game(self):
        self.destroy()
        app = CharacterSelection()
        app.mainloop()

def show_winner_and_restart(winner):
    pygame.mixer.music.stop() 
    pygame.quit()  
    winner_screen = WinnerScreen(winner)
    winner_screen.mainloop()

# Function to display and update countdown timer
def countdown_timer(screen, game_start_time, font):
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - game_start_time) / 1000
    remaining_time = max(0, game_duration - elapsed_time)
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)

    # Check if game time is over
    if remaining_time <= 0:
        show_winner_and_restart("DEFEAT!")
        return

    # Display countdown timer at the top center of the screen
    timer_text = f"Time left: {minutes:02}:{seconds:02}"
    timer_render = font.render(timer_text, True, (255, 255, 255))
    screen.blit(timer_render, (480 - timer_render.get_width() // 2, 10))

def shop():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((960, 540))
    return_to_home = False
    running = True
    play_background_music()
    pygame.event.clear(pygame.USEREVENT)
    pygame.time.set_timer(pygame.USEREVENT, 1000) 
    x=0
    y=0
    z= 500
    while running:
        bg = pygame.image.load(r'shop\bg3.png')     
        screen.blit(bg, (0, 0))
        home = pygame.image.load(r'shop\home.png')     
        home_hcn = screen.blit(home, (10, 10))        
        ruby = pygame.image.load(r'shop\ruby.png')     
        ruby_hcn = screen.blit(ruby, (800, 10))  
        money = pygame.image.load(r'shop\money.png')     
        money_hcn = screen.blit(money, (640, 10))  
        jade = pygame.image.load(r'shop\jade.png')     
        jade_hcn = screen.blit(jade, (10, y+140))  
        arg = pygame.image.load(r'shop\arg.png')     
        arg_hcn = screen.blit(arg, (10, y+220))
        jade2 = pygame.image.load(r'shop\jade2.png')     
        jade2_hcn = screen.blit(jade2, (10, z+140))  
        arg2 = pygame.image.load(r'shop\arg2.png')     
        arg2_hcn = screen.blit(arg2, (10, z+220))      
        bgjade = pygame.image.load(r'shop\bgjade2.png')     
        screen.blit(bgjade, (160, 100 + y )) 
        bgkafka = pygame.image.load(r'shop\bgkafka.png')     
        screen.blit(bgkafka, (160, 100 + z)) 
        quay = pygame.image.load(r'shop\quay.png')     
        quay_hcn = screen.blit(quay, (730, 480))
        quay5 = pygame.image.load(r'shop\quay6.png')     
        quay5_hcn = screen.blit(quay5, (550, 480))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                if not pygame.mixer.music.get_busy():
                    handle_music_end_event()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if home_hcn.collidepoint(event.pos):
                    running = False
                    return_to_home = True
                elif arg_hcn.collidepoint(mouse_x, mouse_y):
                    y= 500
                    z= 0  
                elif jade2_hcn.collidepoint(mouse_x, mouse_y):
                    y= 0
                    z= 500 
                elif quay_hcn.collidepoint(mouse_x, mouse_y):
                    pygame.mixer.music.stop()
                    gacha()
                elif quay5_hcn.collidepoint(mouse_x, mouse_y):
                    pygame.mixer.music.stop()
                    gacha()

        pygame.display.flip()
    pygame.quit()
    if return_to_home:
        # CharacterSelection().mainloop()
        CharacterSelection().restart_game()
    else:
        sys.exit() 

def gacha():
    pygame.init()
    screen = pygame.display.set_mode((940, 540))
    video_path = r'video\gacha.mp4'  # Thay đường dẫn bằng đường dẫn thực tế đến video của bạn
    cap = cv2.VideoCapture(video_path)
    sound = pygame.mixer.Sound(r"sound\xxx.mp3")
    # Lấy kích thước video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Xác định vị trí ban đầu của video trên màn hình
    video_x = -350
    video_y = -60

    # Phát video
    clock = pygame.time.Clock()
    while True:
        sound.play()
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.image.frombuffer(frame.tostring(), (frame_width, frame_height), "RGB")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        screen.blit(frame, (video_x, video_y))
        pygame.display.flip()
        clock.tick(60)
    cap.release()
    pygame.quit()
    shop()

def start_game_with_character(character):
    pygame.init()
    screen = pygame.display.set_mode((960, 540))
    clock = pygame.time.Clock()
    running = True
    return_to_home = False
    # Play background music
    play_background_music()
    pygame.event.clear(pygame.USEREVENT)
    pygame.time.set_timer(pygame.USEREVENT, 1000) 

    run_images_right = [
        pygame.image.load(r'assets\chayphai.png'),
        pygame.image.load(r'assets\dichuyen111.png'),
        pygame.image.load(r'assets\dichuyen1.png')
    ]
    run_images_left = [
        pygame.image.load(r'assets\chaytrai.png'),
        pygame.image.load(r'assets\dichuyen222.png'),
        pygame.image.load(r'assets\dichuyen2.png')
    ] 
    images = {
        'idle': pygame.image.load(r'assets\2.png'),
        'run_right': run_images_right,
        'run_left': run_images_left,
        'dodge': pygame.image.load(r'assets\dodge.png'),
        'hit' : pygame.image.load(r'assets\dodge.png'),
        'skill1_start': pygame.image.load(r'assets\skillroger1.png'),
        'skill2_start': pygame.image.load(r'assets\skillroger2.png'),
        'skill1_end': pygame.image.load(r'assets\skillroger11.png'),
        'skill2_end': pygame.image.load(r'assets\skillroger22.png'),
    }

    rogerai = RogerAInv(300, 50, images, speed=200, jump_height=400, health=100)

    run_images_right = [
        pygame.image.load(r'bgon\rek6.png'),
        pygame.image.load(r'bgon\rek6.png'),
    ]
    run_images_left = [
        pygame.image.load(r'bgon\rek5.png'),
        pygame.image.load(r'bgon\rek5.png'),
    ] 
    imagesrek = {
        'idle': pygame.image.load(r'bgon\rek6.png'),
        'run_right': run_images_right,
        'run_left': run_images_left,
        'dodge': pygame.image.load(r'bgon\rek6.png'),
        'skill1_start': pygame.image.load(r'bgon\rek8.png'),
        'skill1_end': pygame.image.load(r'bgon\rek7.png'),
    }

    rek = Monter(300, 130, imagesrek, speed=100)

    run_images_right = [
        pygame.image.load(r'assets\luffybinhthuong1.png'),
        pygame.image.load(r'assets\luffybinhthuong2.png'),
        pygame.image.load(r'assets\luffybinhthuong3.png'),
    ]
    run_images_left = [
        pygame.image.load(r'assets\luffybinhthuong1trai.png'),
        pygame.image.load(r'assets\luffybinhthuong2trai.png'),
        pygame.image.load(r'assets\luffybinhthuong3trai.png'),
    ]

    imagesluffy = {
        'idle': pygame.image.load(r'assets\luffy.png'),
        'run_right': run_images_right,
        'run_left': run_images_left,
        'dodge': pygame.image.load(r'assets\luffydodge2.png'),
        'hit': pygame.image.load(r'assets\luffydodge2.png'),
        'skill1_start': pygame.image.load(r'assets\luffy4.png'),
        'skill2_start': pygame.image.load(r'assets\luffy44.png'),
        'skill1_end': pygame.image.load(r'assets\luffygay1.png'),
        'skill2_end': pygame.image.load(r'assets\luffybeo1.png'),
    }

    luffyai = LuffyAInv(300, 50, imagesluffy, speed=200, jump_height=400, health=100)

    # Random kẻ địch
    enemy = random.choice([luffyai, rogerai])

    if character == "Luffynv":
        run_images_right = [
            pygame.image.load(r'assets\luffybinhthuong1.png'),
            pygame.image.load(r'assets\luffybinhthuong2.png'),
            pygame.image.load(r'assets\luffybinhthuong3.png'),
        ]
        run_images_left = [
            pygame.image.load(r'assets\luffybinhthuong1trai.png'),
            pygame.image.load(r'assets\luffybinhthuong2trai.png'),
            pygame.image.load(r'assets\luffybinhthuong3trai.png'),
        ]

        imagesluffy = {
            'idle': pygame.image.load(r'assets\luffy.png'),
            'run_right': run_images_right,
            'run_left': run_images_left,
            'dodge': pygame.image.load(r'assets\luffydodge2.png'),
            'hit': pygame.image.load(r'assets\luffydodge2.png'),
            'skill1_start': pygame.image.load(r'assets\luffy4.png'),
            'skill2_start': pygame.image.load(r'assets\luffy44.png'),
            'skill1_end': pygame.image.load(r'assets\luffygay1.png'),
            'skill2_end': pygame.image.load(r'assets\luffybeo1.png'),
        }
        player = Luffynv(300, 380, imagesluffy, speed=200, jump_height=400, health=100)

    elif character == "Rogernv":
        run_images_right = [
            pygame.image.load(r'assets\chayphai.png'),
            pygame.image.load(r'assets\dichuyen111.png'),
            pygame.image.load(r'assets\dichuyen1.png')
        ]
        run_images_left = [
            pygame.image.load(r'assets\chaytrai.png'),
            pygame.image.load(r'assets\dichuyen222.png'),
            pygame.image.load(r'assets\dichuyen2.png')
        ] 
        images = {
            'idle': pygame.image.load(r'assets\2.png'),
            'run_right': run_images_right,
            'run_left': run_images_left,
            'dodge': pygame.image.load(r'assets\dodge.png'),
            'hit' : pygame.image.load(r'assets\dodge.png'),
            'skill1_start': pygame.image.load(r'assets\skillroger1.png'),
            'skill2_start': pygame.image.load(r'assets\skillroger2.png'),
            'skill1_end': pygame.image.load(r'assets\skillroger11.png'),
            'skill2_end': pygame.image.load(r'assets\skillroger22.png'),
        }
        player = Rogernv(300, 380, images, speed=200, jump_height=400, health=100)
    elif character == "Yamatonv":
        run_images_right = [
            pygame.image.load(r'assets\yamato1.png'),
            pygame.image.load(r'assets\yamato2.png'),
            pygame.image.load(r'assets\yamato3.png')
        ]
        run_images_left = [
            pygame.image.load(r'assets\yamatotrai1.png'),
            pygame.image.load(r'assets\yamatotrai2.png'),
            pygame.image.load(r'assets\yamatotrai3.png')
        ] 
        images = {
            'idle': pygame.image.load(r'assets\yamato.png'),
            'run_right': run_images_right,
            'run_left': run_images_left,
            'dodge': pygame.image.load(r'assets\yamatododge.png'),
            'hit': pygame.image.load(r'assets\yamatododge.png'),
            'skill1': pygame.image.load(r'assets\yamatoskill1.png'),
            'skill2': pygame.image.load(r'assets\yamatoskill2.png')
        }
        player = Yamatonv(300, 380, images, speed=200, jump_height=400, health=100)


    # Game timer variables
    game_start_time = pygame.time.get_ticks()  # Get current time in milliseconds
    font = pygame.font.Font(None, 36)  # Font for timer display
    x=0
    y=0
    back_button_rect = pygame.Rect(10, 10, 80, 40)

    def draw_back_button():
        pygame.draw.rect(screen, (255, 0, 0), back_button_rect)
        text_surface = font.render("QUIT", True, (255, 255, 255))
        screen.blit(text_surface, (20, 20))
    while running:
        dt = clock.tick(60) / 1200

        bgr1 = pygame.image.load(r'bgon\bgsea21.png')
        x1= screen.blit(bgr1, (x, 0)) 
        bgr2 = pygame.image.load(r'bgon\bgsea23.png')
        x2=screen.blit(bgr2, (x+960, 0))
        bgr1 = pygame.image.load(r'bgon\bgsea21.png')
        x1= screen.blit(bgr1, (x + 1920, 0))  

        bgr3 = pygame.image.load(r'bgon\bgsea22.png')
        x3= screen.blit(bgr3, (y, 270)) 
        bgr4 = pygame.image.load(r'bgon\bgsea24.png')
        x4= screen.blit(bgr4, (y-960, 270)) 
        bgr3 = pygame.image.load(r'bgon\bgsea22.png')
        x3= screen.blit(bgr3, (y - 1920, 270)) 
        x -= 10
        y +=10
        if x <= -1920:
            x = 0
        if y >= 1920:
            y =0
        khobau = pygame.image.load(r'bgon\tau6.png')     
        screen.blit(khobau, (100, 110))
        bau = pygame.image.load(r'bgon\tau11.png')     
        screen.blit(bau, (100, 400))
        ys = pygame.image.load(r'bgon\yasuo2.png')     
        screen.blit(ys, (200, 400))
        zed = pygame.image.load(r'bgon\zed5.png')     
        screen.blit(zed, (670, 90))
        btntrai = pygame.image.load(r'assets\btntrai2.png')
        btnphai = pygame.image.load(r'assets\btnphai2.png')
        btnlen = pygame.image.load(r'assets\skill1.png')
        btnxuong = pygame.image.load(r'assets\skill2.png')
        btnnhay = pygame.image.load(r'assets\skillnhay.png')
        btntrai_hcn = screen.blit(btntrai, (15, 400))
        btnphai_hcn = screen.blit(btnphai, (85, 400))
        btnnhay_hcn = screen.blit(btnnhay, (780, 330))
        btnlen_hcn = screen.blit(btnlen, (820, 280))
        btnxuong_hcn = screen.blit(btnxuong, (880, 260))

        countdown_timer(screen, game_start_time, font) 
        #nhan vat
        target_x = 482  # Trung tâm màn hình
        enemy.ai(target_x)      
        enemy.update(dt,player.bullets)
        enemy.draw(screen)
        rek.ai(target_x)
        rek.update(dt, enemy)
        rek.draw(screen) 
        player.update(dt,enemy.bullets) 
        player.update(dt, rek.bullets) 
        player.draw(screen)

        enemy.update(dt, rek.bullets)
        if isinstance(player, Luffynv):
            for bullet in player.bullets:
                bullet.draw(screen)
        if isinstance(enemy, LuffyAInv):
            for bullet in enemy.bullets:
                bullet.draw(screen)
        # Calculate elapsed time since game started
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - game_start_time) / 1000  # Convert milliseconds to seconds

        # Calculate remaining time
        remaining_time = max(0, game_duration - elapsed_time)
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)

        # Check if game time is over
        if remaining_time <= 0:
            show_winner_and_restart("DEFEAT!")
            return
        # Check for game over condition
        if player.health <= 0:
            show_winner_and_restart("DEFEAT!")
            running = False
        elif enemy.health <= 0:
            show_winner_and_restart("VICTORY!!!")
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                if not pygame.mixer.music.get_busy():
                    handle_music_end_event()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left = True
                elif event.key == pygame.K_RIGHT:
                    player.move_right = True
                elif event.key == pygame.K_DOWN:
                    player.fire_skill1()
                elif event.key == pygame.K_UP:
                    player.fire_skill2()
                elif event.key == pygame.K_SPACE:
                    player.dodge()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.move_left = False
                elif event.key == pygame.K_RIGHT:
                    player.move_right = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if btntrai_hcn.collidepoint(mouse_x, mouse_y):
                    player.move_left = True
                elif btnphai_hcn.collidepoint(mouse_x, mouse_y):
                    player.move_right = True
                elif btnxuong_hcn.collidepoint(mouse_x, mouse_y):
                    player.fire_skill1()
                elif btnlen_hcn.collidepoint(mouse_x, mouse_y):
                    player.fire_skill2()
                elif btnnhay_hcn.collidepoint(mouse_x, mouse_y):
                    player.dodge()
                elif back_button_rect.collidepoint(event.pos):
                    running = False
                    return_to_home = True
                    # CharacterSelection().restart_game()
            elif event.type == pygame.MOUSEBUTTONUP:
                if btntrai_hcn.collidepoint(mouse_x, mouse_y):
                    player.move_left = False
                elif btnphai_hcn.collidepoint(mouse_x, mouse_y):
                    player.move_right = False

        draw_back_button()
        pygame.display.flip()

        # Check game end condition
        if pygame.time.get_ticks() - game_start_time >= game_duration * 1000:
            show_winner_and_restart("No One")  # Handle game over

    pygame.quit()
    if return_to_home:
        CharacterSelection().mainloop()
        CharacterSelection().restart_game()
    else:
        sys.exit() 

def return_to_character_selection():
    app = CharacterSelection()
    app.restart_game()
    app.mainloop()

if __name__ == "__main__":
    app = CharacterSelection()
    app.mainloop()
