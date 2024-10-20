import pygame
import random
#######################################
pygame.init()

screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Dodge")

clock = pygame.time.Clock()

total_score = 0
level_control = 10
total_level = 0
total_level_list = [10, 30, 50, 70, 90, 100, 120, 150, 180, 200, 250, 300, 350, 400, 10000000]
A = []
game_font = pygame.font.Font('arial.ttf', 20)

background = pygame.image.load("back.png")
img = pygame.image.load('img.png')
img = pygame.transform.scale(img, (21, 21))

player = pygame.image.load("player_small.png")
player_size = player.get_rect().size
player_width = player_size[0]
plyaer_height = player_size[1]
player_x_pos = (screen_width / 2) - (player_width / 2)
player_y_pos = (screen_height / 2) - (plyaer_height / 2)


player_to_x = 0
player_to_y = 0

player_speed = 0.3

enemy_list = list()
class enemy_class:
    enemy_image = img
    enemy_size = enemy_image.get_rect().size
    enemy_width = enemy_size[0]
    enemy_height = enemy_size[1]
    enemy_spawnPoint = None
    enemy_speed = 0
    enemy_x_pos = 0
    enemy_y_pos = 0
    enemy_rad = 0

    enemy_rect = enemy_image.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    def __init__(self):
        self.enemy_speed = random.choice([1.0, 1.5, 2.0, 2.5, 3.0])
        self.enemy_spawnPoint = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

        # 스폰 지점 설정
        if self.enemy_spawnPoint == 'LEFT':
            self.enemy_x_pos = - self.enemy_width
            self.enemy_y_pos = random.randint(0, screen_height - self.enemy_height)
            self.enemy_rad = random.choice([(1, 3), (1, 2), (2, 2), (2, 1), (3, 1), (3, 0), (1, -3), (1, -2), (2, -2), (2, -1), (3, -1)])
        elif self.enemy_spawnPoint == 'RIGHT':
            self.enemy_x_pos = screen_width
            self.enemy_y_pos = random.randint(0, screen_height - self.enemy_height)
            self.enemy_rad = random.choice([(-1, 3), (-1, 2), (-2, 2), (-2, 1), (-3, 1), (-3, 0), (-1, -3), (-1, -2), (-2, -2), (-2, -1), (-3, -1)])
        elif self.enemy_spawnPoint == 'UP':
            self.enemy_x_pos = random.randint(0, screen_width - self.enemy_width)
            self.enemy_y_pos = - self.enemy_height
            self.enemy_rad = random.choice([(3, 1), (2, 1), (2, 2), (1, 2), (1, 3), (0, 3), (-3, 1), (-2, 1), (-2, 2), (-1, 2), (-1, 3)])
        elif self.enemy_spawnPoint == 'DOWN':
            self.enemy_x_pos = random.randint(0, screen_width - self.enemy_width)
            self.enemy_y_pos = screen_height
            self.enemy_rad = random.choice([(3, -1), (2, -1), (2, -2), (1, -2), (1, -3), (0, -3), (-3, -1), (-2, -1), (-2, -2), (-1, -2), (-1, -3)])
    # 메서드
    def enemy_move(self):
        self.enemy_x_pos+=self.enemy_speed*self.enemy_rad[0]
        self.enemy_y_pos+=self.enemy_speed*self.enemy_rad[1]
        global total_score

        def boundary_UP():
            if self.enemy_y_pos<-self.enemy_height:
                return True

        def boundary_DOWN():
            if self.enemy_y_pos>screen_height:
                return True

        def boundary_LEFT():
            if self.enemy_x_pos<-self.enemy_width:
                return True

        def boundary_RIGHT():
            if self.enemy_x_pos>screen_width:
                return True

        if self.enemy_spawnPoint == 'UP':
            if boundary_LEFT() or boundary_RIGHT() or boundary_DOWN():
                enemy_list.remove(self)
                total_score += 1

        if self.enemy_spawnPoint == 'DOWN':
            if boundary_LEFT() or boundary_RIGHT() or boundary_UP():
                enemy_list.remove(self)
                total_score += 1

        if self.enemy_spawnPoint == 'LEFT':
            if boundary_UP() or boundary_DOWN() or boundary_RIGHT():
                enemy_list.remove(self)
                total_score += 1

        if self.enemy_spawnPoint == 'RIGHT':
            if boundary_UP() or boundary_DOWN() or boundary_LEFT():
                enemy_list.remove(self)
                total_score += 1

    def enemy_coll(self):
        self.enemy_rect = self.enemy_image.get_rect()
        self.enemy_rect.left = self.enemy_x_pos
        self.enemy_rect.top = self.enemy_y_pos

running=True

while running:
    dt=clock.tick(60)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                player_to_x-=player_speed
            if event.key==pygame.K_RIGHT:
                player_to_x+=player_speed
            if event.key==pygame.K_UP:
                player_to_y-=player_speed
            if event.key==pygame.K_DOWN:
                player_to_y+=player_speed

        if event.type==pygame.KEYUP:
            if event.key in [pygame.K_LEFT,pygame.K_RIGHT]:
                player_to_x=0
            if event.key in [pygame.K_UP,pygame.K_DOWN]:
                player_to_y=0

    player_x_pos+=player_to_x*dt
    player_y_pos+=player_to_y*dt

    # 플레이어 경계값
    if player_x_pos<0:
        player_x_pos=0
    elif player_x_pos>screen_width-player_width:
        player_x_pos=screen_width-player_width
    if player_y_pos<0:
        player_y_pos=0
    elif player_y_pos>screen_height-plyaer_height:
        player_y_pos=screen_height-plyaer_height

    # 적 생성
    if total_score>=total_level_list[total_level]:
        total_level+=1

    if total_level+level_control>=len(enemy_list):
        enemy_list.append(enemy_class())

    # 충돌 처리
    player_rect=player.get_rect()
    player_rect.left=player_x_pos
    player_rect.top=player_y_pos

    for i in enemy_list:
        i.enemy_coll()
        if player_rect.colliderect(i.enemy_rect):
            print("충돌")
            print("점수 : ",total_score)
            running=False

    # 화면에 그리기

    screen.blit(background,(0,0))
    screen.blit(player,(player_x_pos,player_y_pos))

    for i in enemy_list:
        i.enemy_move()
        screen.blit(i.enemy_image,(i.enemy_x_pos,i.enemy_y_pos))

    enemy_count=game_font.render(str(len(enemy_list)),True,(255,255,255))
    screen.blit(enemy_count,(10,10))

    score=game_font.render(str(int(total_score)),True,(255,255,255))
    screen.blit(score,(screen_width-50,10))

    pygame.display.update()