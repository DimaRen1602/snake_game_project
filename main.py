import pygame
import time
import random
import os

# Инициализация Pygame
pygame.init()

# Цветовые константы
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Параметры дисплея
dis_width = 1024
dis_height = 768
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка на Python')

clock = pygame.time.Clock()

# Изменим размер блока змейки на делитель размеров окна
snake_block = 16  # 16 является делителем 1024 и 768
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Глобальная переменная для лучшего счёта
high_score = 0

# Функции загрузки и сохранения лучшего счёта остаются без изменений
def load_high_score():
    global high_score
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                high_score = int(f.read())
            except:
                high_score = 0
    else:
        high_score = 0

def save_high_score(score):
    global high_score
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))

def Your_score(score):
    value = score_font.render("Ваш счёт: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def High_score_display():
    value = score_font.render("Лучший счёт: " + str(high_score), True, yellow)
    dis.blit(value, [dis_width - 250, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    load_high_score()  # Загружаем лучший счёт при старте игры
    game_over = False
    game_close = False

    # Выравниваем начальные позиции змейки по сетке
    x1 = dis_width // (2 * snake_block) * snake_block
    y1 = dis_height // (2 * snake_block) * snake_block

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Корректируем генерацию позиции еды
    def generate_food():
        foodx = random.randint(0, (dis_width - snake_block) // snake_block) * snake_block
        foody = random.randint(0, (dis_height - snake_block) // snake_block) * snake_block
        return foodx, foody

    foodx, foody = generate_food()

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("Вы проиграли! Нажмите C-играть снова или Q-выход", red)
            Your_score(Length_of_snake - 1)
            High_score_display()  # Отображаем лучший счёт на экране
            pygame.display.update()

            save_high_score(Length_of_snake - 1)  # Сохраняем лучший счёт

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        High_score_display()  # Отображаем лучший счёт во время игры

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food()
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
