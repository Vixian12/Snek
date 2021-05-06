import pygame, sys, random

from pygame.math import Vector2
# eliminates the need to write 'pygame.math' before the vector
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/Sound_crunch.wav')
        self.points_sound = pygame.mixer.Sound('Sound/ten_points.wav')
        self.fail_sound = pygame.mixer.Sound('Sound/collision_hit.wav')

        self.refesh_time = 150

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            # 1. we still need a rect for positioning
            if index == 0:
                screen.blit(self.head,block_rect)
                # updates snake head direction
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x ==  next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y ==  next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
            #2. What direction is the face heading?

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
            self.head = self.head_left
        elif head_relation == Vector2(-1,0):
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):
            self.head = self.head_down

        #for block in self.body:
            #x_pos = int(block.x * cell_size)
            #y_pos = int(block.y * cell_size)
            #block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            #pygame.draw.rect(screen, (133, 191, 122), block_rect)
            # create a rect
            # draw the rect
        #this is old code

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def play_points_sound(self):
        self.points_sound.play()

    def play_fail_sound(self):
        self.fail_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0,0)

class FRUIT:
    def __init__(self):
      self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        #pygame.draw.rect(screen,(126, 100, 114),fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_width - 1)
        self.y = random.randint(1, cell_height - 1)
        # fruit will randomise anywhere within the screen, EXCEPT for the banner
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.highscore_score = 0
        self.volume = pygame.image.load('Graphics/icons8-speaker-30.png')
        self.mute = pygame.image.load('Graphics/icons8-mute-30.png')
        self.playing = True

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_volume()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            if (len(main_game.snake.body) - 2) % 10 == 0 and (len(main_game.snake.body) - 3) != 0:
                self.snake.play_points_sound()
                #self.snake.refesh_time -= 100
                #pygame.time.set_timer(SCREEN_UPDATE, refresh_time)
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
            # repositions fruit
            # adds another block to the snake

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_width or not 1 <= self.snake.body[0].y < cell_height :
            self.game_over()
        # check if the snake is outside the screen
        #collision also occurs when hitting the banner

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
        # check if snake hits itself

    def game_over(self):
        score_text = str(len(self.snake.body) - 3)
        highscore_score = str(score_text)
        if self.snake.direction != Vector2(0,0):
            self.snake.play_fail_sound()
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167,209,61)
        top_color = (242, 242, 226)
        border_color = (56,74,12)
        for row in range(cell_height):
            if row == 1:
                top_rect = pygame.Rect(0,0,cell_width*cell_size, cell_size)
                linebottom_rect = pygame.Rect(0,cell_size-2,cell_width*cell_size,2)
                linetop_rect = pygame.Rect(0,0,cell_width*cell_size,2)
                lineleft_rect = pygame.Rect(0,0,2,cell_size)
                lineright_rect = pygame.Rect((cell_width*cell_size)-2,0,2,cell_size)

                pygame.draw.rect(screen,top_color,top_rect)
                pygame.draw.rect(screen,border_color,linebottom_rect)
                pygame.draw.rect(screen, border_color, linetop_rect)
                pygame.draw.rect(screen,border_color,lineleft_rect)
                pygame.draw.rect(screen,border_color,lineright_rect)
                #making the top 'banner'
            if row % 2 == 0:
                for col in range(cell_width):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_width):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56,74,12))
        score_x = int(cell_size * cell_width - 60)
        score_y = int(cell_size * cell_height - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, (164,209,61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen, (56,74,12), bg_rect, 2)

        if int(self.highscore_score) <= int(score_text):
            self.highscore_score = score_text

        highscore_text = 'Highscore: '
        highscore_x = int((cell_size*cell_width) /2)
        highscore_y = int(cell_size-20)
        highscore_text_surface = game_font.render(highscore_text + str(self.highscore_score), True, (56, 74, 12))
        highscore_text_rect = highscore_text_surface.get_rect(center=(highscore_x, highscore_y))

        screen.blit(highscore_text_surface, highscore_text_rect)

    def draw_volume(self):
       speaker = pygame.image.load('Graphics/icons8-speaker-30.png')
       mute = pygame.image.load('Graphics/icons8-mute-30.png')
       music_playing = pygame.mixer.get_busy()
       speaker_x = cell_width*cell_size-7
       speaker_y = 5
       speaker_rect = speaker.get_rect(topright = (speaker_x,speaker_y))

       #if event.type == pygame.MOUSEBUTTONUP:
       pos = pygame.mouse.get_pos()

       if self.playing == True and speaker_rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONUP:
           pygame.mixer.music.set_volume(0)
           screen.blit(mute,speaker_rect)
           self.playing = False
       elif self.playing == False and speaker_rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONUP:
           pygame.mixer.music.set_volume(0.3)
           screen.blit(speaker, speaker_rect)
           self.playing = True
       elif self.playing == False:
           screen.blit(mute, speaker_rect)
       elif self.playing == True:
           screen.blit(speaker, speaker_rect)



vol = 0.3
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.mixer.music.load('Sound/guitar_house.mp3')
pygame.mixer.music.set_volume(vol)
pygame.mixer.music.play(-1,0,0)

# needed to make pygame run
cell_size = 40
cell_number = 17
cell_width = 20
cell_height = 17
screen = pygame.display.set_mode((cell_width * cell_size, cell_height * cell_size))
# creates window
clock = pygame.time.Clock()
# this will be used to cap the max framerate
apple = pygame.image.load('/Users/Maia/PycharmProjects/pythonGame/Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

refresh_time = 150

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()
main_game.snake.fail_sound.set_volume(vol)
main_game.snake.points_sound.set_volume(vol)
main_game.snake.crunch_sound.set_volume(vol)

while True:
    # all elements will be displayed here
    for event in pygame.event.get():
        # this allows the window to close.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            # the pygame command reads user input and closes the window, and the sys command is an added layer of protection
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
                    # inverting direction causes an instant fail, so this statement prevents the snake fom directly reversing itself
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    # keeps the window from closing automatically
    clock.tick(60)
    # caps the framerate at 60 fpsws