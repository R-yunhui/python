import pygame
import random

# 初始化Pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 设置游戏窗口
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# 设置游戏时钟
clock = pygame.time.Clock()

# 蛇的属性
SNAKE_BLOCK_SIZE = 20
SNAKE_SPEED = 15

# 定义字体
font = pygame.font.SysFont('simhei', 30)

def display_score(score):
    score_text = font.render(f"Score: {score}", True, BLUE)
    window.blit(score_text, [10, 10])

def draw_snake(snake_block_size, snake_body):
    for pos in snake_body:
        pygame.draw.rect(window, GREEN, [pos[0], pos[1], snake_block_size, snake_block_size])

def game_main_loop():
    game_over = False
    game_exit = False
    
    # 蛇的初始位置
    x = WIDTH / 2
    y = HEIGHT / 2
    
    # 蛇的移动方向
    x_change = 0
    y_change = 0
    
    # 蛇身体
    snake_body = []
    snake_length = 1
    
    # 食物位置
    food_x = round(random.randrange(0, WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
    
    # 游戏循环
    while not game_exit:
        
        # 游戏结束界面
        while game_over:
            window.fill(WHITE)
            game_over_text = font.render("Game Over! Press Q to Quit or C to Play Again", True, RED)
            window.blit(game_over_text, [WIDTH/2 - 280, HEIGHT/2])
            display_score(snake_length - 1)
            pygame.display.update()
            
            # 检测游戏结束后的按键
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        game_main_loop()
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change != SNAKE_BLOCK_SIZE:
                    x_change = -SNAKE_BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change != -SNAKE_BLOCK_SIZE:
                    x_change = SNAKE_BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change != SNAKE_BLOCK_SIZE:
                    y_change = -SNAKE_BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change != -SNAKE_BLOCK_SIZE:
                    y_change = SNAKE_BLOCK_SIZE
                    x_change = 0
        
        # 检查蛇是否撞墙
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_over = True
        
        # 更新蛇的位置
        x += x_change
        y += y_change
        
        # 清空屏幕
        window.fill(BLACK)
        
        # 画食物
        pygame.draw.rect(window, RED, [food_x, food_y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])
        
        # 更新蛇身体
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_body.append(snake_head)
        
        # 确保蛇身体长度正确
        if len(snake_body) > snake_length:
            del snake_body[0]
        
        # 检查蛇是否撞到自己
        for segment in snake_body[:-1]:
            if segment == snake_head:
                game_over = True
        
        # 画蛇
        draw_snake(SNAKE_BLOCK_SIZE, snake_body)
        
        # 显示分数
        display_score(snake_length - 1)
        
        # 更新屏幕
        pygame.display.update()
        
        # 检查是否吃到食物
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
            snake_length += 1
        
        # 控制游戏速度
        clock.tick(SNAKE_SPEED)
    
    # 退出游戏
    pygame.quit()
    quit()

# 启动游戏
if __name__ == "__main__":
    game_main_loop() 