import sys
import random
import pygame
import time

pygame.init()

WIN_X, WIN_Y = 800, 600
WIN = pygame.display.set_mode((WIN_X, WIN_Y))
pygame.display.set_caption('Snake Game')
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont('comicsans', 40)


def main():
    snake_block_width = 10
    init_snake_length = 3
    snake_color = (0, 255, 255)
    fruit_color = (24, 100, 9)
    golden_fruit_color = (255, 215, 0)
    fruit_pos = [0, 0]
    fruit_spawn = True
    golden_fruit_spawn = True
    golden_fruit_show = False
    golden_fruit_pos = [1000, 1000]
    golden_fruit_counter = 100
    opposite_direction = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    head = [
        random.randint(snake_block_width * init_snake_length * 2, WIN_X - init_snake_length * snake_block_width * 2),
        random.randint(0, WIN_Y - snake_block_width)]
    x, y = head

    snake_body = [[x - snake_block_width * i, y] for i in range(init_snake_length, -1, -1)]
    direction = 'right'
    score = 0

    while True:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()

            previous_direction = direction

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                direction = 'up'
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                direction = 'down'
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                direction = 'right'
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                direction = 'left'

            if opposite_direction[direction] == previous_direction:
                direction = previous_direction
        WIN.fill((0, 0, 0))
        # pygame.draw.rect(WIN, fruit_color, (0, 0, WIN_X, WIN_Y))
        # pygame.draw.rect(WIN, (0, 0, 0), (
        #     snake_block_width // 3, snake_block_width // 3, WIN_X - snake_block_width // 2,
        #     WIN_Y - snake_block_width // 2))

        for square in snake_body:
            pygame.draw.rect(WIN, snake_color, (square[0], square[1], snake_block_width, snake_block_width))

        if direction == 'right':
            head[0] += snake_block_width
        elif direction == 'left':
            head[0] -= snake_block_width
        elif direction == 'up':
            head[1] -= snake_block_width
        elif direction == 'down':
            head[1] += snake_block_width

        if head[0] < 0:
            head[0] = WIN_X
        elif head[0] > WIN_X:
            head[0] = 0
        elif head[1] < 0:
            head[1] = WIN_Y
        elif head[1] > WIN_Y:
            head[1] = 0

        snake_body.append(list(head))

        if fruit_spawn:
            fruit_pos = [random.randrange(30, WIN_X - 30), random.randrange(30, WIN_Y - 30)]
            fruit_spawn = False

        if golden_fruit_spawn and golden_fruit_show:
            golden_fruit_pos = [random.randrange(30, WIN_X - 30), random.randrange(30, WIN_Y - 30)]
            if golden_fruit_pos == fruit_pos:
                golden_fruit_pos = [random.randrange(30, WIN_X - 30), random.randrange(30, WIN_Y - 30)]
            golden_fruit_spawn = False

        if golden_fruit_counter == 0:
            golden_fruit_show = golden_fruit_show ^ True
            if golden_fruit_show:
                golden_fruit_spawn = True
            golden_fruit_counter = random.randrange(100, 150)
        else:
            golden_fruit_counter -= 1

        pygame.draw.rect(WIN, fruit_color, (fruit_pos[0], fruit_pos[1], snake_block_width, snake_block_width))
        if golden_fruit_show:
            pygame.draw.rect(WIN, golden_fruit_color,
                             (golden_fruit_pos[0], golden_fruit_pos[1], snake_block_width, snake_block_width))
        else:
            golden_fruit_pos = [1000, 1000]
        snake_head = pygame.Rect(head[0], head[1], snake_block_width, snake_block_width)
        snake_block = [pygame.Rect(block[0], block[1], snake_block_width, snake_block_width) for block in snake_body]
        fruit_block = pygame.Rect(fruit_pos[0], fruit_pos[1], snake_block_width, snake_block_width)
        golden_fruit_block = pygame.Rect(golden_fruit_pos[0], golden_fruit_pos[1], snake_block_width, snake_block_width)

        if fruit_block.colliderect(snake_head):
            fruit_spawn = True
            score += 10
        elif golden_fruit_block.colliderect(snake_head):
            score += 50
            golden_fruit_counter = 0

        else:
            snake_body.pop(0)

        for block in snake_block[0:len(snake_block) - 1]:
            if snake_head.colliderect(block):
                game_over(score)
                sys.exit()

        score_font = font.render(f'{score}', True, (0, 255, 0))
        font_pos = score_font.get_rect(center=(WIN_X // 2 - 40, 30))
        WIN.blit(score_font, font_pos)

        pygame.display.update()
        CLOCK.tick(24)


def main_menu():

    while 1:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                time.sleep(0.5)

                main()
        WIN.fill((0, 0, 0))

        main_menu_message = font.render('Press any key to start the game', True, (255, 255, 255))
        font_pos = main_menu_message.get_rect(center=(WIN_X//2, WIN_Y//2))
        WIN.blit(main_menu_message, font_pos)
        pygame.display.update()


def game_over(score):

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        WIN.fill((0, 0, 0))
        game_over_message = font.render('You Lost', True, (255, 0, 0))
        game_over_score = font.render(f'Your Score was {score}', True, (255, 255, 255))

        font_pos_message = game_over_message.get_rect(center=(WIN_X // 2, WIN_Y // 2))
        font_pos_score = game_over_score.get_rect(center=(WIN_X // 2, WIN_Y // 2 + 32))
        WIN.blit(game_over_message, font_pos_message)
        WIN.blit(game_over_score, font_pos_score)
        pygame.display.update()
        time.sleep(2)
        main_menu()


main_menu()
