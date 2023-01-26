import base64
import io
import os
import random
import time

import pygame

screen_size = [500, 500]

block_size = 20

FPS = 10

game_difficulty = "easy"

score = 0

highscores = []

pygame.init()
flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.NOFRAME
# full screen and centered
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode(screen_size, flags, vsync=1)
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

snake_length = 3


def base64_to_sprite(base64_string):
    output = io.BytesIO(base64.b64decode(base64_string))
    sprite = pygame.image.load(output).convert_alpha()
    sprite = pygame.transform.scale(sprite, (block_size, block_size))
    return sprite


head = 'iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAB0SURBVChTY3TYKv+fAQc44P2QEcpkYILSDN9X80BZCIBsCFghSBFn6BewwH6vB2AMAzDFYIUwRTDAyMgIshbKgyjG60ZkAHcjIYChEOQ+kLXIVoMA3DPI4P///yB3QXmQYIK7EdnnyAAWlnCr8SliYGBgAACyti/L6Ke/WAAAAABJRU5ErkJggg=='
head_sprite = base64_to_sprite(head)

body = 'iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAAXNSR0IArs4c6QAAAEtJREFUKFNjdNgq/58BCXxfzQPmcYZ+QRZmYIQpBClAl0QWAyvEZQqyONxEFHuwcBjNE7T/o1uJrg5kMvEK0X2Nywmke4ao4CEmwAElAjglrNSPmwAAAABJRU5ErkJgggAA'
body_sprite = base64_to_sprite(body)

apple = 'iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAAXNSR0IArs4c6QAAAGZJREFUKFOV0MENgCAMBdDfXRjKm44mN3eSRTx902KJNfQgISTQx29AkIy1gNfZi4dAZOYU1QarLQQDJEC/tBVgb30nNp/ljWYdFJsekPSj4CNMkLePickPjMTQ/oPDY37BGfY0rd2ZkyALjNFMHAAAAABJRU5ErkJgggAA'
apple_sprite = base64_to_sprite(apple)

fire = 'iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAAXNSR0IArs4c6QAAAGJJREFUKFONkMEOgDAIQ0v8bQ877LfNDGhJa2KUwzbYWykLPGINrBgIlpl3QS/yrHDlufBV7tpAYVNscAcwXdW8lFpCGfPaqPoLLGvmj2o0Ku1d8Qu0IbZ78CPMZ39PD/ICntEUNImh3h2TAAAAAElFTkSuQmCC'
fire_sprite = base64_to_sprite(fire)


def display_score():
    global score

    font = pygame.font.Font("8bit.ttf", 16)
    text = font.render("Score: " + str(score), True, (255, 255, 255))

    screen.blit(text, [screen_size[0] - 150, block_size])


def show_highscores():
    global score
    global highscores

    # check if "highscores.txt" exists
    if not os.path.exists("highscores.txt"):
        # if not, create it
        with open("highscores.txt", "w") as file:
            for i in range(10):
                file.write("0\n")

    # open highscores file and add each line to the highscores list
    with open("highscores.txt", "r") as file:
        for line in file:
            highscores.append(int(line))

    # add the current score to the highscores list
    highscores.append(score)

    # sort the highscores list in descending order
    highscores.sort(reverse=True)

    # show only the top 10 highest scores
    highscores = highscores[:10]

    # open highscores file and write the top 10 scores to it
    with open("highscores.txt", "w") as file:
        for score in highscores:
            file.write(str(score) + "\n")

    while True:
        # set font for highscores
        ts_font = pygame.font.Font("8bit.ttf", 36)

        # print "Top Scores" to the top center of the screen in alternating colors
        # list of colors
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

        for i in range(len(colors)):
            # clear the screen
            screen.fill((0, 0, 0))

            text = ts_font.render("Top Scores", True, colors[i])
            screen.blit(text, [screen_size[0] / 2 - text.get_width() / 2, 20])

            # update the screen
            pygame.time.wait(100)

            # print the top 10 scores to the screen
            font = pygame.font.Font("8bit.ttf", 20)
            for i in range(len(highscores)):
                text = font.render(str(i + 1) + ". " + str(highscores[i]), True, (255, 255, 255))
                screen.blit(text, [(screen_size[0] / 2) - 40, 110 + i * 30])

            # print "Press any key to continue" to the bottom center of the screen
            font = pygame.font.Font("8bit.ttf", 16)
            text = font.render("Press any key to continue", True, (255, 255, 255))
            screen.blit(text, [screen_size[0] / 2 - text.get_width() / 2, screen_size[1] - 40])

            # update the screen
            pygame.display.update()

            # wait for a keypress
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return


def display_time(time):
    font = pygame.font.Font("8bit.ttf", 16)
    text = font.render("Alive for: {} seconds".format(str(time)), True, (255, 255, 255))

    # draw time to top left of screen
    screen.blit(text, [20, block_size])


def random_number():
    x, y = random.randrange(block_size, screen_size[0] - block_size, block_size), random.randrange(40, screen_size[
        1] - block_size, block_size)
    return x, y


def random_color():
    r, g, b = random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)
    return r, g, b


def main_menu():
    while True:
        # set up main menu screen with black background
        screen.fill((0, 0, 0))

        # set font for main menu
        font = pygame.font.Font("8bit.ttf", 32)

        # print "SNAKE GAME" to top center of screen
        text = font.render("SNAKE GAME", True, (255, 255, 255))
        screen.blit(text, [screen_size[0] / 2 - (text.get_size()[0] / 2), 100])

        # print "Press ESC to quit" to bottom center of screen
        font = pygame.font.Font("8bit.ttf", 16)
        text = font.render("Press ESC to quit", True, (255, 255, 255))
        screen.blit(text, [screen_size[0] / 2 - (text.get_size()[0] / 2), screen_size[1] - 100])

        font = pygame.font.Font("8bit.ttf", 32)
        # let player choose easy or hard mode, using left and right arrow keys, highlight selected mode as red, default as white
        mode = "easy"
        # get key presses
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        mode = "easy"
                    if event.key == pygame.K_DOWN:
                        mode = "hard"
                    if event.key == pygame.K_RETURN:
                        return mode
                    if event.key == pygame.K_ESCAPE:
                        mode = "quit"

            if mode == "easy":
                text = font.render("Easy", True, (255, 0, 0))
                screen.blit(text, [screen_size[0] / 2 - (text.get_size()[0] / 2), 200])
                text = font.render("Hard", True, (255, 255, 255))
                screen.blit(text, [screen_size[0] / 2 - (text.get_size()[0] / 2), 300])
            elif mode == "hard":
                text = font.render("Easy", True, (255, 255, 255))
                screen.blit(text, [screen_size[0] / 2 - (text.get_size()[0] / 2), 200])
                text = font.render("Hard", True, (255, 0, 0))
                screen.blit(text, [screen_size[0] / 2 - (text.get_size()[0] / 2), 300])
            elif mode == "quit":
                pygame.quit()
                quit()

            # update screen
            pygame.display.update()


def game_over():
    screen.fill((0, 0, 0))

    font = pygame.font.Font("8bit.ttf", 24)
    text = font.render("Game", True, (255, 255, 255))
    screen.blit(text, [(screen_size[0] / 2) - 50, (screen_size[1] / 2) - 30])
    text = font.render("Over", True, (255, 255, 255))
    screen.blit(text, [(screen_size[0] / 2) - 50, (screen_size[1] / 2) + block_size])
    pygame.display.update()
    pygame.time.wait(2000)

    show_highscores()


class Snake:
    global snake_length

    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_change = 0
        self.y_change = 0
        self.snake_list = []
        self.snake_length = snake_length
        self.snake_direction = "right"

    def move(self):
        self.x += self.x_change
        self.y += self.y_change
        self.snake_list.append([self.x, self.y])
        if len(self.snake_list) > self.snake_length:
            del self.snake_list[0]

    def change_direction(self, direction):
        if direction == "left" and self.snake_direction != "right":
            self.x_change = -block_size
            self.y_change = 0
            self.snake_direction = "left"
        elif direction == "right" and self.snake_direction != "left":
            self.x_change = block_size
            self.y_change = 0
            self.snake_direction = "right"
        elif direction == "up" and self.snake_direction != "down":
            self.x_change = 0
            self.y_change = -block_size
            self.snake_direction = "up"
        elif direction == "down" and self.snake_direction != "up":
            self.x_change = 0
            self.y_change = block_size
            self.snake_direction = "down"

    def draw(self, on_fire=False):

        if on_fire:
            for i in self.snake_list[0:-1]:
                screen.blit(fire_sprite, (i[0], i[1]))
        else:
            for i in self.snake_list[0:-1]:
                screen.blit(body_sprite, (i[0], i[1]))

        if self.snake_direction == "right":
            screen.blit(head_sprite, (self.x, self.y))
        elif self.snake_direction == "left":
            screen.blit(pygame.transform.flip(head_sprite, True, False), (self.x, self.y))
        elif self.snake_direction == "up":
            screen.blit(pygame.transform.rotate(head_sprite, 90), (self.x, self.y))
        elif self.snake_direction == "down":
            screen.blit(pygame.transform.rotate(head_sprite, 270), (self.x, self.y))

    def reset(self):
        self.x = pygame.display.get_surface().get_width() / 2
        self.y = pygame.display.get_surface().get_height() / 2
        self.snake_direction = "right"
        self.snake_list = []
        self.snake_length = snake_length

    def on_fire(self):
        self.snake_list.reverse()

        offset_x, offset_y = 0, 0

        if self.x < screen_size[0] / 2 and self.y < screen_size[1] / 2:
            offset_x = 0
            offset_y = -50

        if self.x > screen_size[0] / 2 and self.y < screen_size[1] / 2:
            offset_x = -200
            offset_y = -20

        if self.x < screen_size[0] / 2 and self.y > screen_size[1] / 2:
            offset_x = 0
            offset_y = -50

        if self.x > screen_size[0] / 2 and self.y > screen_size[1] / 2:
            offset_x = -200
            offset_y = -20

        for i in range(10):
            font = pygame.font.Font("8bit.ttf", 10)
            text = font.render("AHHH! I'M BURNING!", True, (255, 0, 0))
            screen.blit(text, [self.x + offset_x, self.y + offset_y])

            for i in self.snake_list:
                screen.blit(fire_sprite, (i[0], i[1]))
                pygame.display.update()
                pygame.time.wait(20)

                # do same thing, but with fire_sprite flipped horizontally
                screen.blit(pygame.transform.flip(fire_sprite, True, False), (i[0], i[1]))
                pygame.display.update()
                pygame.time.wait(20)

    def check_collision(self, target):
        if self.x == target.x and self.y == target.y:
            return True
        else:
            return False


class Food:
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self):
        screen.blit(apple_sprite, (self.x, self.y))

    def reset(self):
        self.x, self.y = random_number()


class Fire:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.frame = 0

    def draw(self):
        if self.frame == 0:
            screen.blit(fire_sprite, (self.x, self.y))
            self.frame = 1

        # flip the fire sprite horizontally
        elif self.frame == 1:
            screen.blit(pygame.transform.flip(fire_sprite, True, False), (self.x, self.y))
            self.frame = 0

    def reset(self):
        self.x, self.y = random_number()


def main(difficulty):
    global score

    snake = Snake()
    snake.x = (pygame.display.get_surface().get_width() / 2) - (block_size / 2)
    snake.y = (pygame.display.get_surface().get_height() / 2) - (block_size / 2)
    snake.x_change = block_size

    food = Food()
    food.reset()

    fires = []

    bg_color = random_color()

    score = 0

    # get current time
    start_time = time.time()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if snake.x_change != block_size:
                        snake.change_direction("left")

                elif event.key == pygame.K_RIGHT:
                    if snake.x_change != -block_size:
                        snake.change_direction("right")

                elif event.key == pygame.K_UP:
                    if snake.y_change != block_size:
                        snake.change_direction("up")

                elif event.key == pygame.K_DOWN:
                    if snake.y_change != -block_size:
                        snake.change_direction("down")

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # change background color
        screen.fill(bg_color)

        # put black rectangle at top of screen
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen_size[0], 40))

        snake.move()

        display_score()

        # calculate number of seconds since start of game
        seconds = int(time.time() - start_time)

        display_time(seconds)

        snake.draw()
        food.draw()

        if difficulty == "hard":
            fire = Fire()
            fire.reset()
            fires.append(fire)

            for f in fires:
                # if the fire is on the same position as the food, reset the fire
                if f.x == food.x and f.y == food.y:
                    f.reset()

            # remove random item in fires list and reset it
            if len(fires) > 5 and seconds % 5 == 0:
                random_fire = random.choice(fires)
                fires.remove(random_fire)
                random_fire.reset()

            for fire in fires:
                fire.draw()

            # Check for collision between snake and fire
            for fire in fires:
                if snake.check_collision(fire):
                    snake.on_fire()
                    snake.reset()
                    break

        # Detect collision with food
        if snake.x == food.x and snake.y == food.y:
            food.reset()
            snake.snake_length += 1
            score += block_size
            screen.fill((255, 255, 255))

        # Detect collision between head and body
        for i in snake.snake_list[0:-1]:
            if snake.x == i[0] and snake.y == i[1]:
                break

        # Detect collision with screen edges
        if snake.x < 0 or snake.x > screen_size[0] - block_size or snake.y < 40 or snake.y > screen_size[
            1] - block_size:
            break

        clock.tick(FPS)

        pygame.display.flip()

    game_over()


if __name__ == "__main__":
    while True: main(main_menu())
