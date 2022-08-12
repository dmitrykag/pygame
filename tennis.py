import pygame

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

    def update(self, paddle_rect: pygame.Rect):
        if self.rect.colliderect(paddle_rect):
            self.speed[0] *= -1
        elif self.rect.top < 0 or self.rect.bottom > HEIGHT:
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

class Scene:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.cleanup()
        self.create()

    def cleanup(self):
        self.ball = None
        self.paddle = None

    def create(self):
        if not self.ball:
            self.ball = Ball()
            self.paddle = Paddle()

    def pumpEvents(self) -> bool:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False

        keyState = pygame.key.get_pressed()
        if keyState[pygame.K_DOWN]:
            self.paddle.rect.centery += 3
        elif keyState[pygame.K_UP]:
            self.paddle.rect.centery -= 3
        
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
        while b_run:
            self.screen.fill(BACKGROUND)

            if game_over:
                game_over = self.game_over()
                b_run = self.pumpEvents()
                continue
            else:
                self.create()

            if self.ball.rect.left < 0:
                game_over = True
        
            self.screen.blit(self.ball.image, self.ball.rect)
            pygame.draw.rect(self.screen, WHITE, self.paddle.rect)
            self.ball.update(self.paddle.rect)
            pygame.display.flip()
            self.clock.tick(240)
            b_run = self.pumpEvents()

def main():
    scene = Scene()
    scene.play()

if __name__ == "__main__":
    main()