import pygame
import random
import math

pygame.init()

# =========================
# SCREEN SETTINGS
# =========================
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Target Shooter 🤖🔫")

clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 70)

# =========================
# COLORS
# =========================
WHITE = (255, 255, 255)
BLACK = (15, 15, 20)
RED = (220, 50, 50)
GREEN = (50, 220, 100)
BLUE = (50, 150, 255)
YELLOW = (255, 220, 50)
GRAY = (100, 100, 100)

# =========================
# PLAYER
# =========================
player = {
    "x": WIDTH // 2,
    "y": HEIGHT - 100,
    "size": 40,
    "speed": 6,
    "health": 100
}

# =========================
# GAME DATA
# =========================
bullets = []
enemies = []

score = 0
game_over = False
spawn_timer = 0


# =========================
# CREATE ENEMY
# =========================
def create_enemy():
    return {
        "x": random.randint(40, WIDTH - 40),
        "y": random.randint(50, 200),
        "size": random.randint(30, 50),
        "speed": random.uniform(1.2, 2.5) + score * 0.02,
        "direction": random.choice([-1, 1])
    }


# =========================
# SHOOT BULLET
# =========================
def shoot():
    bullets.append({
        "x": player["x"],
        "y": player["y"] - 30,
        "speed": 10
    })


# =========================
# DRAW PLAYER
# =========================
def draw_player():
    x = player["x"]
    y = player["y"]

    # Body
    pygame.draw.rect(
        screen,
        BLUE,
        (x - 20, y - 20, 40, 40),
        border_radius=8
    )

    # Gun
    pygame.draw.rect(
        screen,
        GRAY,
        (x - 5, y - 40, 10, 30)
    )

    # AI glow
    pygame.draw.circle(screen, YELLOW, (x, y), 6)


# =========================
# DRAW ENEMY
# =========================
def draw_enemy(enemy):
    pygame.draw.circle(
        screen,
        RED,
        (int(enemy["x"]), int(enemy["y"])),
        enemy["size"] // 2
    )

    # Enemy eyes
    pygame.draw.circle(
        screen,
        WHITE,
        (int(enemy["x"] - 8), int(enemy["y"] - 5)),
        5
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (int(enemy["x"] + 8), int(enemy["y"] - 5)),
        5
    )


# =========================
# DRAW UI
# =========================
def draw_ui():
    score_text = font.render(f"Score: {score}", True, WHITE)
    health_text = font.render(
        f"Health: {player['health']}",
        True,
        GREEN if player["health"] > 30 else RED
    )

    screen.blit(score_text, (20, 20))
    screen.blit(health_text, (20, 60))


# =========================
# MAIN GAME LOOP
# =========================
running = True

while running:

    clock.tick(60)

    # Background
    screen.fill(BLACK)

    # =====================
    # EVENTS
    # =====================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if not game_over:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    shoot()

        else:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    # Restart
                    player["health"] = 100
                    player["x"] = WIDTH // 2
                    player["y"] = HEIGHT - 100

                    bullets.clear()
                    enemies.clear()

                    score = 0
                    game_over = False

    # =====================
    # GAME LOGIC
    # =====================
    if not game_over:

        # Player Movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player["x"] -= player["speed"]

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player["x"] += player["speed"]

        player["x"] = max(30, min(WIDTH - 30, player["x"]))

        # =====================
        # BULLETS
        # =====================
        for bullet in bullets[:]:

            bullet["y"] -= bullet["speed"]

            pygame.draw.rect(
                screen,
                YELLOW,
                (bullet["x"] - 3, bullet["y"], 6, 15)
            )

            if bullet["y"] < 0:
                bullets.remove(bullet)

        # =====================
        # SPAWN ENEMIES
        # =====================
        spawn_timer += 1

        spawn_rate = max(20, 70 - score)

        if spawn_timer >= spawn_rate:

            enemies.append(create_enemy())

            spawn_timer = 0

        # =====================
        # AI ENEMY MOVEMENT
        # =====================
        for enemy in enemies[:]:

            # AI TRACKS PLAYER
            if enemy["x"] < player["x"]:
                enemy["x"] += enemy["speed"]
            else:
                enemy["x"] -= enemy["speed"]

            # Move downward
            enemy["y"] += enemy["speed"] * 0.7

            draw_enemy(enemy)

            # Collision with player
            distance = math.sqrt(
                (enemy["x"] - player["x"]) ** 2 + 
                (enemy["y"] - player["y"]) ** 2
            )

            if distance < enemy["size"]:

                player["health"] -= 20

                enemies.remove(enemy)

                if player["health"] <= 0:
                    game_over = True

                continue

            # =====================
            # BULLET COLLISION
            # =====================
            for bullet in bullets[:]:

                distance = math.sqrt(
                    (enemy["x"] - bullet["x"]) ** 2 + 
                    (enemy["y"] - bullet["y"]) ** 2
                )

                if distance < enemy["size"] / 2 + 10:

                    if bullet in bullets:
                        bullets.remove(bullet)

                    if enemy in enemies:
                        enemies.remove(enemy)

                    score += 10

                    break

        # Draw player
        draw_player()

        # Draw UI
        draw_ui()

        # Instructions
        instruction = font.render(
            "A/D or Arrow Keys = Move | SPACE = Shoot",
            True,
            GRAY
        )

        screen.blit(
            instruction,
            (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 40)
        )

    # =====================
    # GAME OVER SCREEN
    # =====================
    else:

        game_over_text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        score_text = font.render(
            f"Final Score: {score}",
            True,
            WHITE
        )

        restart_text = font.render(
            "Press R to Restart",
            True,
            YELLOW
        )

        screen.blit(
            game_over_text,
            (
                WIDTH // 2 - game_over_text.get_width() // 2,
                HEIGHT // 2 - 100
            )
        )

        screen.blit(
            score_text,
            (
                WIDTH // 2 - score_text.get_width() // 2,
                HEIGHT // 2
            )
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                HEIGHT // 2 + 60
            )
        )

    pygame.display.update()

pygame.quit()
