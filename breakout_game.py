import pygame
import math
import sys
import random

# 게임 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("블럭 깨기 게임 (Breakout)")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PINK = (255, 105, 180)
ORANGE = (255, 165, 0)

# 시계 및 FPS 설정
clock = pygame.time.Clock()
FPS = 60

# 폰트 설정
font_small = pygame.font.Font(None, 24)
font_large = pygame.font.Font(None, 48)


class Paddle:
    """게임 패들 클래스"""
    def __init__(self, x, y, width=300, height=15):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            self.rect.x = self.x

    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            self.rect.x = self.x

    def draw(self, surface):
        pygame.draw.rect(surface, CYAN, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)


class Ball:
    """게임 공 클래스"""
    def __init__(self, x, y, radius=8):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = 5
        self.speed_y = -5
        self.rect = pygame.Rect(self.x - radius, self.y - radius, 2 * radius, 2 * radius)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def bounce_x(self):
        self.speed_x *= -1

    def bounce_y(self):
        self.speed_y *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius)

    def reset(self, paddle):
        """공을 패들 위에 리셋"""
        self.x = paddle.x + paddle.width // 2
        self.y = paddle.y - self.radius - 10
        self.speed_x = 5
        self.speed_y = -5


class Item:
    """아이템 클래스 (총알 무기 획득)"""
    def __init__(self, x, y, width=15, height=15):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 3
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, surface):
        pygame.draw.rect(surface, ORANGE, self.rect)
        pygame.draw.rect(surface, YELLOW, self.rect, 2)

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT


class Bullet:
    """총알 클래스"""
    def __init__(self, x, y, speed=10):
        self.x = x
        self.y = y
        self.width = 3
        self.height = 15
        self.speed = speed
        self.rect = pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)

    def move(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 1)

    def is_off_screen(self):
        return self.y < 0


class Brick:
    """블럭 클래스"""
    def __init__(self, x, y, width=75, height=15, color=RED, health=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.health = health
        self.max_health = health
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        # 내구도에 따라 색상 변경
        brightness = int(200 + 55 * (self.health / self.max_health))
        color = tuple(min(c, brightness) for c in self.color)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 1)

    def hit(self):
        """블럭이 맞음"""
        self.health -= 1
        return self.health <= 0


class BrickBreaker:
    """블럭깨기 게임 메인 클래스"""
    def __init__(self):
        self.paddle = Paddle(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 50)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.bricks = []
        self.items = []
        self.bullets = []
        self.score = 0
        self.level = 1
        self.game_over = False
        self.game_won = False
        self.ball_in_play = False
        self.has_weapon = False
        self.create_bricks()

    def create_bricks(self):
        """블럭 생성"""
        self.bricks = []
        colors = [RED, YELLOW, GREEN, BLUE, PINK]
        brick_width = 75
        brick_height = 15
        spacing = 10
        start_x = 30
        start_y = 50
        rows = 3 + self.level
        cols = 8

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (brick_width + spacing)
                y = start_y + row * (brick_height + spacing)
                
                # 건강도는 줄 번호에 따라 증가
                health = 1 + row // 3
                color = colors[row % len(colors)]
                brick = Brick(x, y, brick_width, brick_height, color, health)
                self.bricks.append(brick)

    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    if self.has_weapon:
                        # 총알 발사
                        bullet = Bullet(self.paddle.x + self.paddle.width // 2, self.paddle.y - 20)
                        self.bullets.append(bullet)
                    elif not self.ball_in_play:
                        self.ball_in_play = True
                        self.ball.speed_y = -5

        # 패들 조작
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move_left()
        if keys[pygame.K_RIGHT]:
            self.paddle.move_right()

        return True

    def update(self):
        """게임 상태 업데이트"""
        if self.game_over or self.game_won:
            return

        # 공이 발사되지 않았으면 패들을 따라가게
        if not self.ball_in_play:
            self.ball.x = self.paddle.x + self.paddle.width // 2
            self.ball.y = self.paddle.y - self.ball.radius - 10
        else:
            # 공 이동
            self.ball.move()

            # 화면 경계 충돌
            if self.ball.x - self.ball.radius <= 0 or self.ball.x + self.ball.radius >= SCREEN_WIDTH:
                self.ball.bounce_x()
                self.ball.x = max(self.ball.radius, min(SCREEN_WIDTH - self.ball.radius, self.ball.x))

            if self.ball.y - self.ball.radius <= 0:
                self.ball.bounce_y()
                self.ball.y = self.ball.radius

            # 공이 화면 아래로 떨어지면 게임 오버
            if self.ball.y > SCREEN_HEIGHT:
                self.game_over = True
                return

            # 패들과의 충돌
            if self.ball.rect.colliderect(self.paddle.rect):
                if self.ball.speed_y > 0:
                    self.ball.bounce_y()
                    self.ball.y = self.paddle.y - self.ball.radius
                    
                    # 패들의 위치에 따라 공의 각도 조정
                    hit_pos = (self.ball.x - self.paddle.x) / self.paddle.width
                    hit_pos = max(0.1, min(0.9, hit_pos))
                    angle = (hit_pos - 0.5) * 100
                    self.ball.speed_x = angle / 20

            # 블럭과의 충돌
            for brick in self.bricks[:]:
                if self.ball.rect.colliderect(brick.rect):
                    brick.hit()
                    self.score += 10
                    
                    if brick.health <= 0:
                        self.bricks.remove(brick)
                        self.score += 50
                        
                        # 30% 확률로 아이템 드롭
                        if random.random() < 0.3:
                            item = Item(brick.x + brick.width // 2 - 7, brick.y + brick.height)
                            self.items.append(item)

                    # 공의 이동 방향에 따라 어느 쪽에서 맞았는지 판단
                    # 상/하 충돌
                    if abs(self.ball.y - brick.rect.centery) < abs(self.ball.x - brick.rect.centerx):
                        self.ball.bounce_y()
                        self.ball.y = brick.rect.top if self.ball.speed_y > 0 else brick.rect.bottom
                    # 좌/우 충돌
                    else:
                        self.ball.bounce_x()
                        self.ball.x = brick.rect.left if self.ball.speed_x > 0 else brick.rect.right
                    break

        # 아이템 업데이트
        for item in self.items[:]:
            item.move()
            
            # 패들과의 충돌 (아이템 획득)
            if item.rect.colliderect(self.paddle.rect):
                self.items.remove(item)
                self.has_weapon = True
                self.score += 100
            # 화면 밖으로 나감
            elif item.is_off_screen():
                self.items.remove(item)

        # 총알 업데이트
        for bullet in self.bullets[:]:
            bullet.move()
            
            # 블럭과의 충돌
            hit = False
            for brick in self.bricks[:]:
                if bullet.rect.colliderect(brick.rect):
                    if brick.hit():
                        self.bricks.remove(brick)
                        self.score += 50
                    hit = True
                    break
            
            if hit:
                self.bullets.remove(bullet)
            # 화면 밖으로 나감
            elif bullet.is_off_screen():
                self.bullets.remove(bullet)

        # 모든 블럭이 사라지면 승리
        if len(self.bricks) == 0:
            self.game_won = True

    def draw(self, surface):
        """화면에 그리기"""
        surface.fill(BLACK)

        # 점수 및 레벨 표시
        score_text = font_small.render(f"Score: {self.score}", True, WHITE)
        level_text = font_small.render(f"Level: {self.level}", True, WHITE)
        bricks_text = font_small.render(f"Bricks: {len(self.bricks)}", True, WHITE)
        weapon_text = font_small.render(f"Weapon: {'ON' if self.has_weapon else 'OFF'}", True, GREEN if self.has_weapon else RED)
        surface.blit(score_text, (10, 10))
        surface.blit(level_text, (10, 35))
        surface.blit(bricks_text, (10, 60))
        surface.blit(weapon_text, (10, 85))

        # 게임이 시작되지 않았으면 안내 메시지
        if not self.ball_in_play and not self.game_over and not self.game_won:
            start_text = font_small.render("Press SPACE to start", True, GREEN)
            surface.blit(start_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))

        # 블럭 그리기
        for brick in self.bricks:
            brick.draw(surface)

        # 아이템 그리기
        for item in self.items:
            item.draw(surface)

        # 총알 그리기
        for bullet in self.bullets:
            bullet.draw(surface)

        # 패들 그리기
        self.paddle.draw(surface)

        # 공 그리기
        self.ball.draw(surface)

        # 게임 오버 메시지
        if self.game_over:
            over_text = font_large.render("GAME OVER", True, RED)
            restart_text = font_small.render("Press R to restart or ESC to quit", True, WHITE)
            surface.blit(over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            surface.blit(restart_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 30))

        # 게임 승리 메시지
        if self.game_won:
            win_text = font_large.render("YOU WIN!", True, GREEN)
            next_text = font_small.render("Press N for next level or ESC to quit", True, WHITE)
            surface.blit(win_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 50))
            surface.blit(next_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 30))

    def next_level(self):
        """다음 레벨로 이동"""
        self.level += 1
        self.ball_in_play = False
        self.game_won = False
        self.has_weapon = False
        self.items = []
        self.bullets = []
        self.create_bricks()
        self.paddle = Paddle(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 50)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

    def restart(self):
        """게임 재시작"""
        self.level = 1
        self.score = 0
        self.ball_in_play = False
        self.game_over = False
        self.game_won = False
        self.has_weapon = False
        self.items = []
        self.bullets = []
        self.paddle = Paddle(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 50)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.create_bricks()


def main():
    """메인 게임 루프"""
    game = BrickBreaker()
    running = True

    while running:
        # 이벤트 처리
        running = game.handle_events()

        # 게임 상태별 키 입력 처리
        keys = pygame.key.get_pressed()
        if game.game_over and keys[pygame.K_r]:
            game.restart()
        elif game.game_won and keys[pygame.K_n]:
            game.next_level()

        # 게임 업데이트
        game.update()

        # 화면에 그리기
        game.draw(screen)
        pygame.display.flip()

        # FPS 설정
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
