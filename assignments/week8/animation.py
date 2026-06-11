import pygame
import math


pygame.init()

# set screen
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Clothesline Project")

clock = pygame.time.Clock()

# add clothes
tshirt = pygame.image.load("tshirt.png").convert_alpha()
hoodie = pygame.image.load("hoodie.png").convert_alpha()
pants = pygame.image.load("pants.png").convert_alpha()
socks = pygame.image.load("socks.png").convert_alpha()
shorts = pygame.image.load("shorts.png").convert_alpha()

# resize clothes

tshirt = pygame.transform.scale(tshirt, (200, 200))
hoodie = pygame.transform.scale(hoodie, (420, 420))
pants = pygame.transform.scale(pants, (530, 530))
socks = pygame.transform.scale(socks, (240, 240))
shorts = pygame.transform.scale(shorts, (400, 400))

running = True

# make clothes wobbly
offset_x = -1000
speed = 1

while running:
    clock.tick(60)

    offset_x += speed

    # loop after leaving screen
    if offset_x > width + 300:
        offset_x = -1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # set background
    screen.fill((135, 206, 235))

    pygame.draw.circle(screen, (255, 255, 255), (150, 100), 40)
    pygame.draw.circle(screen, (255, 255, 255), (190, 100), 50)
    pygame.draw.circle(screen, (255, 255, 255), (240, 100), 40)

    pygame.draw.circle(screen, (255, 255, 255), (500, 80), 45)
    pygame.draw.circle(screen, (255, 255, 255), (550, 80), 60)
    pygame.draw.circle(screen, (255, 255, 255), (610, 80), 45)

    pygame.draw.circle(screen, (255, 255, 255), (800, 120), 40)
    pygame.draw.circle(screen, (255, 255, 255), (840, 120), 50)
    pygame.draw.circle(screen, (255, 255, 255), (890, 120), 40)

    pygame.draw.rect(screen, (80, 180, 80), (0, 450, width, 200))

    # clothesline
    pygame.draw.line(
        screen,
        (139, 90, 43),
        (0, 150),
        (1000, 150),
        5
    )


    # wobble effect

    time = pygame.time.get_ticks()


    def wobble(i):
        return 5 * math.sin(time * 0.002 + i)


    screen.blit(tshirt, (offset_x + 20, 150 + wobble(1)))
    screen.blit(hoodie, (offset_x + 140, 80 + wobble(2)))
    screen.blit(pants, (offset_x + 330, 50 + wobble(3)))
    screen.blit(shorts, (offset_x + 570, 50 + wobble(4)))
    screen.blit(socks, (offset_x + 780, 90 + wobble(5)))

    # add clothes pins for vibes lol

    pygame.draw.rect(screen, (200, 160, 100), (offset_x + 30, 140, 10, 20))
    pygame.draw.rect(screen, (200, 160, 100), (offset_x + 150, 140, 10, 20))
    pygame.draw.rect(screen, (200, 160, 100), (offset_x + 340, 140, 10, 20))
    pygame.draw.rect(screen, (200, 160, 100), (offset_x + 580, 140, 10, 20))
    pygame.draw.rect(screen, (200, 160, 100), (offset_x + 790, 140, 10, 20))


    pygame.display.flip()

pygame.quit()
