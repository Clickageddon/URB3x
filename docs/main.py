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
    "3": pygame.image.load("secret_zone_bloc.png"),
    "L": pygame.image.load("ladder.webp")
}

for key in textures:
    textures[key] = pygame.transform.scale(textures[key], (TILE_SIZE, TILE_SIZE))


# -------------------
# MAP
# -------------------

level_map = [
'00000000000000000000000000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'00000000000000000000L00000000000000000',
'01111111111111111111L11111111111111110',
'00000000000000000001L10000000000000000',
'00000000000000000001L10000000000000000',
'00000000000000000001L10000000000000000',
'01111111111111110001L10000000000000000',
'01000000000000010001L10000000000000000',
'01000000000000010001L10000000000000000',
'01000000000000010001L10000000000000000',
'01131111111111111111L11111100000000000',
'010L0000000000000000L00000110000000000',
'010L0000000000000000L00000011000000000',
'010L0000000000000000L00000001000000000',
'011L1111111111111111111111111111111110',
'010L000000000000000000000000000000L010',
'010L000000000000000000000000000000L010',
'010L000000000000000000000000000000L010',
'0111111111111111111111111111111111L110',
'0000000000000000000000000000000010L010',
'0000000000000000000000000000000010L010',
'0111111111111111111111111111111110L010',
'0100000000000000000000000000000000L010',
'0100000000000000000000000000000000L010',
'0100P00000000000000000000000000000L010',
'01111111111111111111111111111111111110',
'00000000000000000000000000000000000000'
]

# -------------------
# BIOME MAP
# -------------------

biome_map = [
'00000000000000000000000000000000000000',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'03333333333333333333333333333333333330',
'00000000000000000000300000000000000000',
'00000000000000000000300000000000000000',
'00000000000000000000300000000000000000',
'00000000000000000000300000000000000000',
'00000000000000000000300000000000000000',
'00333333333333300000300000000000000000',
'00333333333333300000300000000000000000',
'00333333333333300000300000000000000000',
'00030000000000000000300000000000000000',
'00333333333333333333333333000000000000',
'00333333333333333333333333300000000000',
'00333333333333333333333333330000000000',
'00020000000000000000000000000000000000',
'00222222222222222222222222222222222200',
'00222222222222222222222222222222222200',
'00222222222222222222222222222222222200',
'00000000000000000000000000000000001000',
'00000000000000000000000000000000011100',
'00000000000000000000000000000000011100',
'00000000000000000000000000000000011100',
'00111111111111111111111111111111111100',
'00111111111111111111111111111111111100',
'00111111111111111111111111111111111100',
'00000000000000000000000000000000000000']

# -------------------
# NOMS DES BIOMES
# -------------------

biome_names = {
    "0": "vide",
    "1": "floor 0",
    "2": "floor 1",
    "3": "floor 2"
}

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

# LECTURE BIOME MAP
biome_tiles = {}

for y, row in enumerate(biome_map):
    for x, biome in enumerate(row):
        biome_tiles[(x, y)] = biome

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

# GAME LOOP
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

    on_ladder = False
    for tile in ladder_tiles:
        if player.colliderect(tile):
            on_ladder = True

    on_top_of_ladder = False
    for tile in ladder_tiles:
        if (
            player.bottom <= tile.top + 5 and
            player.bottom >= tile.top - 5 and
            player.right > tile.left and
            player.left < tile.right
        ):
            on_top_of_ladder = True

    if on_ladder:
        vel_y = 0

        if keys[pygame.K_z]:
            player.y -= 4

        if keys[pygame.K_s]:
            player.y += 4

    if keys[pygame.K_SPACE] and on_ground and not on_ladder:
        vel_y = jump_power
    if keys[pygame.K_SPACE] and on_top_of_ladder:
        vel_y = jump_power

    if not on_ladder:
        vel_y += gravity
        dy += vel_y

    player.x += dx

    for tile in tiles:
        if player.colliderect(tile):
            if dx > 0:
                player.right = tile.left
            if dx < 0:
                player.left = tile.right

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

    for tile in deadly_tiles:
        if player.colliderect(tile):
            respawn()

    camera_x = player.centerx - WIDTH // 2
    camera_y = player.centery - HEIGHT // 2

    # DETECTION BIOME JOUEUR
    player_tile_x = player.centerx // TILE_SIZE
    player_tile_y = player.centery // TILE_SIZE

    current_biome = biome_tiles.get((player_tile_x, player_tile_y), "0")
    biome_name = biome_names.get(current_biome, "inconnu")

    pygame.display.set_caption(f"URB-3x | Biome: {biome_name}")

    screen.blit(background, (0, 0))

    for tile in tiles:
        screen.blit(textures["1"], (tile.x - camera_x, tile.y - camera_y))

    for tile in deadly_tiles:
        screen.blit(textures["2"], (tile.x - camera_x, tile.y - camera_y))

    for tile in ladder_tiles:
        screen.blit(textures["L"], (tile.x - camera_x, tile.y - camera_y))

    screen.blit(player_texture, (player.x - camera_x, player.y - camera_y))

    for tile in no_collision_tiles:
        screen.blit(textures["3"], (tile.x - camera_x, tile.y - camera_y))

    pygame.display.update()
    clock.tick(60)
