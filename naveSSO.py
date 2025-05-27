import pygame
import os
import random
import sys

# Inicializar pygame
pygame.init()

# Tamaño de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceMax Defender")

# Cargar imagen
def load_img(name, size=None):
    try:
        path = os.path.join("assets", "images", name)
        print(f"Cargando imagen: {path}")
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except Exception as e:
        print(f"Error cargando imagen '{path}': {e}")
        sys.exit()

# Cargar imágenes
background = load_img("background.png", size=(WIDTH, HEIGHT))
player_img = load_img("player.png", size=(64, 64))
bullet_img = load_img("bala.png", size=(10, 30))
enemy_imgs = [
    load_img("enemigo1.png", size=(60, 60)),
    load_img("enemigo2.png", size=(60, 60)),
    load_img("enemigo3.png", size=(60, 60)),
]
# Jugador
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 50))
player_speed = 5

# Balas
bullets = []
bullet_speed = -10

# Enemigos
enemies = []
enemy_speed = 2
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 1000)

# Reloj
clock = pygame.time.Clock()

# Fuente
font = pygame.font.SysFont("arial", 30)
score = 0

# Función para dibujar texto
def draw_text(text, x, y, color=(255, 255, 255)):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Bucle principal
running = True
while running:
    clock.tick(60)
    screen.blit(background, (0, 0))

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_ENEMY:
            enemy = random.choice(enemy_imgs)
            rect = enemy.get_rect(center=(random.randint(50, WIDTH - 50), -30))
            enemies.append((enemy, rect))

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:  # Máximo 5 balas en pantalla
            bullet_rect = bullet_img.get_rect(center=(player_rect.centerx, player_rect.top))
            bullets.append(bullet_rect)

    # Movimiento de balas
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Movimiento de enemigos
    for i, (enemy, rect) in enumerate(enemies[:]):
        rect.y += enemy_speed
        if rect.top > HEIGHT:
            enemies.remove((enemy, rect))

        # Colisión con balas
        for bullet in bullets[:]:
            if rect.colliderect(bullet):
                enemies.remove((enemy, rect))
                bullets.remove(bullet)
                score += 1
                break

    # Dibujar jugador
    screen.blit(player_img, player_rect)

    # Dibujar balas
    for bullet in bullets:
        screen.blit(bullet_img, bullet)

    # Dibujar enemigos
    for enemy, rect in enemies:
        screen.blit(enemy, rect)

    # Dibujar puntuación
    draw_text(f"Puntos: {score}", 10, 10)

    pygame.display.flip()

pygame.quit()
