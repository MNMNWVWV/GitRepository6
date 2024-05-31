# src/main.py
import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Brick Breaker")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 패들 설정
paddle = pygame.Rect(375, 550, 50, 10)

# 공 설정
ball = pygame.Rect(390, 540, 10, 10)
ball_dx = 3
ball_dy = -3

# 벽돌 설정
brick_rows = 5
brick_cols = 8
brick_offset_y = 100  # 벽돌의 y 위치를 아래로 이동시키기 위한 오프셋
bricks = [pygame.Rect(col * 100, row * 30 + brick_offset_y, 98, 28) for row in range(brick_rows) for col in range(brick_cols)]

# 점수와 생명 설정
score = 0
lives = 3
font = pygame.font.Font(None, 36)

# 파워업 설정
powerups = []
POWERUP_CHANCE = 0.1  # 파워업이 생성될 확률

# 게임 루프
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 패들 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= 5
    if keys[pygame.K_RIGHT] and paddle.right < 800:
        paddle.right += 5
    
    # 공 이동
    ball.left += ball_dx
    ball.top += ball_dy

    # 벽과 충돌 처리
    if ball.left <= 0 or ball.right >= 800:
        ball_dx = -ball_dx
    if ball.top <= 0:
        ball_dy = -ball_dy
    
    # 패들과 충돌 처리
    if ball.colliderect(paddle):
        ball_dy = -ball_dy

    # 벽돌과 충돌 처리
    for brick in bricks[:]:
        if ball.colliderect(brick):
            ball_dy = -ball_dy
            bricks.remove(brick)
            score += 10  # 점수 증가
            
            # 파워업 생성
            if random.random() < POWERUP_CHANCE:
                powerup = pygame.Rect(brick.left + brick.width // 2 - 10, brick.top + brick.height // 2 - 10, 20, 20)
                powerups.append(powerup)

    # 파워업 이동 및 충돌 처리
    for powerup in powerups[:]:
        powerup.top += 3
        if powerup.colliderect(paddle):
            powerups.remove(powerup)
            paddle.width += 20  # 패들 크기 증가
        elif powerup.top > 600:
            powerups.remove(powerup)

    # 공이 바닥에 닿았을 때 처리
    if ball.top >= 600:
        lives -= 1  # 생명 감소
        if lives == 0:
            running = False
        else:
            ball.left = 390
            ball.top = 540
            ball_dx = 3
            ball_dy = -3

    # 화면 그리기
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    for brick in bricks:
        pygame.draw.rect(screen, WHITE, brick)
    
    # 파워업 그리기
    for powerup in powerups:
        pygame.draw.rect(screen, GREEN, powerup)
    
    # 점수와 생명 표시
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (700, 10))
    
    pygame.display.flip()

    # 프레임 속도 조절
    pygame.time.delay(30)

# 게임 종료 처리
pygame.quit()
sys.exit()
