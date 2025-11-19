
# -------------------------------
# 🐸 Wise Frog - Game Setup Module
# -------------------------------

import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
from shop_screen import run_shop_screen
from pyth import monster_hunting
from menu import Menu 
from guide import run_guide_screen

pygame.init()
screen = pygame.display.set_mode((1500, 750))  # اندازه مطابق با WIDTH و HEIGHT

# ----audio system and load sound effects----
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

coin_sound = pygame.mixer.Sound("data/music/sounds/Coin.wav")
croak_sound = pygame.mixer.Sound("data/music/sounds/Croak.wav")

pygame.display.set_caption(".::Wise Frog::.")
icon = pygame.image.load("data/frog-prince.png")
pygame.display.set_icon(icon)

# ----Background music playlist and track cycling----
background_track = [
    "data/music/main/bg1.mp3",
    "data/music/main/bg2.mp3"
]

current_track = 0


def play_next_track():
    global current_track
    pygame.mixer.music.load(background_track[current_track])
    pygame.mixer.music.play()
    current_track = (current_track + 1) % len(background_track)


# screen wigh and hight
WIDTH, HIGHT = 1500, 750
# زمان بر حسب ثانیه
FPS = 60
# player speed
PLAYER_VEL = 8

window = pygame.display.set_mode((WIDTH, HIGHT))

#----UI icons and decorative images----
heart_img = pygame.image.load("data/Health/life.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (40, 30))

setting_img = pygame.image.load("data/menu/botton/setting.png").convert_alpha()
setting_img = pygame.transform.smoothscale(setting_img, (30, 30))
setting_rect = setting_img.get_rect(topright=(WIDTH - 20, 20))
setting_rotated = setting_img

restart_img = pygame.image.load("data/menu/botton/Restart.png").convert_alpha()
restart_img = pygame.transform.scale(restart_img, (100, 100))

menu_img = pygame.image.load("data/menu/botton/icon/menu.png").convert_alpha()
menu_img = pygame.transform.scale(menu_img, (50, 50))

next_img = pygame.image.load("data/menu/botton/icon/next.png").convert_alpha()
next_img = pygame.transform.scale(next_img, (50, 50))

score_palen = pygame.image.load("data/decoration/decorate/99.png")
score_palen = pygame.transform.scale(score_palen, (200, 200))

key_img = pygame.image.load("data/decoration/decorate/key.png")
key_img = pygame.transform.scale(key_img, (40, 40))

frog_icon = pygame.image.load("data/frog-head.png")
frog_icon = pygame.transform.scale(frog_icon, (50, 30))


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("data", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_block(size):
    path = join("data", "terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_help_block(size):
    path = join("data", "terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 130, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_fires(block_size):
    fires = []
    positions = [(350, HIGHT - block_size * 4 - 64, 16, 32),
                 (900, HIGHT - block_size * 3 - 64, 16, 32),
                 (2300, HIGHT - block_size * 4 - 64, 16, 32),
                 (2525, HIGHT - block_size * 4 - 64, 16, 32),
                 (2730, HIGHT - block_size * 4 - 64, 16, 32),
                 (4800, HIGHT - block_size * 3 - 64, 16, 32),
                 (5250, HIGHT - block_size * 3 - 64, 16, 32),

    ]
    for x, y, w, h in positions:
        fire = Fire(x, y, w, h)
        fire.on()
        fires.append(fire)
    return fires


def make_platform(start_x, y, count, size):
    return [Block(start_x + i * size, y, size) for i in range(count)]

def make_bushs(start_x, y, count, width, height, bush_type = "2", space =70):
    return [Bush(start_x + i * space, y, width, height, bush_type = bush_type) for i in range(count)]

def make_collectibale(start_x, y, count, width, height, item_type = "gold"):
    return [collectible(start_x + i * 40, y, width, height, item_type = item_type) for i in range(count)]

def make_spike(start_x, y, count, width, height, spike_type = "1", space= 20):
    return [Trap(start_x + i * space, y, width, height, spike_type = spike_type) for i in range(count)]



class Player(pygame.sprite.Sprite):

    color = (255, 0, 0)
    GRAVITY = 1
    SPRITES_RAW = load_sprite_sheets("character", "BlueBlue", 48, 33, True)
    SPRITES = {key: [pygame.transform.smoothscale(
        img, (96, 66)) for img in frames] for key, frames in SPRITES_RAW.items()}

    ANIMATION_DELAY = 4

    def __init__(self, x, y, width, height, score_display_list):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.Y_vel = 0
        self.mask = None
        self.direction = "right"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.fall = False
        self.fall_timer = 0
        self.dodge = False
        self.attack = False
        self.hit_cooldown = 60
        self.hit_count = 0
        self.score = 0
        self.health = 5
        self.dead = False
        self.exploding = False
        self.exploding_end = False
        self.score_item_display = score_display_list
        self.effects = []
        self.attack_rect = self.rect.copy()
        self.spits = pygame.sprite.Group()
        self.key_count = 0
        self.visible = True
        self.coins = 0
        self.diamonds = 0
        self.collected_item_images = []  # لیست تصاویر آیتم‌های جمع‌شده
        self.collected_item_counts = {}


    def jump(self):
        self.Y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0
        croak_sound.play()

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        if not self.hit:
            self.hit = True
            self.hit_count = 0
            self.health = max(0, self.health - 1)
            croak_sound.play()

            if self.health == 0:
                self.dead = True
                self.exploding = True
                self.exploding_end = False
                self.animation_count = 0
                self.x_vel = 0
                self.Y_vel = 0

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        if self.exploding:
            self.update_sprite()
            return
        self.Y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.Y_vel)

        if self.rect.top < 0:
            self.rect.top = 0
            self.Y_vel = 0 

        if self.rect.left < 0:
            self.rect.left = 0

        if self.hit:
            self.hit_count += 1
        if self.hit_count >= self.hit_cooldown:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.Y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.Y_vel *= -1

    def shoot_spit(self):
        spit_x = self.rect.centerx
        spit_y = self.rect.centery
        spit = Spit(spit_x, spit_y, self.direction)
        self.spits.add(spit)

    def update_sprite(self):
        if self.exploding and not self.exploding_end:
            sprite_sheet = "Explosion"
            sprite_sheet_name = sprite_sheet + "_" + self.direction
            sprites = self.SPRITES[sprite_sheet_name]
            sprite_index = (self.animation_count // self.ANIMATION_DELAY)
            if sprite_index >= len(sprites):
                self.exploding_end = True
                return
            self.sprite = sprites[sprite_index]
            self.animation_count += 1
            self.update()
            return

        sprite_sheet = "Idle"

        if self.dodge:
            sprite_sheet = "dodge"

        if self.attack:
            sprite_sheet = "attack"
            sprite_sheet_name = sprite_sheet + "_" + self.direction
            sprites = self.SPRITES[sprite_sheet_name]
            sprite_index = (self.animation_count // self.ANIMATION_DELAY)
            if not sprites:
                return
            self.index = self.animation_count // self.ANIMATION_DELAY
            if sprite_index >= len(sprites):
                self.attack = False
                self.animation_count = 0
                return

            self.sprite = sprites[sprite_index]
            self.animation_count += 1
            self.update()
            return

        if self.fall:
            sprite_sheet = "Hurt"
            self.fall_timer += 1
            if self.fall_timer >= 70:
                self.fall = False
                self.fall_timer = 0

        elif self.hit:
            sprite_sheet = "Hurt"

        elif self.Y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump3"
            elif self.jump_count == 2:
                sprite_sheet = "jump3"

        if self.Y_vel > self.GRAVITY * 2:
            sprite_sheet = "Idle"
        if self.x_vel != 0:
            sprite_sheet = "Hop"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def collect_item(self, objects, key_flash, chest_flash, chest_drops):
        item_to_remove = []
        collectible_names = ["gold", "silver", "dimon3", "dimon2",
                             "potion1", "potion2", "potion3", "potion4", "plant", "gem1", "gem2", "gem3", "potions", "key", "chest"]
        for obj in objects:
            if obj.name in collectible_names and self.rect.colliderect(obj.rect):
                if obj.name == "chest":
                    if self.key_count < 1:
                        continue
                item_to_remove.append(obj)
                coin_sound.play()

                if obj.name == "gold":
                    self.score += 1
                    self.coins += 1
                    self.score_item_display.append(ScoreItemDisplay(obj.image))

                if obj.name == "gem3":
                    self.score += 1
                    self.diamonds += 1
                    self.score_item_display.append(ScoreItemDisplay(obj.image))

                if obj.name == "dimon2":
                    self.score += 10
                    self.diamonds += 1
                    self.score_item_display.append(ScoreItemDisplay(obj.image))

                if obj.name == "dimon3":
                    self.score += 15
                    self.diamonds += 2
                    self.score_item_display.append(ScoreItemDisplay(obj.image))

                if obj.name == "gem2":
                    self.score += 1
                    self.diamonds +=1
                    self.score_item_display.append(ScoreItemDisplay(obj.image))

                if obj.name == "plant":
                    self.score += 2
                    self.score_item_display.append(ScoreItemDisplay(obj.image))
                    if obj.image not in self.collected_item_images:
                        self.collected_item_images.append(obj.image)

                    index = self.collected_item_images.index(obj.image)
                    self.collected_item_counts[index] = self.collected_item_counts.get(index, 0) + 1

                if obj.name == "key":
                    key_flash.trigger()
                    self.key_count +=1

                if obj.name == "chest":
                    if self.key_count >= 1:
                        self.key_count -=1
                        chest_flash.trigger()
                        center_x = window.get_width() // 2
                        center_y = window.get_height() // 2

                        potion_image = load_sprite_sheets("item", "potions", 24, 50)["potion1"][0]
                        chest_drops.append(ChestDropEffect(potion_image, center_x, center_y))
                    
                if obj.name == "potions":
                    if self.health < 5:
                        self.health +=1
                    self.score_item_display.append(ScoreItemDisplay(obj.image))
                    self.effects.append(PlusEffect(self.rect.centerx, self.rect.top - 10))
                    if obj.image not in self.collected_item_images:
                        self.collected_item_images.append(obj.image)

                    index = self.collected_item_images.index(obj.image)
                    self.collected_item_counts[index] = self.collected_item_counts.get(index, 0) + 1


        for item in item_to_remove:
            objects.remove(item)
            coin_sound.play()

    def draw(self, win, offset_x):
        if self.visible:
            win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))   
        for effect in self.effects:
            effect.update()
            effect.draw(win, offset_x)
        self.effects = [e for e in self.effects if e.lifetime > 0]

class Spit(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load("data/spit.png").convert_alpha()
        offset_y = 10
        self.rect = self.image.get_rect(center=(x, y + offset_y))
        self.vel = 5 if direction == "right" else -5
        self.start_x = self.rect.x

    def update(self):
        self.rect.x += self.vel
        if abs(self.rect.x - self.start_x) >= 150:
            self.kill()

def check_spit_collision(spits, bees, player, snails, boars):
    # Handle bee collisions
    for spit in spits:
        for bee in bees:
            if bee.alive and spit.rect.colliderect(bee.rect):
                bee.health -= 1
                bee.animation_state = "Hit"
                bee.animation_count = 0
                spit.kill()
                if bee.health <= 0:
                    bee.alive = False
                    player.score += 5
                    coin_sound.play()
                    bees.remove(bee)

    # Handle boar collisions
    for spit in spits:
        for boar in boars:
            if boar.alive and spit.rect.colliderect(boar.rect):
                boar.health -= 1
                boar.animation_state = "Hit"
                boar.animation_count = 0
                spit.kill()
                if boar.health <= 0:
                    boar.alive = False
                    player.score += 5
                    coin_sound.play()
                    bees.remove(bee)

# Handle snail collisions
    for spit in spits:
        for snail in snails:
            if snail.alive and spit.rect.colliderect(snail.rect):
                snail.hit_count += 1
                snail.animation_state = "Hit"
                snail.animation_count = 0
                spit.kill()
                if snail.hit_count >= 4:
                    snail.animation_state = "Die"
                    snail.animation_count = 0
                    snail.alive = False
                    player.score += 5
                    coin_sound.play()


class SettingIcon:
    def __init__(self, name, img_path, size, offset_y):
        self.name = name
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, size)
        self.rect = self.image.get_rect()
        self.offset_y = offset_y
        self.visible = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self, rect):
        self.rect.midtop = (rect.centerx, rect.bottom + self.offset_y)

    def draw(self, window):
        if self.visible:
            window.blit(self.image, self.rect)

    def clicked(self, mouse_pos):
        return self.visible and self.rect.collidepoint(mouse_pos)


class TutorialCharacter:
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 50
        self.height = 60
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.X_vel = 0
        self.Y_vel = 0
        # self.gravity = 1

        self.sprite = pygame.image.load(
            "data/character/Gobo/gobo2.png").convert_alpha()
        self.sprite = pygame.transform.smoothscale(self.sprite, (80, 100))
        self.mask = pygame.mask.from_surface(self.sprite)

        self.scale_timer = 0
        self.base_size = (80, 100)
        self.scale_range = (0.9, 1.1)

        self.jumping = False
        self.jump_offset = 0
        self.jump_height = 10
        self.jump_direct = -1

        self.dodging = False
        self.dodge_offset = 0
        self.dodge_height = 15
        self.dodge_direct = 1

    def move_left(self, vel):
        self.X_vel = -vel

    def move_right(self, vel):
        self.X_vel = vel

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jump_offset = 0
            self.jump_direct = -1

    def dodge(self):
        if not self.dodging:
            self.dodging = True
            self.dodge_offset = 0
            # self.dodge_direct = -1

    def stop(self):
        self.X_vel = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.mask = pygame.mask.from_surface(self.sprite)

# Apply pulsing scale and blue tint animation
    def animation(self):
        self.scale_timer += 1

        wave = math.sin(self.scale_timer * 0.1)
        self.current_scale = 1.0 + wave * 0.1

        tint = int((math.sin(self.scale_timer * 0.1) + 1) * 100)
        tint_surface = pygame.Surface(self.sprite.get_size(), pygame.SRCALPHA)
        tint_surface.fill((tint, tint, 255, 30))
        self.sprite.blit(tint_surface, (0, 0),
                         special_flags=pygame.BLEND_RGBA_ADD)

        new_width = int(self.base_size[0] * self.current_scale)
        new_height = int(self.base_size[1] * self.current_scale)
        self.sprite = pygame.transform.smoothscale(
            pygame.image.load("data/character/Gobo/gobo2.png").convert_alpha(),
            (new_width, new_height)
        )
        self.mask = pygame.mask.from_surface(self.sprite)

    def loop(self):
        self.x += self.X_vel
        self.rect.x = self.x
        if self.jumping:
            self.y += self.jump_direct * 8
            self.rect.y = self.y
            self.jump_offset += 1

            if self.jump_offset >= self.jump_height:
                if self.jump_direct == -1:
                    self.jump_direct = 1
                    self.jump_offset = 0
                else:
                    self.jumping = False

        if self.dodging:
            self.y += self.dodge_direct * 2
            self.rect.y = self.y
            self.dodge_offset += 1

            if self.dodge_offset >= self.dodge_height:
                if self.dodge_direct == 1:
                    self.dodge_direct = -1
                    self.dodge_offset = 0
                else:
                    self.dodging = False
                    self.dodge_offset = 0
                    self.dodge_direct = 1

        self.animation()

    def draw(self, surface, offset_x=0):
        # glow = pygame.Surface(self.sprite.get_size(), pygame.SRCALPHA)
        # glow.fill((100, 100, 255, 40))  # هاله‌ی آبی با شفافیت
        sprite_rect = self.sprite.get_rect(midbottom=self.rect.midbottom)
        # surface.blit(glow, (sprite_rect.x - offset_x, sprite_rect.y))
        surface.blit(self.sprite, (sprite_rect.x - offset_x, sprite_rect.y))


class Tutorial:
    def __init__(self, size, pos,):

        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect(center=pos)
        self.tutorial_bg = pygame.image.load("data/background/b2.png")

        # Load frame and UI button images
        self.frame_image = pygame.image.load("data/decoration/frame/frame.png").convert_alpha()
        self.frame_image = pygame.transform.smoothscale(self.frame_image, (300, 500))

        self.exit_img = pygame.image.load("data/menu/botton/exit.png")
        self.exit_button = pygame.transform.smoothscale(self.exit_img, (44, 44))
        self.exit_rect = pygame.Rect(755, 0, 44, 44)

        self.left_button = pygame.image.load("data/menu/botton/left.png")
        self.left_button = pygame.transform.smoothscale(self.left_button, (50, 50))
        self.left_rect = pygame.Rect(445, 100, 50, 50)

        self.right_button = pygame.image.load("data/menu/botton/right.png")
        self.right_button = pygame.transform.smoothscale(self.right_button, (50, 50))
        self.right_rect = pygame.Rect(305, 100, 50, 50)

        self.down_button = pygame.image.load("data/menu/botton/down.png")
        self.down_button = pygame.transform.smoothscale(self.down_button, (50, 50))
        self.down_rect = pygame.Rect(375, 100, 50, 50)

        self.space_button = pygame.image.load("data/menu/botton/space.png")
        self.space_button = pygame.transform.smoothscale(self.space_button, (170, 45))
        self.space_rect = pygame.Rect(312, 200, 50, 50)

        # Hover state flags
        self.hovering_right = False
        self.hovering_left = False
        self.hovering_space = False
        self.hovering_down = False

        self.corner_tl = self.frame_image.subsurface(pygame.Rect(30, 115, 44, 47))
        self.edge_top = self.frame_image.subsurface(pygame.Rect(74, 115, 152, 47))
        self.edge_left = self.frame_image.subsurface(pygame.Rect(30, 162, 44, 136))
        
        # Initialize tutorial character and demo objects
        self.character = TutorialCharacter(30, 337)
        self.objects = self.demo_objects()
        self.offset_x = 0
        self.frame = 0
        self.active = False

    def demo_objects(self):
        block_size = 96
        floor = [HelpBlock(i * block_size, 370, block_size) for i in range(10)]
        coin = collectible(300, 150, 16, 16, item_type="gold")
        return [*floor, coin]

    # Start and reset character position and state
    def start(self):
        self.active = True
        self.frame = 0
        surface_width = self.surface.get_width()
        self.x_start = surface_width // 2 - self.character.width // 2
        self.character.x = self.x_start
        self.character.y = 350 - self.character.height

        self.character.rect.x = self.character.x
        self.character.rect.y = self.character.y
        self.character.X_vel = 0
        self.character.Y_vel = 0
        self.offset_x = 0

    # Update character movement based on hover states
    def update(self):
        if not self.active:
            return

        if self.hovering_space:
            self.character.jump()

        if self.hovering_down:
            self.character.dodge()

        if self.hovering_left:
            self.character.move_right(5)
        elif self.hovering_right:
            self.character.move_left(5)
        else:
            self.character.stop()

        self.character.loop()

    # Draw decorative frame around tutorial surface
    def draw_frame(self):
        width, height = self.surface.get_size()

        self.surface.blit(self.corner_tl, (0, 0))
        self.surface.blit(self.corner_tl, (width - 44, 0))
        self.surface.blit(self.corner_tl, (0, height - 47))
        self.surface.blit(self.corner_tl, (width - 44, height - 47))

        top = pygame.transform.smoothscale(self.edge_top, (width - 2 * 43, 44))
        left = pygame.transform.smoothscale(
            self.edge_left, (44, height - 2 * 46))

        self.surface.blit(top, (44, 0))
        self.surface.blit(top, (44, height - 44))
        self.surface.blit(left, (0, 47))
        self.surface.blit(left, (width - 44, 47))

    # Draw tooltip text box near hovered button
    def draw_tooltip(self, text, pos):
        font = pygame.font.Font("data/Font/1.ttf", 8)
        tooltip = font.render(text, True, (255, 255, 255))
        bg = pygame.Surface(
            (tooltip.get_width() + 10, tooltip.get_height() + 6))
        bg.fill((200, 200, 200))
        self.surface.blit(bg, pos)
        self.surface.blit(tooltip, (pos[0] + 5, pos[1] + 3))

    def draw(self, window):
        if not self.active:
            return

        help_bg = pygame.transform.scale(
            self.tutorial_bg, self.surface.get_size())
        self.surface.blit(help_bg, (10, 0))

        for obj in self.objects:
            obj.draw(self.surface, self.offset_x)

        # Detect mouse hover over buttons
        mouse_pos = pygame.mouse.get_pos()
        local_mouse = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)
        hovering_right = self.right_rect.collidepoint(local_mouse)
        hovering_left = self.left_rect.collidepoint(local_mouse)
        hovering_down = self.down_rect.collidepoint(local_mouse)
        hovering_space = self.space_rect.collidepoint(local_mouse)
        hovering_exit = self.exit_rect.collidepoint(local_mouse)

        # Draw buttons with highlight and tooltip if hovered
        if hovering_right:
            bright_right = self.right_button.copy()
            bright_right.fill((80, 80, 80), special_flags=pygame.BLEND_RGB_ADD)
            self.surface.blit(bright_right, self.right_rect.topleft)
            self.draw_tooltip("Press LEFT to move left!",
                              (self.right_rect.x, self.right_rect.y + 55))
        else:
            self.surface.blit(self.right_button, self.right_rect.topleft)

        if hovering_down:
            bright_down = self.down_button.copy()
            bright_down.fill((80, 80, 80), special_flags=pygame.BLEND_RGB_ADD)
            self.surface.blit(bright_down, self.down_rect.topleft)
            self.draw_tooltip("Press DOWN to crouch",
                              (self.down_rect.x, self.down_rect.y + 55))
        else:
            self.surface.blit(self.down_button, self.down_rect.topleft)

        if hovering_left:
            bright_left = self.left_button.copy()
            bright_left.fill((80, 80, 80), special_flags=pygame.BLEND_RGB_ADD)
            self.surface.blit(bright_left, self.left_rect.topleft)
            self.draw_tooltip("Press RIGHT to move right!",
                              (self.left_rect.x, self.left_rect.y + 55))
        else:
            self.surface.blit(self.left_button, self.left_rect.topleft)

        if hovering_space:
            bright_space = self.space_button.copy()
            bright_space.fill((80, 80, 80), special_flags=pygame.BLEND_RGB_ADD)
            self.surface.blit(bright_space, self.space_rect.topleft)
            self.draw_tooltip("Press SPACE to jump!",
                              (self.space_rect.x, self.space_rect.y + 55))
        else:
            self.surface.blit(self.space_button, self.space_rect.topleft)

        # Update hover states
        self.hovering_right = self.right_rect.collidepoint(local_mouse)
        self.hovering_left = self.left_rect.collidepoint(local_mouse)
        self.hovering_space = self.space_rect.collidepoint(local_mouse)
        self.hovering_down = self.down_rect.collidepoint(local_mouse)

        # Draw tutorial character and frame
        self.character.draw(self.surface, self.offset_x)
        self.draw_frame()
        
        # Draw exit button with highlight if hovered
        if hovering_exit:
            bright_exit = self.exit_button.copy()
            bright_exit.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_ADD)
            self.surface.blit(bright_exit, self.exit_rect.topleft)
        else:
            self.surface.blit(self.exit_button, self.exit_rect.topleft)

        window.blit(self.surface, self.rect)


class ScoreItemDisplay:
    def __init__(self, image):
        self.image = image
        self.timer = 60
        self.rect = self.image.get_rect(center=(35, 50))

    def update(self):
        self.timer -= 1

    def draw(self, window):
        window.blit(self.image, self.rect)

    def is_alive(self):
        return self.timer > 0


class object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class HelpBlock(object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_help_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class Bee(object):
    ANIMATION_DELAY = 5
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "bee")
        self.health = 3
        self.alive = True
        self.bee = load_sprite_sheets("Traps", "Bee", width, height, direction=True)
        # self.hit = self.bee["Hit_" + self.direction]
        self.image = self.bee["Fly_right"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(x, y, width, height)
        self.animation_state = "Fly"
        self.animation_count = 0
        self.ANIMATION_DELAY = 5
        self.direction = "right"
        self.move_count = 0
        self.move_limit = 100
        self.vel = 2
        self.hit_timer = 0

        
    def loop(self):
        if not self.alive and self.animation_state != "Hit":
            return
        
        self.sprite_sheet_name = self.animation_state + "_" + self.direction
        sprites = self.bee[self.sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        if self.animation_state == "Hit" :
            self.hit_timer +=1
            if self.animation_count // self.ANIMATION_DELAY >= len(sprites):
                self.animation_count = 0
                self.hit_timer =0
                if self.health <= 0:
                    self.alive = False
                else:
                    self.animation_state = "Fly"

        if self.animation_state == "Fly":
            if self.direction == "right":
                self.rect.x -= self.vel
            else:
                self.rect.x += self.vel

        self.move_count += 1
        if self.move_count >= self.move_limit:
            self.move_count = 0
            self.direction = "left" if self.direction == "right" else "right"
        
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win, offset_x):
        if self.alive or self.animation_state != "Hit":
            win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Boar(object):
    ANIMATION_DELAY = 5
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "boar")
        self.health = 3
        self.alive = True
        self.boar = load_sprite_sheets("Traps", "Boar", width, height, direction=True)
        # self.hit = self.bee["Hit_" + self.direction]
        self.image = self.boar["Walk_right"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(x, y, width, height)
        self.animation_state = "Walk"
        self.animation_count = 0
        self.ANIMATION_DELAY = 5
        self.direction = "right"
        self.move_count = 0
        self.move_limit = 100
        self.vel = 2
        self.hit_timer = 0

        
    def loop(self):
        if not self.alive and self.animation_state != "Hit":
            return
        
        self.sprite_sheet_name = self.animation_state + "_" + self.direction
        sprites = self.boar[self.sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        if self.animation_state == "Hit" :
            self.hit_timer +=1
            if self.animation_count // self.ANIMATION_DELAY >= len(sprites):
                self.animation_count = 0
                self.hit_timer =0
                if self.health <= 0:
                    self.alive = False
                else:
                    self.animation_state = "Walk"

        if self.animation_state == "Walk":
            if self.direction == "right":
                self.rect.x -= self.vel
            else:
                self.rect.x += self.vel

        self.move_count += 1
        if self.move_count >= self.move_limit:
            self.move_count = 0
            self.direction = "left" if self.direction == "right" else "right"
        
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win, offset_x):
        if self.alive or self.animation_state != "Hit":
            win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Snail:
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        self.health = 3
        self.alive = True
        self.snail = load_sprite_sheets("Traps", "Snail", width, height, direction=True)
        self.image = self.snail["Walk_right"][0]
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(self.image)

        self.animation_state = "Walk"
        self.animation_count = 0
        self.direction = "right"
        self.move_count = 0
        self.ANIMATION_DELAY = 5
        self.move_limit = 100
        self.vel = 1
        self.hit_timer = 0
        self.ready_to_delete = False
        self.hit_count = 0

    def loop(self):
        if self.animation_state == "Dead":
            self.ready_to_delete = True
            return

        if self.animation_state == "Die":
            sprites = self.snail.get("Dead", [self.image])  
        else:
            sprite_key = self.animation_state + "_" + self.direction
            sprites = self.snail.get(sprite_key, [self.image])

        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        if self.animation_state == "Hit":
            self.hit_timer += 1
            if self.animation_count // self.ANIMATION_DELAY >= len(sprites):
                self.animation_count = 0
                self.hit_timer = 0
                if self.hit_count >= 4:
                    self.animation_state = "Die"
                    self.animation_count = 0
                    self.alive = False
                else:
                    self.animation_state = "Walk"


                    self.animation_state = "Walk"

        elif self.animation_state == "Die":
            sprites = self.snail.get("Dead", [self.image])
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
            self.image = sprites[sprite_index]
            self.animation_count += 1

            if self.animation_count // self.ANIMATION_DELAY >= len(sprites):
                self.animation_state = "Dead"
                self.ready_to_delete = True

        elif self.animation_state == "Walk" and self.alive:
            if self.direction == "right":
                self.rect.x -= self.vel
            else:
                self.rect.x += self.vel

            self.move_count += 1
            if self.move_count >= self.move_limit:
                self.move_count = 0
                self.direction = "left" if self.direction == "right" else "right"

        self.mask = pygame.mask.from_surface(self.image)
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Trap(object):
    def __init__(self, x, y, width, height, spike_type="1"):
        super().__init__(x, y, width, height, "spike")
        self.spike_type = spike_type
        spike_path = f"data/Traps/Spikes/{spike_type}.png"
        spike_img = pygame.image.load(spike_path).convert_alpha()
        self.image = pygame.transform.scale(spike_img, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win, offset_x=0):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

    def collision(self, player):
        return self.rect.colliderect(player.rect)

class Tree(object):
    def __init__(self, x, y, width, height, tree_type="1"):
        super().__init__(x, y, width, height, "tree")
        tree_path = f"data/decoration/trees/{tree_type}.png"
        tree_img = pygame.image.load(tree_path).convert_alpha()
        self.image = pygame.transform.scale(tree_img, (width, height))
        self.mask = pygame.mask.from_surface(self.image)

class Bush(object):
    def __init__(self, x, y, width, height, bush_type="1"):
        super().__init__(x, y, width, height, "bush")
        bush_path = f"data/decoration/bushes/{bush_type}.png"
        bush_img = pygame.image.load(bush_path).convert_alpha()
        self.image = pygame.transform.scale(bush_img, (width, height))
        self.mask = pygame.mask.from_surface(self.image)
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Plant(object):
    def __init__(self, x, y, width, height, plant_type="1"):
        super().__init__(x, y, width, height, "plant")
        plant_path = f"data/item/flowers/{plant_type}.png"
        plant_img = pygame.image.load(plant_path).convert_alpha()
        self.image = pygame.transform.scale(plant_img, (width, height))
        self.mask = pygame.mask.from_surface(self.image)
        self.stars = [StarParticle(self.rect.centerx, self.rect.top, self.rect.height) for _ in range(10)]
    
    def draw(self, win, offset_x=0):
        for star in self.stars:
            star.update()
            star.draw(win, offset_x)
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Key(object):
    def __init__(self, x, y, width, height, key_type = "1"):
        super().__init__(x, y, width, height, "key")
        key_path = f"data/item/key/{key_type}.png"
        key_img = pygame.image.load(key_path).convert_alpha()
        self.image = pygame.transform.scale(key_img, (width, height))
        self.mask = pygame.mask.from_surface(self.image)
        self.stars = [StarParticle(self.rect.centerx, self.rect.top, self.rect.height) for _ in range(10)]

    def draw(self, win, offset_x):
        for star in self.stars:
            star.update()
            star.draw(win, offset_x)
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Chest(object):
    def __init__(self, x, y, width, height, chest_type = "1"):
        super().__init__(x, y, width, height, "chest")
        chest_path = f"data/item/chest/{chest_type}.png"
        chest_img = pygame.image.load(chest_path).convert_alpha()
        self.image = pygame.transform.scale(chest_img, (width, height))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Broom(object):
    def __init__(self, x, y, width, height, broom_type = "1"):
        super().__init__(x, y, width, height, "chest")
        broom_path = f"data/item/broom/{broom_type}.png"
        broom_img = pygame.image.load(broom_path).convert_alpha()
        self.image = pygame.transform.scale(broom_img, (width, height))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class ChestDropEffect:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.start_y = y
        self.timer = 0
        self.active = True
        self.velocity = -10
        self.pause_duration = 5
        self.state = "rise"  
    def update(self):
        if not self.active:
            return

        self.timer += 1

        if self.state == "rise":
            self.y += self.velocity
            self.velocity += 0.3
            if self.velocity >= 0:
                self.state = "fall"
                self.velocity = 0.5

        elif self.state == "fall":
            self.y += self.velocity
            self.velocity += 0.4
            if self.y >= self.start_y:
                self.y = self.start_y
                self.state = "pause"
                self.timer = 0

        elif self.state == "pause":
            if self.timer > self.pause_duration:
                self.active = False


        # if self.active:
        #     self.y += self.velocity
        #     self.velocity += 0.1
        #     self.timer += 1
        #     if self.timer > 80:
        #         self.active = False

    def draw(self, surface):
        if self.active:
            surface.blit(self.image, (self.x - self.image.get_width()//2,
                                      self.y - self.image.get_height()//2))


class Potion(object):
    def __init__(self, x, y, width, height, potion_type="1"):
        super().__init__(x, y, width, height, "potions")
        potion_path = f"data/item/potions/{potion_type}.png"
        potion_img = pygame.image.load(potion_path).convert_alpha()
        self.image = pygame.transform.scale(potion_img, (width, height))
        self.mask = pygame.mask.from_surface(self.image)
        self.stars = [StarParticle(self.rect.centerx, self.rect.top, self.rect.height) for _ in range(10)]
    
    def draw(self, win, offset_x=0):
        for star in self.stars:
            star.update()
            star.draw(win, offset_x)
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class StarParticle:
    def __init__(self, x, y, height):
        self.orginal_x = x
        self.orginal_y = y
        self.height = height
        self.reset()
        # self.x = x + random.randint(-20, 20)
        # self.y = y + random.randint(0, height // 2)
        # self.radius = random.randint(1, 2)
        # self.alpha = random.randint(220, 255)
        # self.fade_speed = random.uniform(0.5, 1.5)

    def reset(self):
        self.x = self.orginal_x + random.randint(-20, 20)
        self.y = self.orginal_y + random.randint(0, self.height // 2)
        self.radius = random.randint(1, 2)
        self.alpha = random.randint(200, 255)
        self.fade_speed = random.uniform(0.5, 1.5)

    def update(self):
        self.y -= 0.5
        self.alpha -= self.fade_speed
        if self.alpha <= 0:
            self.reset()
            # self.alpha = random.randint(100, 200)
            # self.x += random.randint(-5, 5)
            # self.y += random.randint(-5, 5)
    

    def draw(self, win, offset_x=0):
        star_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(star_surface, (255, 255, 200, int(self.alpha)), (self.radius, self.radius), self.radius)
        win.blit(star_surface, (self.x - offset_x, self.y))

class PlusEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alpha = 255
        self.lifetime = 30
        self.font = pygame.font.SysFont("arial", 24, bold=True)

    def update(self):
        self.y -= 1
        self.alpha -= 8
        self.lifetime -= 1

    def draw(self, win, offset_x=0):
        if self.lifetime > 0:
            text = self.font.render("+", True, (0, 255, 0))
            text.set_alpha(self.alpha)
            win.blit(text, (self.x - offset_x, self.y))

class FlashEffect:
    def __init__(self, image, hold_last_frame=False):
        self.image = image
        self.timer = 0
        self.active = False
        self.hold_last_frame = hold_last_frame
    
    def trigger(self):
        self.timer = 0
        self.active = True
    
    def update(self):
        if self.active:
            self.timer += 1
            if self.hold_last_frame:
                if self.timer > (len(self.image) * 5 + 70):
                    self.active = False
            else:
                if self.timer > (len(self.image) * 5):
                    self.active = False


    def draw(self, surface):
        if not self.active :
            return
        
        frame_index = (self.timer // 3)

        if frame_index >= len(self.image):
            frame_index = len(self.image) - 1
            # self.active = False
            # return

        key_image =self.image[frame_index]

        flash_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        center = (surface.get_width()//2, surface.get_height()//2)

        pygame.draw.circle(flash_surface, (255, 252, 255, 180), center, 200)

        for i in range(8):
            angle = i * (360 // 8)
            length = 300
            x = center[0] + int(length * math.cos(math.radians(angle)))
            y = center[1] + int(length * math.sin(math.radians(angle)))
            pygame.draw.line(flash_surface, (255, 255, 255, 80), center, (x, y), 4)

        rotation_angle = self.timer * 1  # سرعت چرخش
        rotated_flash = pygame.transform.rotate(flash_surface, rotation_angle)

        new_rect = rotated_flash.get_rect(center=center)
        surface.blit(rotated_flash, new_rect.topleft)

        surface.blit(flash_surface, (0, 0))
        surface.blit(key_image, (center[0] - key_image.get_width()//2,
                                  center[1] - key_image.get_height()//2))

class collectible(object):
    ANIMATION_DELAY = 4

    def __init__(self, x, y, width, height, item_type="coin", animation_name="1"):
        super().__init__(x, y, width, height, item_type)
        self.sprites = load_sprite_sheets("Item", item_type, width, height)
        self.image = self.sprites[animation_name][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = animation_name

    def loop(self):
        sprites = self.sprites[self.animation_name]
        sprites_index = (self.animation_count //
                         self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprites_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


def get_background(name):
    image = pygame.image.load(join("data", "background", name))
    image = pygame.transform.smoothscale(image, (1900, 970))
    _, _, width, heigth = image.get_rect()
    tiles = []
    for i in range(WIDTH // width + 1):
        for j in range(HIGHT // heigth + 1):
            pos = (i * width, j * heigth)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_img, player, objects, offset_x, setting_img, setting_open,setting_rotated, setting_icons,
        help_tutorial, bees, bushes, spikes, snails, boars, key_flash, chest_flash, chest_drops, broom_flying, broom_x, broom_y, broom2_img, game_state):
    for tile in background:
        window.blit(bg_img, tile)

    for bush in bushes:
            bush.draw(window, offset_x)

    for obj in objects:
        obj.draw(window, offset_x)

    for b in bees:
        b.draw(window, offset_x)

    for b in boars:
        b.draw(window, offset_x)
    
    for s in snails:
        s.draw(window, offset_x)

    for spike in spikes:
        spike.draw(window, offset_x)

    if broom_flying:
        broom_x += 5  
        window.blit(broom2_img, (broom_x - offset_x, broom_y))
    
    player.spits.update()
    check_spit_collision(player.spits, bees , player, snails, boars)
    for spit in player.spits:
        window.blit(spit.image, (spit.rect.x - offset_x, spit.rect.y))

    if player.visible:
        player.draw(window, offset_x)
# کشیدن امتیاز
    window.blit(score_palen, (5, -50))
    window.blit(frog_icon, (75, 100))
    window.blit(key_img, (250, 30))
    key_flash.update()
    key_flash.draw(window)
    chest_flash.update()
    chest_flash.draw(window)
    for drop in chest_drops:
            drop.update()
            drop.draw(window)

    chest_drops = [d for d in chest_drops if d.active]

    for icon in setting_icons:
        icon.draw(window)

    if setting_open:
        setting_rotated = pygame.transform.rotozoom(setting_img, 30, 1)
        rotated_rect = setting_rotated.get_rect(center=setting_rect.center)
        window.blit(setting_rotated, rotated_rect)
    else:
        window.blit(setting_img, setting_rect)

    key_font = pygame.font.SysFont("Verdana", 23, bold=True)
    key_text = key_font.render(f"x{player.key_count}", True, (0, 0, 0))
    window.blit(key_text, (300, 35))

# قسمت score
    font = pygame.font.SysFont("Verdana", 18)
    score_text = font.render(f"score:{player.score}", True, (255, 255, 0))
    score_rect = score_text.get_rect(center=(125, 50))

    window.blit(score_text, score_rect)

    for i in range(player.health):
        window.blit(heart_img, (10 + i * 35, 150))
# نمایش دریافتی ها
    for display in player.score_item_display[:]:
        display.update()
        display.draw(window)
        if not display.is_alive():
            player.score_item_display.remove(display)
    help_tutorial.draw(window)
    pygame.display.update()


def game_over_screen(window):
    font = pygame.font.SysFont("comicsans", 60)
    text = font.render("GAME OVER!", True, (0, 0, 0))

    overlay = pygame.Surface((WIDTH, HIGHT))
    pygame.mixer.music.stop()
    pygame.mixer.music.load("data/music/sounds/gameover.mp3")
    pygame.mixer.music.play()
    overlay.set_alpha(180)
    overlay.fill((255, 255, 255))
    window.blit(overlay, (0, 0))

    window.blit(text, (WIDTH // 2 - text.get_width() // 2, HIGHT // 2 - 100))

    restart_X = WIDTH // 2 - 50
    restart_Y = HIGHT // 2 + 50
    window.blit(restart_img, (restart_X, restart_Y))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if restart_X <= mouse[0] <= restart_X + 100 and restart_Y <= mouse[1] <= restart_Y + 100:
                    return "menu"


def win_game(window):
    pygame.mixer.music.stop()
    pygame.mixer.music.load("data/music/sounds/win.mp3")
    pygame.mixer.music.play()

    overlay = pygame.Surface((WIDTH, HIGHT))
    overlay.fill((255, 255, 255))
    overlay.set_alpha(200)
    window.blit(overlay, (0, 0))

    font = pygame.font.SysFont("comicsans", 60)
    text = font.render("YOU WON!", True, (0, 0, 0))
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, HIGHT // 2 - 100))

    next_rect = next_img.get_rect(center=(WIDTH // 2 - 100, HIGHT // 2 + 50))
    menu_rect = menu_img.get_rect(center=(WIDTH // 2 + 100, HIGHT // 2 + 50))

    window.blit(next_img, next_rect.topleft)
    window.blit(menu_img, menu_rect.topleft)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_rect.collidepoint(event.pos):
                    return "monster"
                if menu_rect.collidepoint(event.pos):
                    return "menu"


def death_check(player):
    if player is None:
        return
    if not player.dead and player.rect.y > HIGHT + 100:
        if player.health > 0:
            player.health -= 1
            player.rect.x -= 100
            player.rect.y = 100

            player.fall = True
            player.fall_timer = 0
            player.fall_count = 1
            player.jump_count = 0
            player.x_vel = 0
            player.Y_vel = 0
            player.animation_count = 0
        else:
            player.dead = True
            player.exploding = True
            player.exploding_end = False
            player.animation_count = 0
            player.x_vel = 0
            player.Y_vel = 0


def handel_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.Y_vel = 0
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects, bees, spikes, snails, boars):
    keys = pygame.key.get_pressed()
    coins_to_remove = []
    for obj in objects:
        if obj.name == "coin" and pygame.sprite.collide_mask(player, obj):
            coins_to_remove.append(obj)
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    player.x_vel = 0
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)

    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    if keys[pygame.K_DOWN] and not collide_right and not collide_left:
        player.dodge = True

    vertical_collide = handel_vertical_collision(player, objects, player.Y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()
    for bee in bees:
        if pygame.sprite.collide_mask(player, bee):
            player.make_hit()
    for boar in boars:
        if pygame.sprite.collide_mask(player, boar):
            player.make_hit()
    for sanil in snails:
        if pygame.sprite.collide_mask(player, sanil):
            player.make_hit()
    for spike in spikes:
        if spike.collision(player):
            player.make_hit()

def calculate_offset(player, screen_width):
    return max(0, player.rect.x - (screen_width // 2 - player.rect.width // 2))


def start_game():
    while True:
        menu = Menu(window)
        result = menu.run_m()

        if result == "start":
            player = Player(x=100, y=100, width=50, height=50, score_display_list=[])
            outcome = main(window, player)

            if outcome == "menu":
                continue  # برگشت به منو
        elif result == "shop":
            player = Player(x=100, y=500, width=50, height=60, score_display_list=[])
            run_shop_screen(window, player)
        
        elif result == "guide":
            result = run_guide_screen(window)
            if result == "menu":
                continue

        elif result == "exit":
            pygame.quit()
            break

def main(window, player):
    clock = pygame.time.Clock()
    background, bg_img = get_background("Pink.png")
    pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
    play_next_track()
    game_state = "playing"
    flying_timer = 0
    help_tutorial = Tutorial((800, 500), (WIDTH // 2, HIGHT // 2))
    setting_open = False
    setting_rotated = setting_img
    sound_on = True
    block_size = 96
    bush_size = 150
    bush_height = 100
    offset_x = calculate_offset(player, WIDTH)

    key_icon = load_sprite_sheets("decoration", "keys", 32, 32)["1"]
    key_flash = FlashEffect(key_icon, hold_last_frame=False)
    chest_icon = load_sprite_sheets("decoration", "chest", 48, 32)["1"]
    chest_flash = FlashEffect(chest_icon, hold_last_frame=True)
    chest_drops = []
    broom2_img = pygame.image.load("data/item/broom/2.png").convert_alpha()
    broom2_img = pygame.transform.scale(broom2_img, (200, 100))
    broom_flying = False
    broom_x = 0
    broom_y = 0

    fire = Fire(100, HIGHT - block_size - 64, 16, 32)
    fire.on()
    fires = get_fires(block_size)

    floor = [Block(i * block_size, HIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]

    setting_icons = [
        SettingIcon("help",  "data/menu/botton/icon/help.png", (40, 60), 10),
        SettingIcon("shop", "data/menu/botton/icon/shop.png", (32, 32), 70),
        SettingIcon("home", "data/menu/botton/icon/home.png", (29, 29), 114),
        SettingIcon("volume", "data/menu/botton/icon/volume.png", (30, 30), 160)
        
    ]
    for icons in setting_icons:
        icons.visible = setting_open
        icons.update(setting_rect)

    bees = [
        Bee(500, HIGHT - block_size - 50, 32, 32),
        Bee(1500, HIGHT - block_size * 1 - 150, 32, 32),
        Bee(4000, HIGHT - block_size - 50, 32, 32),
        Bee(4150, HIGHT - block_size * 2 - 50, 32, 32),
        Bee(8250, HIGHT - block_size * 2 - 50, 32, 32),
        Bee(8600, HIGHT - block_size * 3 - 50, 32, 32),
        Bee(8800, HIGHT - block_size * 2 - 50, 32, 32)
            ]
    
    boars = [Boar(2690, HIGHT - block_size - 49, 39, 26),
             Boar(9700, HIGHT - block_size * 3 - 49, 39, 26),
             ]
    
    snails = [Snail(4900, HIGHT - block_size - 49, 39, 26),
              Snail(7550, HIGHT - block_size - 49, 39, 26)
              ]
    
    spikes = (make_spike(1850, HIGHT - block_size * 6 - 15, 4, 20, 20, spike_type="1", space= 20)+
              make_spike(2600, HIGHT - block_size * 3 - 5, 5, 30, 50, spike_type="2", space= 30)+
              make_spike(4100, HIGHT - block_size * 3 - 8, 1, 50, 50, spike_type="9", space= 20)+
              make_spike(4600, HIGHT - block_size * 6 - 30, 2, 30, 30, spike_type="3", space= 30)+
              make_spike(5973, HIGHT - block_size * 4 - 15, 3, 20, 20, spike_type="1", space= 20)+
              make_spike(6555, HIGHT - block_size * 2 - 15, 4, 20, 20, spike_type="1", space= 20)+
              make_spike(6900, HIGHT - block_size * 1 - 65, 3, 30, 70, spike_type="5", space= 30)+
              make_spike(8600, HIGHT - block_size * 3 - 8, 1, 50, 50, spike_type="9", space= 20)
              )

    coins = (make_collectibale(500, HIGHT - block_size * 4 - 50, 1, 16, 16, item_type="gold")+
             make_collectibale(800, HIGHT - block_size * 3 - 40, 1, 16, 16, item_type="gold")+
             make_collectibale(1000, HIGHT - block_size * 1 - 40, 1, 16, 16, item_type="gold")+
             make_collectibale(1550, HIGHT - block_size * 6 - 60, 1, 16, 16, item_type="gold")+
             make_collectibale(1550, HIGHT - block_size * 1 - 50, 1, 16, 16, item_type="gold")+
             make_collectibale(1900, HIGHT - block_size * 3 - 50, 4, 16, 16, item_type="gold")+
             make_collectibale(2400, HIGHT - block_size * 2 - 50, 1, 16, 16, item_type="gold")+
             make_collectibale(2580, HIGHT - block_size * 2 - 50, 1, 9, 15, item_type="gem2")+
             make_collectibale(2630, HIGHT - block_size * 4 - 40, 1, 10, 10, item_type="gem3")+
             make_collectibale(3600, HIGHT - block_size * 2 - 50, 5, 16, 16, item_type="gold")+
             make_collectibale(4100, HIGHT - block_size * 4 - 40, 3, 16, 16, item_type="gold")+
             make_collectibale(4600, HIGHT - block_size * 6 - 60, 1, 16, 16, item_type="gold")+
             make_collectibale(4950, HIGHT - block_size * 1 - 60, 5, 16, 16, item_type="dimon3")+
             make_collectibale(5532, HIGHT - block_size * 4 - 60, 1, 16, 16, item_type="gold")+
             make_collectibale(6182, HIGHT - block_size * 2 - 60, 1, 16, 16, item_type="gold")+
             make_collectibale(6382, HIGHT - block_size * 4 - 60, 1, 16, 16, item_type="dimon2")+
             make_collectibale(7800, HIGHT - block_size * 3 - 60, 5, 16, 16, item_type="gold")+
             make_collectibale(10300, HIGHT - block_size * 3 - 60, 6, 16, 16, item_type="gold")+
             make_collectibale(9800, HIGHT - block_size * 5 - 60, 3, 10, 10, item_type="gem3")
             )
    
    trees = [Tree(330, HIGHT - block_size * 4 - 400, 420, 500, tree_type="13"),
             Tree(800, HIGHT - block_size * 1 - 20, 40, 30, tree_type="10"),
             Tree(1400, HIGHT - block_size * 1 - 520, 450, 650, tree_type="13"),
             Tree(9850, HIGHT - block_size * 3 - 350, 350, 450, tree_type="13"),
             ]
    
    bushes = (make_bushs(1350, HIGHT - block_size * 1 - 78, 22, bush_size, bush_height, bush_type="2", space=70)+
              make_bushs(3500, HIGHT - block_size * 4 - 400, 1, bush_size + 200, bush_height +350, bush_type="6", space=70)+
              make_bushs(4760, HIGHT - block_size * 1 - 78, 9, bush_size, bush_height, bush_type="2", space=70)+
              make_bushs(5325, HIGHT - block_size * 1 - 78, 1, bush_size, bush_height, bush_type="2", space=70)+
              make_bushs(6930, HIGHT - block_size * 1 - 78, 12, bush_size, bush_height, bush_type="2", space=70)+
              make_bushs(6900, HIGHT - block_size * 1 - 78, 1, bush_size, bush_height, bush_type="2", space=70)+
              make_bushs(7710, HIGHT - block_size * 1 - 78, 1, bush_size, bush_height, bush_type="2", space=70)+
              make_bushs(8500, HIGHT - block_size * 2 - 400, 1, bush_size + 200, bush_height +350, bush_type="6", space=70)+
              make_bushs(7996, HIGHT - block_size * 2 - 36, 21, 49, 39, bush_type="10", space=46)+
              make_bushs(9950, HIGHT - block_size * 3 - 78, 12, bush_size, bush_height, bush_type="2", space=70)+
              make_bushs(9400, HIGHT - block_size * 3 - 18, 44, 29, 18, bush_type="11", space=33)
              )
    
    plants = [
        Plant(200, HIGHT - block_size * 1 - 40, 50, 50, plant_type="1"),
        Plant(430, HIGHT - block_size * 4 - 40, 50, 50, plant_type="1"),
        Plant(1690, HIGHT - block_size * 6 - 13, 30, 13, plant_type="5"),
        Plant(1700, HIGHT - block_size * 6 - 30, 30, 30, plant_type="5"),
        Plant(1710, HIGHT - block_size * 6 - 20, 30, 20, plant_type="5"),
        Plant(2400, HIGHT - block_size * 4 - 30, 50, 35, plant_type="8"),
        Plant(2030, HIGHT - block_size * 1 - 30, 50, 35, plant_type="9"),
        Plant(2100, HIGHT - block_size * 1 - 30, 50, 35, plant_type="9"),
        Plant(2170, HIGHT - block_size * 1 - 30, 50, 35, plant_type="9"),
        Plant(4350, HIGHT - block_size * 1 - 30, 50, 35, plant_type="11"),
        Plant(4400, HIGHT - block_size * 1 - 30, 50, 35, plant_type="11"),
        Plant(4450, HIGHT - block_size * 1 - 30, 50, 35, plant_type="11"),
        Plant(4500, HIGHT - block_size * 1 - 30, 50, 35, plant_type="11"),
        Plant(4550, HIGHT - block_size * 1 - 30, 50, 35, plant_type="11"),
        Plant(4600, HIGHT - block_size * 1 - 30, 50, 35, plant_type="11"),
        Plant(4650, HIGHT - block_size * 1 - 30, 50, 35, plant_type="11"),
        Plant(6772, HIGHT - block_size * 4 - 13, 30, 13, plant_type="5"),
        Plant(6782, HIGHT - block_size * 4 - 30, 30, 30, plant_type="5"),
        Plant(6792, HIGHT - block_size * 4 - 20, 30, 20, plant_type="5"),
        Plant(7552, HIGHT - block_size * 3 - 30, 45, 32, plant_type="12"),
              ]
    
    keys = [Key(1700, HIGHT - block_size * 1 - 90, 30, 30, key_type="1"),
            Key(7600, HIGHT - block_size * 1 - 50, 30, 30, key_type="1"),
            ]

    chests = [Chest(5000, HIGHT - block_size * 3 - 40, 60, 50, chest_type="1"),
              Chest(9800, HIGHT - block_size * 3 - 40, 60, 50, chest_type="1"),
              ]
    broom = Broom(11000, HIGHT - block_size * 3 - 40, 200, 100, broom_type="1")
    
    potions = [Potion(4100, HIGHT - block_size * 1 - 43, 50, 50, potion_type="11"),
               Potion(8900, HIGHT - block_size * 2 - 43, 50, 50, potion_type="11"),
               ]   
    
    score_item_display = []

    object = [*plants,*potions,*keys,
              *floor, Block(0, HIGHT - block_size * 2, block_size),
              *make_platform(300, HIGHT - block_size * 4, 3, block_size),
              *make_platform(800, HIGHT - block_size * 3, 4, block_size),
              *make_platform(-300, HIGHT - block_size * 3, 2, block_size),
              *make_platform(1300, HIGHT - block_size * 4, 1, block_size),
              *make_platform(1500, HIGHT - block_size * 6, 5, block_size),
              *make_platform(2300, HIGHT - block_size * 4, 5, block_size),
              *make_platform(3050, HIGHT - block_size * 2, 3, block_size),
              *make_platform(3550, HIGHT - block_size * 4, 7, block_size),
              *make_platform(3550, HIGHT - block_size * 1, 20, block_size),
              *make_platform(4500, HIGHT - block_size * 6, 2, block_size),
              *make_platform(4800, HIGHT - block_size * 3, 5, block_size),
              *make_platform(5500, HIGHT - block_size * 4, 1, block_size),
              *make_platform(5750, HIGHT - block_size * 2, 1, block_size),
              *make_platform(5950, HIGHT - block_size * 4, 1, block_size),
              *make_platform(6150, HIGHT - block_size * 2, 1, block_size),
              *make_platform(6350, HIGHT - block_size * 4, 1, block_size),
              *make_platform(6550, HIGHT - block_size * 2, 1, block_size),
              *make_platform(6750, HIGHT - block_size * 4, 1, block_size),
              *make_platform(6900, HIGHT - block_size * 1, 10, block_size),
              *make_platform(7400, HIGHT - block_size * 3, 3, block_size),
              *make_platform(8000, HIGHT - block_size * 2, 10, block_size),
              *make_platform(9400, HIGHT - block_size * 3, 15, block_size),
              *make_platform(9750, HIGHT - block_size * 5, 2, block_size),
              *chests,
              *fires,
              fire,
              *trees,
              *coins,
              *spikes,
              broom]

    scroll_area_width = 200
    run = True
    while run:
        clock.tick(FPS)
        clicked_help = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.USEREVENT + 1:
                play_next_track()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_m:
                    player.attack = True
                    player.animation_count = 0
                    player.shoot_spit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.dodge = False
                if event.key == pygame.K_m:
                    player.attack = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if setting_rect.collidepoint(mouse):
                    setting_open = not setting_open

                    for icon in setting_icons:
                        if setting_open:
                            icon.show()
                        else:
                            icon.hide()
                        icon.update(setting_rect)

                for icon in setting_icons:
                    if icon.clicked(mouse):
                        if icon.name == "help":
                            help_tutorial.start()
                            clicked_help = True

                        if icon.name == "shop":
                           run_shop_screen(window, player)
                           pygame.mixer.music.stop()
                           play_next_track()
                        
                        if icon.name == "home":
                           pygame.mixer.music.stop()
                           play_next_track()
                           return "menu"

                        if icon.name == "volume":
                            if sound_on:
                                icon.image = pygame.image.load(
                                    "data/menu/botton/icon/mute.png").convert_alpha()
                                icon.image = pygame.transform.smoothscale(
                                    icon.image, (30, 30))
                                pygame.mixer.music.set_volume(0)
                                sound_on = False
                            else:
                                icon.image = pygame.image.load(
                                    "data/menu/botton/icon/volume.png").convert_alpha()
                                icon.image = pygame.transform.smoothscale(
                                    icon.image, (30, 30))
                                pygame.mixer.music.set_volume(1)
                                sound_on = True

                if help_tutorial.active and not clicked_help:
                    local_pos = (
                        event.pos[0] - help_tutorial.rect.left, event.pos[1] - help_tutorial.rect.top)
                    if help_tutorial.exit_rect.collidepoint(local_pos):

                        help_tutorial.active = False

        if game_state == "playing":
            player.loop(FPS)
            fire.loop()
            for f in fires:
                f.loop()

            for c in coins:
                c.loop()

            for b in bees:
                b.loop()

            for bo in boars:
                bo.loop()

            for s in snails:
                s.loop()

            snails = [s for s in snails if not s.ready_to_delete]

            help_tutorial.update()
            help_tutorial.draw(window)
            if player.rect.colliderect(broom.rect):
                broom_flying = True
                broom_x = broom.rect.x
                broom_y = broom.rect.y
                player.visible = False
                flying_timer = pygame.time.get_ticks()
                game_state = "flying"

            death_check(player)
            if player and player.dead and player.exploding and player.exploding_end:
                game_state = "lost"

            if game_state == "lost":
                result = game_over_screen(window)
                if result == "menu":
                    return "menu"

            elif game_state == "won":
                result = win_game(window)
                if result == "monster":
                    pygame.mixer.music.stop()
                    from pyth import monster_hunting  
                    monster_hunting()
                    return "menu"

            if player:
                player.collect_item(object, key_flash, chest_flash, chest_drops)

            
            handle_move(player, object, bees, spikes, snails, boars)

        if game_state == "flying":
            broom_flying = True
            if pygame.time.get_ticks() - flying_timer > 2000:
                game_state = "won"

        if game_state == "won":
            result = win_game(window)
            pygame.mixer.music.stop()

            if result == "monster":
                from pyth import monster_hunting
                monster_hunting()
                return "menu"

            elif result == "menu":
                return "menu"

        draw(window, background, bg_img, player, object, offset_x, setting_img,setting_open, setting_rotated,
              setting_icons, help_tutorial, bees, bushes, spikes, snails, boars, key_flash, chest_flash, chest_drops, broom_flying, broom_x, broom_y, broom2_img, game_state)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    start_game()
