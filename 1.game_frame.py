import pygame
import random
import sys

# 초기화
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🔥 Rengoku's Yaiba 🔥")
clock = pygame.time.Clock()

# 이미지 로드
background = pygame.image.load("./image/background.png")
rengoku_img = pygame.image.load("./image/rengoku.png")
oni_img = pygame.image.load("./image/akaza.png")
sword_img = pygame.image.load("./image/sword.png")
heart_img = pygame.image.load("./image/heart.png")

# 효과음 로드
eat_sound = pygame.mixer.Sound("./sound/umai.wav")
kill_sounds = [
    pygame.mixer.Sound("./sound/firebreath.wav"),
    pygame.mixer.Sound("./sound/knife.wav"),
    pygame.mixer.Sound("./sound/responsibility.wav"),
    pygame.mixer.Sound("./sound/responsibility2.wav")
]
gameover_sound = pygame.mixer.Sound("./sound/kokoro.wav")

# 볼륨 조절
eat_sound.set_volume(0.7)
for k in kill_sounds:
    k.set_volume(0.8)
gameover_sound.set_volume(0.7)

# 여러 음식 이미지
food_paths = [
    "./image/food1.png",
    "./image/food2.png",
    "./image/food3.png"
]

# 이미지 크기 조절
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
rengoku_img = pygame.transform.scale(rengoku_img, (60, 80))
oni_img = pygame.transform.scale(oni_img, (50, 60))
heart_img = pygame.transform.scale(heart_img, (30, 30))

# 글꼴
font = pygame.font.Font("./fonts/Galmuri14.ttf", 30)
big_font = pygame.font.Font("./fonts/Galmuri11.ttf", 40) 

# 클래스 
class Rengoku:
    def __init__(self):
        self.image = rengoku_img
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-100))
        self.speed = 6

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

class Food:
    def __init__(self):
        chosen_path = random.choice(food_paths)
        self.image = pygame.image.load(chosen_path)
        self.image = pygame.transform.scale(self.image, (36, 36))
        self.rect = self.image.get_rect(topleft=(random.randint(0, SCREEN_WIDTH-36), -36))
        self.speed = random.randint(3, 6)

    def fall(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = -36
            self.rect.x = random.randint(0, SCREEN_WIDTH-36)

    def draw(self):
        screen.blit(self.image, self.rect)

class Oni:
    def __init__(self):
        self.image = oni_img
        self.rect = self.image.get_rect(topleft=(random.randint(0, SCREEN_WIDTH-50), random.randint(-400,-50)))
        self.speed = random.randint(2,5)

    def fall(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = random.randint(-400,-50)
            self.rect.x = random.randint(0, SCREEN_WIDTH-50)

    def draw(self):
        screen.blit(self.image, self.rect)

class Sword:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(sword_img, (60, 80))
        self.rect = self.image.get_rect(center=(x, y-20))
        self.speed = 12

    def move(self):
        self.rect.y -= self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

# 객체 생성
rengoku = Rengoku()
foods = [Food() for _ in range(3)]
onis = [Oni() for _ in range(1)]
swords = []

score = 0
lives = 3
game_over = False

# 게임 루프
running = True
while running:
    clock.tick(60)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                swords.append(Sword(rengoku.rect.centerx, rengoku.rect.top))
            if event.key == pygame.K_r and game_over:
                # 초기화
                rengoku = Rengoku()
                foods = [Food() for _ in range(3)]
                onis = [Oni() for _ in range(1)]
                swords = []
                score = 0
                lives = 3
                game_over = False

    if not game_over:
        # 이동
        rengoku.move()
        for f in foods:
            f.fall()
        for o in onis:
            o.fall()
        for s in swords[:]:
            s.move()
            if s.rect.bottom < 0:
                swords.remove(s)

        # 충돌 처리
        for f in foods[:]:
            if rengoku.rect.colliderect(f.rect):
                score += 10
                lives = min(lives+1, 3)
                f.rect.y = -36
                f.rect.x = random.randint(0, SCREEN_WIDTH-36)
                eat_sound.play()  # 음식 먹을 때 효과음

        for s in swords[:]:
            for o in onis:
                if s.rect.colliderect(o.rect):
                    score += 20
                    swords.remove(s)
                    o.rect.y = random.randint(-400,-50)
                    o.rect.x = random.randint(0, SCREEN_WIDTH-50)
                    random.choice(kill_sounds).play()  # 오니 베었을 때 효과음
                    break

        for o in onis:
            if rengoku.rect.colliderect(o.rect):
                lives -= 1
                o.rect.y = random.randint(-400,-50)
                o.rect.x = random.randint(0, SCREEN_WIDTH-50)
                if lives <= 0:
                    game_over = True
                    gameover_sound.play()  # GAME OVER 효과음

        # 화면 그리기
        screen.blit(background, (0,0))
        rengoku.draw()
        for f in foods:
            f.draw()
        for o in onis:
            o.draw()
        for s in swords:
            s.draw()

        # 점수/목숨 표시
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10,10))
        for i in range(lives):
            screen.blit(heart_img, (10 + i*35, 50))

    else:
        # 게임 오버 
        screen.blit(background, (0,0))
        over_text = big_font.render("GAME OVER", True, (255,50,50))
        retry_text = font.render("Press R to Retry", True, (255,255,255))
        screen.blit(over_text, (70,250))
        screen.blit(retry_text, (130,350))

    pygame.display.update()
