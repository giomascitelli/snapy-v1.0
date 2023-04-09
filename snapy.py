import pygame
import random
import os
from collections import deque

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initializing pygame
pygame.init()


# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors used
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FONT = None

clock = pygame.time.Clock()

programIcon = pygame.image.load("assets/snapyicon.png")

pygame.display.set_icon(programIcon)

pygame.mixer.music.set_volume(0.3)


def game_over_screen(screen):

    pygame.mixer.init()
    sound_effect = pygame.mixer.Sound('assets/gameover.mp3')
    sound_effect.play()
    sound_effect.set_volume(0.3)
    pygame.mixer.music.stop()

    font = pygame.font.Font(None, 64)

    # Text creation
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    restart_text = font.render("Press R to restart or ESC to quit", True, (255, 0, 0))

    # Text dimensions
    game_over_text_rect = game_over_text.get_rect()
    restart_text_rect = restart_text.get_rect()

    # Text positions
    game_over_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    restart_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

    # Draw text
    screen.blit(game_over_text, game_over_text_rect)
    screen.blit(restart_text, restart_text_rect)

    # Update screen
    pygame.display.flip()

    # Wait for player to press R to restart or ESC to quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.music.load('assets/bg.mp3')
                    pygame.mixer.music.play(-1)
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False

# Menu function
def draw_menu(screen, menu_options, selected_option):
    screen.fill(BLACK)
    font = pygame.font.Font(FONT, 36)
    for i, option in enumerate(menu_options):
        text = font.render(option, True, WHITE if i == selected_option else GREEN)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + i * 50))
        screen.blit(text, text_rect)
    pygame.display.flip()

# Food generation function
def generate_food():
    x = random.randint(0, SCREEN_WIDTH - 10)
    y = random.randint(0, SCREEN_HEIGHT - 10)
    return (x // 10 * 10, y // 10 * 10)

# Snapy's body function
def update_snake(direction, snake_segments):
    head = snake_segments[-1]
    if direction == 'UP':
        new_head = (head[0], head[1] - 10)
    elif direction == 'DOWN':
        new_head = (head[0], head[1] + 10)
    elif direction == 'LEFT':
        new_head = (head[0] - 10, head[1])
    else:
        new_head = (head[0] + 10, head[1])
    snake_segments.append(new_head)
    return snake_segments

# Snapy function
def draw_segment(screen, color, x, y):
    pygame.draw.rect(screen, color, [x, y, 10, 10])

# Game loop function
def game_loop(screen):
    
    pygame.mixer.init()
    pygame.mixer.music.load('assets/bg.mp3')
    pygame.mixer.music.play(-1)
    
    snake_segments = deque([(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)])
    direction = 'RIGHT'
    score = 0
    game_over = False

    # Generate food position
    food_position = generate_food()

    # Event handling
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

        # Move snake
        snake_segments = update_snake(direction, snake_segments)

        # Check if snake collides with the wall
        head = snake_segments[-1]
        if head[0] < 0:
            head = (SCREEN_WIDTH, head[1])
        elif head[0] >= SCREEN_WIDTH:
            head = (0, head[1])
        elif head[1] < 0:
            head = (head[0], SCREEN_HEIGHT)
        elif head[1] >= SCREEN_HEIGHT:
            head = (head[0], 0)
        snake_segments[-1] = head

        # Check if snake collides with itself
        if len(set(snake_segments)) < len(snake_segments):
            game_over = True

        # Check if snake eats food
        if head == food_position:
            food_position = generate_food()
            score += 1
            pygame.mixer.init()
            sound_effect = pygame.mixer.Sound('assets/feed.mp3')
            sound_effect.set_volume(0.3)
            sound_effect.play()
        else:
            snake_segments.popleft()

        screen.fill(BLACK)

        # Draw snake
        for segment in snake_segments:
            draw_segment(screen, WHITE, segment[0], segment[1])

        # Draw food
        draw_segment(screen, YELLOW, food_position[0], food_position[1])

        # Draw score
        font = pygame.font.Font(FONT, 36)
        text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()

        # Check if game over
        if game_over:
            if game_over_screen(screen):
                snake_segments = deque([(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)])
                direction = 'RIGHT'
                score = 0
                game_over = False
                food_position = generate_food()
            else:
                pygame.quit()
                return

        clock.tick(10)

    game_over_screen(screen)

def start_game():
    # Start screen
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("snapy")

    # Menu options
    menu_options = ["Start", "Quit"]
    selected_option = 0

    # Load image
    image = pygame.image.load(os.path.join("assets/snapylogo.png"))

    # Image position and size
    image_rect = image.get_rect()
    image_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 126)

    # Draw menu
    draw_menu(screen, menu_options, selected_option)
    screen.blit(image, image_rect)

    # Event handling
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                    screen.fill(BLACK)
                    draw_menu(screen, menu_options, selected_option)
                    screen.blit(image, image_rect)
                    pygame.mixer.init()
                    sound_effect = pygame.mixer.Sound('assets/menu.mp3')
                    sound_effect.set_volume(0.3)
                    sound_effect.play()
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                    screen.fill(BLACK)
                    draw_menu(screen, menu_options, selected_option)
                    screen.blit(image, image_rect)
                    pygame.mixer.init()
                    sound_effect = pygame.mixer.Sound('assets/menu.mp3')
                    sound_effect.set_volume(0.3)
                    sound_effect.play()
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        pygame.mixer.init()
                        sound_effect = pygame.mixer.Sound('assets/start.mp3')
                        sound_effect.set_volume(0.3)
                        sound_effect.play()
                        pygame.time.delay(1000)
                        game_loop(screen)
                        screen.fill(BLACK)
                        draw_menu(screen, menu_options, selected_option)
                        screen.blit(image, image_rect)
                    else:
                        pygame.quit()
                        return

        pygame.display.flip()

start_game()
