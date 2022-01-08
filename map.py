import pygame
import random


screen = pygame.display.set_mode((400, 400))

# changing title of the game window
pygame.display.set_caption('candy crash saga')

# 블럭 색 정하기
color = []
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = pygame.image.load("candy/red.PNG").convert()
PURPLE = pygame.image.load("candy/pauple.PNG").convert()
ORANGE = pygame.image.load("candy/orange.PNG").convert()
GREEN = pygame.image.load("candy/green.PNG").convert()
BLUE = pygame.image.load("candy/blue.PNG").convert()
# 바탕색
map_color = (90, 109, 129)
# 리스트에 블럭 색 정리
color.append(RED)
color.append(PURPLE)
color.append(ORANGE)
color.append(GREEN)
color.append(BLUE)
# 좌표에 랜덤 블럭 넣기
coordinate = [] #좌표리스트
b = [] #랜덤 값 리스트

x = 0
y = 0
count = 0
for i in range(0, 25):
    c = []
    if i == 0:
        pass
    else:
        x += 81
        count += 1
        if count == 5:
            x = 0
            y += 81
            count = 0
    c.append(x)
    c.append(y)
    coordinate.append(c)
    b.append(random.randrange(0,5))
# 게임 실행
run = True
while run:
    screen.fill(map_color)
    for u in range(25):
        screen.blit(color[b[u]], (coordinate[u][0], coordinate[u][1]))
    for i in range(1,6):
        pygame.draw.line(screen, BLACK, (80*i, 0), (80*i, 400), 5)
        pygame.draw.line(screen, BLACK, (0, 80*i), (400, 80*i), 5)

    pygame.display.update()