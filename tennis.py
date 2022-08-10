import pygame
import random

WIDTH = 800
HEIGHT = 600
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Ball:
    def __init__(self):
        self.image = pygame.image.load("small_tennis.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.speed = [random.randrange(1,6), 3]
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed[1] *= -1
        elif self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed[0] *= -1
        self.move()

    def move(self):
        self.rect = self.rect.move(self.speed)

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(0, HEIGHT/2, 10, 60)
        self.rect.center = (self.rect.width/2, HEIGHT/2) 

def main():
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    ball = Ball()
    paddle = Paddle()

    def runEventLoop() -> bool:
        for event in pygame.event.get():
            match event.type:
                case pygame.MOUSEBUTTONDOWN:
                    if ball.rect.collidepoint(pygame.mouse.get_pos()):
                        ball.speed[0] = random.randrange(-4, 4)
                        ball.speed[1] = -2
                case pygame.QUIT:
                    return False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False

        keyState = pygame.key.get_pressed()
        if keyState[pygame.K_DOWN]:
            paddle.rect.centery += 5
        elif keyState[pygame.K_UP]:
            paddle.rect.centery -= 5
        
        return True


    b_run = True
    game_over = False
    game_over_timer = 60

    while b_run:
        screen.fill(BACKGROUND)

        if game_over:
            font = pygame.font.SysFont(None, 100)
            text = font.render("Game over", True, RED)
            screen.blit(text,(200,200))
            game_over_timer -= 1
            ball = None
            pygame.display.flip()
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = False
            b_run = runEventLoop()
            continue

        if not ball:
            ball = Ball()

        if ball.rect.colliderect(paddle.rect):
            ball.speed[1] *= -1
        elif ball.rect.left < 0:
            game_over = True
    
        screen.blit(ball.image, ball.rect)
        pygame.draw.rect(screen, WHITE, paddle.rect)
        ball.update()
        pygame.display.flip()
        clock.tick(60)
        b_run = runEventLoop()


if __name__ == "__main__":
    main()