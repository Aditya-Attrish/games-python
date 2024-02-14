import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 480, 510
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Snake class
class Snake:
    def __init__(self):
        self.headX = 360
        self.headY = 240
        self.Count = 3
        self.tailX = [270, 300, 330]
        self.tailY = [240, 240, 240]
        self.foodX = random.randint(0, 15) * 30
        self.foodY = random.randint(0, 15) * 30
        self.direction = "Right"
        self.game_over = False
        self.score = 0

    # Collision on border
    def collision(self):
        if self.headX >= WIDTH:
            self.headX = 0
        elif self.headX < 0:
            self.headX = WIDTH - 30
        elif self.headY < 0:
            self.headY = HEIGHT - 30
        elif self.headY >= HEIGHT:
            self.headY = 0

    def eat_food(self):
        if self.headX == self.foodX and self.headY == self.foodY:
            self.foodX = random.randint(0, 15) * 30
            self.foodY = random.randint(0, 15) * 30
            self.Count += 1
            self.tailX.append(0)
            self.tailY.append(550)
            self.score += 5

    def move(self):
        if not self.game_over:
            self.tailX = [self.headX] + self.tailX[:self.Count - 1]
            self.tailY = [self.headY] + self.tailY[:self.Count - 1]
            if self.direction == "Right":
                self.headX += 30
            elif self.direction == "Left":
                self.headX -= 30
            elif self.direction == "Up":
                self.headY -= 30
            elif self.direction == "Down":
                self.headY += 30
            self.eat_food()
            for i in range(self.Count):
                if self.headX == self.tailX[i] and self.headY == self.tailY[i]:
                    self.game_over = True
            self.collision()

    def draw(self, win):
        # Draw snake
        for i in range(self.Count):
            pygame.draw.rect(win, BLUE, (self.tailX[i], self.tailY[i], 30, 30))
        # Draw food
        pygame.draw.rect(win, YELLOW, (self.foodX, self.foodY, 30, 30))
        # Draw head
        pygame.draw.rect(win, RED, (self.headX, self.headY, 30, 30))
        # Draw score
        font = pygame.font.SysFont(None, 30)
        text = font.render("Score: " + str(self.score), True, WHITE)
        win.blit(text, (10, 10))

    def change_direction(self, x, y):
        if not self.game_over:
            head_center_x = self.headX + 15
            head_center_y = self.headY + 15
            if abs(x - head_center_x) > abs(y - head_center_y):
                if x > head_center_x and self.direction != "Left":
                    self.direction = "Right"
                elif x < head_center_x and self.direction != "Right":
                    self.direction = "Left"
            else:
                if y > head_center_y and self.direction != "Up":
                    self.direction = "Down"
                elif y < head_center_y and self.direction != "Down":
                    self.direction = "Up"

# Main function
def main():
    clock = pygame.time.Clock()
    snake = Snake()

    while not snake.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snake.game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    snake.change_direction(x, y)

        snake.move()
        WIN.fill(BLACK)
        snake.draw(WIN)
        pygame.display.update()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()