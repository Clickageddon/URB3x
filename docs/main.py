import sys
import pygame

def init_game():
    pygame.init()
    pygame.display.set_caption("UBR3x")
    screen = pygame.display.set_mode((640, 640))
    clock = pygame.time.Clock()
    img = pygame.image.load('Bingus.png')
    return screen, clock, img

def run_game(screen, clock, img):
    running = True
    while running:
        screen.blit(img, (100, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

def main():
    screen, clock, img = init_game()
    run_game(screen, clock, img)

if __name__ == "__main__":
    main()
