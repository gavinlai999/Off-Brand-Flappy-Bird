import random
import pygame

pygame.init()

width = 1280
height = 720
fps = 60
#Colors
blue = (0, 102, 204)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
red = (255, 0, 0)
yellow = (255, 255, 0)

#jumping sound effects
pygame.mixer.init()
pygame.mixer.music.load("Powerful-Trap-.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()

#variables
player_x = 255
player_y = 255
y_change = 0
jump_height = 12
gravity = .9
speed = 3
score = 0
high_score = 0
font = pygame.font.Font("freesansbold.ttf", 20)
screen = pygame.display.set_mode([width, height])
timer = pygame.time.Clock()
pygame.display.set_caption("Jet Game")
generate_places = True
game_over = False

#list
obstacles = [1000, 1300, 1600, 1900, 2100, 2400, 2700]
y_positions = []
stars = []

#player looks
def draw_player(x_pos, y_pos):
    global y_change
    mouth = pygame.draw.circle(screen, gray, (x_pos + 25, y_pos + 15), 12)
    play = pygame.draw.rect(screen, white, [x_pos, y_pos, 30, 30], 0, 12)
    eyeball = pygame.draw.circle(screen, black, (x_pos + 24, y_pos + 12), 5)
    jetpack = pygame.draw.rect(screen, white, [x_pos - 20, y_pos, 18, 28 ], 3, 2)
    if y_change < 0:
        flame1 = pygame.draw.rect(screen, red, [x_pos-20, y_pos + 29, 7, 20], 0, 2)
        flame1_yellow = pygame.draw.rect(screen, yellow, [x_pos - 18, y_pos + 30, 3, 18], 0, 2)
        flame2 = pygame.draw.rect(screen, red, [x_pos - 10, y_pos + 29, 7, 20], 0, 2)
        flame2_yellow = pygame.draw.rect(screen, yellow, [x_pos - 8, y_pos + 30, 3, 18], 0, 2)
    return play

#obstacles style
def draw_obstacles(obstacles, y_pos, player):
    global game_over
    for i in range(len(obstacles)):
        y_coord = y_pos[i]
        top_rectangle = pygame.draw.rect(screen, green, [obstacles[i], 0, 30, y_coord])
        top_rectangle2 = pygame.draw.rect(screen, green, [obstacles[i] - 3, y_coord - 15, 36, 20], 0, 5)
        bot_rectangle = pygame.draw.rect(screen, green, [obstacles[i], y_coord + 200, 30, height - (y_coord + 70)])
        bot_rectangle2 = pygame.draw.rect(screen, green, [obstacles[i] - 3, y_coord + 200, 36, 20], 0, 5)
        #game ends when player crashes into a obtsacle(tube thinge)
        if top_rectangle.colliderect(player) or bot_rectangle.colliderect(player):
            game_over = True
            #Plays dying soundeffect from flappy bird when player crashes
        if game_over:
            pygame.mixer_music.stop()
            pygame.mixer.music.load('mi_explosion_03_hpx.mp3')  
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play()
#draw stars that are repeated to stars that go off screen to the left by 3 and
#offscreen to the right by 3 with random different y position
def draw_stars(stars):
    global total
    for i in range(total - 1):
        pygame.draw.rect(screen, white, [stars[i][0], stars[i][1], 3, 3], 0, 2)
        stars[i][0] -= 0.5
        if stars [i][0] < -3:
            stars[i][0] = width + 3
            stars[i][1] = random.randint(0, height)
    return stars

running = True
while running:
    timer.tick(fps)
    screen.fill(blue)
# star and obstacles generator
    if generate_places:
        for i in range(len(obstacles)):
            y_positions.append(random.randint(0, 300))
            total = 100
            for i in range(total):
                x_pos = random.randint(0, width)
                y_pos = random.randint(0, height)
                stars.append([x_pos, y_pos])
        generate_places = False
#player spawn location(Variables defined above)
    stars = draw_stars(stars)
    player = draw_player(player_x, player_y)
    draw_obstacles(obstacles, y_positions, player)
#keybinds and what happens when you hit an obstacle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                y_change = -jump_height
#When you lose game and click space, the game restarts
            if event.key == pygame.K_SPACE and game_over:
                player_x = 225
                player_y = 225
                y_change = 0
                generate_places = True
                obstacles = [400, 700, 1000, 1300, 1600]
                y_positions = []
                score = 0
                pygame.mixer.init()
                pygame.mixer.music.load("Powerful-Trap-.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
                game_over = False


    if player_y + y_change < height - 30:
        player_y += y_change
        y_change += gravity
    else:
        player_y = height - 30
    #When game runs out of obstacles to display, random obstacles are displayed around the
    # intervals of the obstacles in the obstacles list and the old obstacle's lengths are removed
    for i in range(len(obstacles)):
        if not game_over:
            obstacles[i] -= speed
            if obstacles[i] < -30:
                obstacles.remove(obstacles[i])
                y_positions.remove(y_positions[i])
                obstacles.append(random.randint(obstacles[-1] + 280, obstacles[-1] + 320))
                y_positions.append(random.randint(0,300))
                score += 1
#Score info
    if score > high_score:
        high_score = score

    if game_over:
        game_over_text = font.render("Game Over! Click Space Bar to Restart!", True, white)
        screen.blit(game_over_text, (450, 300))
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, (10, 10))
    high_score_text = font.render("High Score: " + str(high_score), True, white)
    screen.blit(high_score_text, (10, 35))

    pygame.display.flip()
pygame.quit()