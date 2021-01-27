import pygame
import os
pygame.font.init()
pygame.mixer.init()

SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 55,50
MISSLE_WIDTH , MISSLE_HEIGHT = 8,40
WIDTH , HEIGHT = 1200, 720

FPS = 60
VEL = 5
BULLET_VEL = 7
MISSLE_VEL = 8
MAX_BULLETS = 5
MAX_MISSLES = 1

RED = (255,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)

BORDER = pygame.Rect(WIDTH//2 - 5,50,2,HEIGHT)

#FONTS
HEALTH_FONT = pygame.font.SysFont('comicsans' , 50)
WINNER_FONT = pygame.font.SysFont('comicsans', 110)
VS_FONT = pygame.font.SysFont('comicsans' , 50)

# user events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
YELLOW_MISSLE_HIT = pygame.USEREVENT +3
RED_MISSLE_HIT = pygame.USEREVENT +4

# sound
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','bullet_hit.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','damage.mp3'))
MISSLE_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','missle_expl.mp3'))
MISSLE_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','explosion.wav'))


WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("space wars")

# MISSLE IMAGES
MISSLE_IMG = pygame.image.load(os.path.join('Assets','rocket1.png'))
IMG_MISSLE_RED = pygame.transform.rotate(pygame.transform.scale(MISSLE_IMG,(MISSLE_WIDTH,MISSLE_HEIGHT)),90)
IMG_MISSLE_YELLOW = pygame.transform.rotate(pygame.transform.scale(MISSLE_IMG,(MISSLE_WIDTH,MISSLE_HEIGHT)),270)

# spaceship images
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))
SPACE_SHIP_YELLOW = pygame.image.load(os.path.join('Assets' , 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(SPACE_SHIP_YELLOW,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
SPACE_SHIP_RED = pygame.image.load(os.path.join('Assets' , 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(SPACE_SHIP_RED,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)) , 270)

def draw_screen(red,yellow,red_bullets,yellow_bullets,missle_list_r,missle_list_y,red_health,yellow_health):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,(51,102,255),BORDER)
    vs_text = VS_FONT.render("Vs",1,WHITE)
    red_health_text = HEALTH_FONT.render("SKYFORCE: " + str(red_health),1,RED)
    yellow_health_text = HEALTH_FONT.render("VANGAURD: " + str(yellow_health), 1, YELLOW)
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width()-10,10))
    WIN.blit(vs_text,(WIDTH//2 - vs_text.get_width()//2 , 10))
    WIN.blit(yellow_health_text,(10,10))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    for missle in missle_list_r:
        WIN.blit(IMG_MISSLE_RED,(missle.x,missle.y))
    for missles in missle_list_y:
        WIN.blit(IMG_MISSLE_YELLOW,(missles.x,missles.y))
    pygame.display.update()

def yellow_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left movement
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < BORDER.x - yellow.width + 20:  # right movement
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # upward movement
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y - VEL + yellow.height + 20 < HEIGHT:  # downward movement
        yellow.y += VEL

def red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width :  # left movement
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH :  # right movement
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # upward movement
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y - VEL + red.height + 20 < HEIGHT:  # downward movement
        red.y += VEL

def handle_bullets(yellow_bullets,red_bullets,missle_list_y,missle_list_r,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
        elif bullet.x < 0:
            red_bullets.remove(bullet)

    for missle in missle_list_y:
        missle.x += MISSLE_VEL
        if red.colliderect(missle):
            missle_list_y.remove(missle)
            pygame.event.post(pygame.event.Event(RED_MISSLE_HIT))
        elif missle.x > WIDTH:
            missle_list_y.remove(missle)

    for missle in missle_list_r:
        missle.x -= MISSLE_VEL
        if yellow.colliderect(missle):
            missle_list_r.remove(missle)
            pygame.event.post(pygame.event.Event(YELLOW_MISSLE_HIT))
        elif missle.x < 0:
            missle_list_r.remove(missle)


def winner_font(text):
    win_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(win_text,(WIDTH//2 - win_text.get_width()//2,HEIGHT//2 - win_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    red = pygame.Rect(600,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    missle_list_r = []
    missle_list_y = []
    red_health = 10
    yellow_health = 10
    run = True
    clock = pygame.time.Clock()
    while run:
        # while will run FPS times per sec
        clock.tick(FPS)
        # checks if exit is clicked
        for event in pygame.event.get():  # checking different events
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # lasers or bullets
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width,yellow.y + yellow.height//2 + 8 - 2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 + 8 - 2 ,10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                # MISSLES
                if event.key == pygame.K_m and len(missle_list_r) < MAX_MISSLES:  # red missles
                    red_missle = pygame.Rect(red.x , red.y + red.height//2 + 8 - 8 ,MISSLE_WIDTH,MISSLE_HEIGHT)
                    missle_list_r.append(red_missle)
                    MISSLE_FIRE_SOUND.play()
                if event.key == pygame.K_x and len(missle_list_y) < MAX_MISSLES:  # yellow missles
                    yellow_missle = pygame.Rect(yellow.x + yellow.width,yellow.y + yellow.height//2 + 8 - 8 ,MISSLE_WIDTH,MISSLE_HEIGHT)
                    missle_list_y.append(yellow_missle)
                    MISSLE_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_MISSLE_HIT:
                yellow_health -= 3
                MISSLE_HIT_SOUND.play()
            if event.type == RED_MISSLE_HIT:
                red_health -= 3
                MISSLE_HIT_SOUND.play()
        winner_text = ""
        if red_health <= 0:
            winner_text = "VANGAURD RULES !"
            winner_font(winner_text)
        if yellow_health <= 0:
            winner_text = "SKYFORCE LEADS !"
            winner_font(winner_text)
        if winner_text != "":
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,missle_list_y,missle_list_r,yellow,red)
        draw_screen(red,yellow,red_bullets,yellow_bullets,missle_list_r,missle_list_y,red_health,yellow_health)

    # for single game add pygame.quit() here else for rematch
    pygame.quit()   # call main() here and quit in above after 102 line

if __name__ == "__main__":
    main()
