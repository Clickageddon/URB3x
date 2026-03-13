import pygame
import sys

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("nullscapes.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# FENETRE
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("URB-3x")
clock = pygame.time.Clock()

TILE_SIZE = 40

# -------------------
# CHARGEMENT IMAGES
# -------------------

background = pygame.image.load("background3.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

player_texture = pygame.image.load("potato.png")
player_texture = pygame.transform.scale(player_texture, (30, 40))

textures = {
    "1": pygame.image.load("ground.png"),
    "2": pygame.image.load("vine.png"),
    "3": pygame.image.load("test_bloc.png"),
    "L": pygame.image.load("ladder.webp")
}

for key in textures:
    textures[key] = pygame.transform.scale(textures[key], (TILE_SIZE, TILE_SIZE))


# -------------------
# MAP
# -------------------
# 0 = vide
# 1 = bloc
# 2 = ronces (tue le joueur)
# 3 = bloc test -> aucune collision
# L = échelle
# P = spawn joueur

level_map = [
'222222222222222222222222222222222222222222222222222222222222222222222222',
'200000000000000000000000000000000000000000000000000000000000000000000002',
'200000000000000000000000000000000000000000000000000000000000000000000002',
'200000000000000000000000000000000000000000000000000000000000000000000002',
'200000000000000000000000000000000000000000000000000000000000000000000002',
'200000000000000000000L00000000000000000000000000000000000000000000000002',
'201010101000001010101L10101010101010101010101010101010101010101010101002',
'200000000000000000000L00000000000000000000000000000000000000000000000002',
'2000P0000001000000000L00000000000000000000000000000000000000000000000002',
'201111111111111111111111111111111111111111111111111111111111111111111102',
'200000000000000000000000000000000000000000000000000000000000000000000002',
'222222222222222222222222222222222222222222222222222222222222222222222222'
]

tiles = []
deadly_tiles = []
no_collision_tiles = []
ladder_tiles = []

spawn_x = 100
spawn_y = 100


# LECTURE MAP
for y, row in enumerate(level_map):
    for x, tile in enumerate(row):

        world_x = x * TILE_SIZE
        world_y = y * TILE_SIZE

        if tile == "1":
            tiles.append(pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE))

        if tile == "2":
            deadly_tiles.append(pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE))
        
        if tile == "3":
            no_collision_tiles.append(pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE))

        if tile == "L":
            ladder_tiles.append(pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE))

        if tile == "P":
            spawn_x = world_x
            spawn_y = world_y


player = pygame.Rect(spawn_x, spawn_y, 30, 40)

vel_y = 0
speed = 3.75
jump_power = -13
gravity = 0.7
on_ground = False

camera_x = 0
camera_y = 0


def respawn():
    global vel_y
    player.x = spawn_x
    player.y = spawn_y
    vel_y = 0


# -------------------
# GAME LOOP
# -------------------

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if keys[pygame.K_q]:
        dx -= speed
    if keys[pygame.K_d]:
        dx += speed

    # DETECTION ECHELLE
    on_ladder = False
    for tile in ladder_tiles:
        if player.colliderect(tile):
            on_ladder = True

    # MOUVEMENT ECHELLE
    if on_ladder:
        vel_y = 0

        if keys[pygame.K_z]:
            player.y -= 4

        if keys[pygame.K_s]:
            player.y += 4

    # SAUT
    if keys[pygame.K_SPACE] and on_ground and not on_ladder:
        vel_y = jump_power

    # GRAVITE
    if not on_ladder:
        vel_y += gravity
        dy += vel_y

    # COLLISION HORIZONTALE
    player.x += dx

    for tile in tiles:
        if player.colliderect(tile):

            if dx > 0:
                player.right = tile.left

            if dx < 0:
                player.left = tile.right

    # COLLISION VERTICALE
    player.y += dy
    on_ground = False

    for tile in tiles:

        if player.colliderect(tile):

            if vel_y > 0:
                player.bottom = tile.top
                vel_y = 0
                on_ground = True

            elif vel_y < 0:
                player.top = tile.bottom
                vel_y = 0

    # TILE MORTELLE
    for tile in deadly_tiles:
        if player.colliderect(tile):
            respawn()

    # CAMERA
    camera_x = player.centerx - WIDTH // 2
    camera_y = player.centery - HEIGHT // 2

    # -------------------
    # DESSIN
    # -------------------

    screen.blit(background, (0, 0))

    # tiles normales
    for tile in tiles:
        screen.blit(
            textures["1"],
            (tile.x - camera_x, tile.y - camera_y)
        )

    # tiles mortelles
    for tile in deadly_tiles:
        screen.blit(
            textures["2"],
            (tile.x - camera_x, tile.y - camera_y)
        )

    # echelles
    for tile in ladder_tiles:
        screen.blit(
            textures["L"],
            (tile.x - camera_x, tile.y - camera_y)
        )

    # joueur
    screen.blit(
        player_texture,
        (player.x - camera_x, player.y - camera_y)
    )

    # tiles sans collision ( devant le joueur )
    for tile in no_collision_tiles:
        screen.blit(
            textures["3"],
            (tile.x - camera_x, tile.y - camera_y)
        )

    pygame.display.update()
    clock.tick(60)
