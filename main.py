import random
import pygame
from sys import exit
from random import randint, choice

  # the sprite class contains a surface and a rectangle; it can be drawn and updated very easily

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0  # used to pick different surfaces
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1  # speed of switching between animations
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]
    # play walking animation if player is on the floor
    # play jumping animation when player is off the floor
def display_score():
    current_time = int((pygame.time.get_ticks() / 1000) - start_time)  # time in ms
    score_surf = test_font.render(f'{current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:  # evaluates if the list is empty or not
        for obstacle_rectangle in obstacle_list:
            obstacle_rectangle.x -= 5

            if obstacle_rectangle.bottom == 300: screen.blit(snail_surf, obstacle_rectangle)
            else: screen.blit(fly_surf, obstacle_rectangle)


        obstacle_list = [obstacle for obstacle in obstacle_list if
                         obstacle.x > -100]  # if the obstacle goes off-screen we kill it after a certain distance
        return obstacle_list
    else: return []


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacles_group, False):
        obstacles_group.empty()
        return False
    else:
        return True

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

#Game initialisation
pygame.init()
screen = pygame.display.set_mode((800, 400))  # width,height #origin point is top left not bottom left
pygame.display.set_caption('My First Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # font type, font size
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play()
bg_music.set_volume(0.2)
bg_music.play(loops = -1)


#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles_group = pygame.sprite.Group()


sky_surf = pygame.image.load('graphics/Sky.png').convert_alpha()  # convert alpha is used to remove the alpha values (game should run faster)
ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()

# score_surface = test_font.render('Score:', False, (64, 64, 64)).convert_alpha()  # text , Anti Aliasing , color
# score_rectangle = score_surface.get_rect(center=(350, 20))

# obstacle surface

snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

# player surface
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0  # used to pick different surfaces
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))  # draw a rectangle around the surface of the player
player_gravity = 0

# intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()  # importing the image
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)  # we update the image with this command , returning a new surface
player_stand_rect = player_stand.get_rect(center=(400, 200))  # creating the rectangle

title_surf = test_font.render('Title: The Retard Runner', False, (64, 64, 64)).convert_alpha()
title_rect = title_surf.get_rect(midtop=(400, 10))

instructions_surf = test_font.render('Press "SpaceBar" to start the game', False, (64, 64, 64))
instructions_rect = instructions_surf.get_rect(midtop=(400, 300))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)  # set the time at which the event happens

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 300)

while True:
    for event in pygame.event.get():  # for any type of event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if player_rect.bottom == 300 and event.key == pygame.K_SPACE:
                    player_gravity = -20

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                obstacles_group.add(Obstacles(choice(['fly','snail','snail','snail'])))  # choice method will pick one of these 4 items
                # if randint(0, 1):
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1200), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]



    if game_active:
        screen.blit(sky_surf, (0, 0))  # blit = block image transfer (one surface on another surface) ; (surface we want to place, position)
        screen.blit(ground_surf, (0, 300))
        # pygame.draw.rect(screen, '#c0e8ec', score_rectangle)
        # pygame.draw.rect(screen, '#c0e8ec', score_rectangle, 10)
        # screen.blit(score_surface, score_rectangle)
        score = display_score()

        # snail_rectangle.x -= 4
        # if snail_rectangle.right < 0:
        #     snail_rectangle.left = 800
        # screen.blit(snail_surface, snail_rectangle)

        # Player
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf, player_rect)

        player.draw(screen)
        player.update()

        obstacles_group.draw(screen)
        obstacles_group.update()

        # Obstacle Movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collision_sprite()
        # game_active = collisions(player_rect, obstacle_rect_list)
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}', False, (64, 64, 64))
        score_message_rectangle = score_message.get_rect(center=(400, 300))
        screen.blit(title_surf, title_rect)

        if score == 0:
            screen.blit(instructions_surf, instructions_rect)
        else:
            screen.blit(score_message, score_message_rectangle)

    pygame.display.update()  # updates the display surface
    clock.tick(60)  # this while true loop will not run faster than 60 times per second
