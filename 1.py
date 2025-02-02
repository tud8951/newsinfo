import pygame
import random

# 初始化 Pygame
pygame.init()

# 屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 颜色定义
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

# 创建屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("打砖块游戏 - 生命值与复杂砖块")

# 字体
font = pygame.font.Font(None, 36)

# 挡板属性
paddle_width = 500
paddle_height = 20
paddle_x = (SCREEN_WIDTH - paddle_width) // 2
paddle_y = SCREEN_HEIGHT - 50

# 球属性
ball_radius = 15
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed_x = 5 * random.choice([-1, 1])
ball_speed_y = -5

# 拖尾特效属性
trail_length = 20  # 拖尾长度
trail_positions = []  # 存储小球的历史位置

# 砖块属性
brick_width = 75
brick_height = 30
brick_rows = 5
brick_cols = 10
bricks = []

# 分数、关卡和生命值
score = 0
level = 1
lives = 3

# 创建砖块
def create_bricks():
    bricks.clear()
    colors = [RED, GREEN, BLUE, YELLOW, ORANGE]
    for row in range(brick_rows + level - 1):  # 每关增加一行砖块
        for col in range(brick_cols):
            brick_x = col * (brick_width + 5) + 30
            brick_y = row * (brick_height + 5) + 50
            color = random.choice(colors)
            health = random.randint(1, 3)  # 砖块需要击中的次数
            bricks.append({"rect": pygame.Rect(brick_x, brick_y, brick_width, brick_height), "color": color, "health": health})

create_bricks()

# 游戏主循环
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取鼠标位置
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # 根据鼠标位置调整挡板位置
    paddle_x = mouse_x - paddle_width // 2

    # 确保挡板不超出屏幕边界
    if paddle_x < 0:
        paddle_x = 0
    elif paddle_x > SCREEN_WIDTH - paddle_width:
        paddle_x = SCREEN_WIDTH - paddle_width

    # 球移动
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # 记录小球的历史位置
    trail_positions.append((ball_x, ball_y))
    if len(trail_positions) > trail_length:
        trail_positions.pop(0)

    # 球与墙碰撞检测
    if ball_x <= 0 or ball_x >= SCREEN_WIDTH:
        ball_speed_x *= -1
    if ball_y <= 0:
        ball_speed_y *= -1

    # 球与挡板碰撞检测
    if (
        paddle_x < ball_x < paddle_x + paddle_width
        and paddle_y < ball_y + ball_radius < paddle_y + paddle_height
    ):
        ball_speed_y *= -1

    # 球与砖块碰撞检测
    brick_to_remove = None
    for brick in bricks:
        if brick["rect"].collidepoint(ball_x, ball_y):
            brick["health"] -= 1
            if brick["health"] == 0:
                brick_to_remove = brick
            ball_speed_y *= -1
            break

    # 移除健康值为0的砖块
    if brick_to_remove:
        bricks.remove(brick_to_remove)
        score += 10  # 每击碎一个砖块得 10 分

    # 如果所有砖块被击碎，进入下一关
    if not bricks:
        level += 1
        create_bricks()
        ball_x = SCREEN_WIDTH // 2
        ball_y = SCREEN_HEIGHT // 2
        ball_speed_x = 5 * random.choice([-1, 1])
        ball_speed_y = -5

    # 球掉出屏幕，生命值减 1
    if ball_y >= SCREEN_HEIGHT:
        lives -= 1
        if lives == 0:
            print(f"游戏结束！你的得分是: {score}")
            running = False
        else:
            # 重置球的位置
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 2
            ball_speed_x = 5 * random.choice([-1, 1])
            ball_speed_y = -5

    # 清屏
    screen.fill(BLACK)

    # 绘制拖尾
    for i, pos in enumerate(trail_positions):
        alpha = 255 - (i / trail_length) * 255  # 计算透明度
        color = (255, 0, 0, alpha)  # 使用红色并设置透明度
        pygame.draw.circle(screen, color, pos, ball_radius)

    # 绘制挡板
    pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y, paddle_width, paddle_height))

    # 绘制球
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

    # 绘制砖块
    for brick in bricks:
        pygame.draw.rect(screen, brick["color"], brick["rect"])

    # 显示分数
    score_text = font.render(f"分数: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

    # 显示关卡
    level_text = font.render(f"关卡: {level}", True, WHITE)
    screen.blit(level_text, (10, 10))

    # 显示生命值
    lives_text = font.render(f"生命: {lives}", True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - 150, 50))

    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 退出游戏
pygame.quit()