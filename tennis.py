import pygame
import csv
import pandas as pd # type: ignore
from sklearn.neighbors import KNeighborsRegressor # type: ignore
from typing import List

WIDTH = 800
HEIGHT = 600
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Ball:
    def __init__(self):
        self.image = pygame.image.load("small_tennis.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.speed = [1, 1]
        self.rect = self.image.get_rect()

    def update(self, *paddle_rects: List[pygame.Rect]):
        b_collision = False
        for r in paddle_rects:
            if self.rect.colliderect(r):
                b_collision = True
                break

        if b_collision:
            self.speed[0] *= -1
        elif self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed[1] *= -1
        elif self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed[0] *= -1
        self.move()

    def move(self):
        self.rect = self.rect.move(self.speed)

class Paddle:
    def __init__(self, left: bool):
        self.rect = pygame.Rect(0, HEIGHT/2, 10, 60)
        if left:
            self.rect.center = (self.rect.width//2, HEIGHT//2)
        else:
            self.rect.center = (WIDTH - self.rect.width//2, HEIGHT//2)

class Scene:
    def __init__(self, learn: bool):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.learn = learn
        self.cleanup()
        self.create()

    def cleanup(self):
        self.ball = None
        self.left_paddle = None
        self.right_paddle = None

    def create(self):
        if not self.ball:
            self.ball = Ball()
            self.left_paddle = Paddle(True)
            self.right_paddle = Paddle(False)

    def pumpEvents(self) -> bool:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False

        keyState = pygame.key.get_pressed()
        paddle = self.right_paddle
        if self.learn:
            paddle = self.left_paddle
        if keyState[pygame.K_DOWN]:
            paddle.rect.centery += 3
        elif keyState[pygame.K_UP]:
            paddle.rect.centery -= 3
        
        return True

    def game_over(self) -> bool:
        font = pygame.font.SysFont('arial', 100)
        text = font.render("Game over", True, RED)
        self.screen.blit(text,(150,200))
        self.cleanup()
        pygame.display.flip()
        self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    def play(self) -> None:
        b_run = True
        game_over = False

        columns = ['x', 'y', 'vx', 'vy', 'paddle.y']

        if self.learn:
            csv_file = open('tennis_data.csv', 'w')
            writer = csv.DictWriter(csv_file, columns)
            writer.writeheader()
        else:
            pong = pd.read_csv('tennis_data.csv')
            pong = pong.drop_duplicates()

            X = pong.drop(columns='paddle.y')
            y = pong['paddle.y']

            clf = KNeighborsRegressor(n_neighbors=3)
            clf.fit(X, y)

        while b_run:
            self.screen.fill(BACKGROUND)

            if game_over:
                game_over = self.game_over()
                b_run = self.pumpEvents()
                continue
            else:
                self.create()

            if self.ball.rect.left < 0 or (not self.learn and self.ball.rect.right > WIDTH):
                game_over = True
        

            values = [
                self.ball.rect.centerx, 
                self.ball.rect.centery,
                self.ball.speed[0],
                self.ball.speed[1],
                self.left_paddle.rect.centery
            ]

            if self.learn:
                writer.writerow(dict(zip(columns, values)))
            else:
                to_append = dict(zip(columns[:-1], values[:-1]))
                to_predict = pd.DataFrame([to_append], columns=columns[:-1])
                should_move = clf.predict(to_predict)
                distance = self.left_paddle.rect.centery - should_move[0]
                if distance > 0:
                    self.left_paddle.rect.centery -= 1
                elif distance < 0:
                    self.left_paddle.rect.centery += 1

            self.screen.blit(self.ball.image, self.ball.rect)
            pygame.draw.rect(self.screen, WHITE, self.left_paddle.rect)
            pygame.draw.rect(self.screen, WHITE, self.right_paddle.rect)
            if self.learn:
                self.ball.update(self.left_paddle.rect)
            else:
                self.ball.update(self.left_paddle.rect, self.right_paddle.rect)

            pygame.display.flip()
            self.clock.tick(240)
            b_run = self.pumpEvents()

def main():
    scene = Scene(False)
    scene.play()

if __name__ == "__main__":
    main()