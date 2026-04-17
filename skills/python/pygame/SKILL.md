---
name: python-pygame
description: >
  Pygame patterns for 2D game development.
  Trigger: When building games with Pygame, game loops, sprites, collision detection, input handling.
metadata:
  author: gentleman-ai
  version: "1.0"
---

## Pygame Initialization (REQUIRED)

```python
import pygame
from pygame.locals import *

pygame.init()

# Display setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Clock for FPS control
clock = pygame.time.Clock()
FPS = 60

def main():
    running = True
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        # Game logic (update)
        
        # Render
        screen.fill(BLACK)
        pygame.display.flip()
        
        # FPS control
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
```

---

## Game Loop Pattern (REQUIRED)

```python
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.all_sprites = pygame.sprite.Group()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                self.handle_keydown(event.key)
    
    def update(self, dt):
        """Update game state. dt = delta time in seconds"""
        self.all_sprites.update(dt)
    
    def render(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            self.handle_events()
            self.update(dt)
            self.render()
        pygame.quit()
```

---

## Sprites (REQUIRED)

```python
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 255, 0))  # Green
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 300  # pixels per second
    
    def update(self, dt):
        """dt = delta time in seconds"""
        keys = pygame.key.get_pressed()
        
        if keys[K_LEFT]:
            self.rect.x -= self.speed * dt
        if keys[K_RIGHT]:
            self.rect.x += self.speed * dt
        if keys[K_UP]:
            self.rect.y -= self.speed * dt
        if keys[K_DOWN]:
            self.rect.y += self.speed * dt
        
        # Keep in bounds
        screen = pygame.display.get_surface()
        self.rect.clamp_ip(screen.get_rect())
```

---

## Collision Detection

```python
# ✅ Simple rectangle collision
if player.rect.colliderect(enemy.rect):
    print("Collision!")

# ✅ Sprite group collision
collisions = pygame.sprite.spritecollide(
    player,          # The sprite to check
    enemies,         # Group to check against
    dokill=True      # Remove collided sprites from group
)

# Use for power-ups, bullets hitting enemies
for enemy in collisions:
    player.score += 10

# ✅ Group vs group collision
hits = pygame.sprite.groupcollide(
    bullets,    # Group 1
    enemies,    # Group 2
    dokilla=True,   # Remove from group 1
    dokillb=True    # Remove from group 2
)
```

---

## Input Handling

```python
# ✅ Continuous input (movement)
def handle_input(self):
    keys = pygame.key.get_pressed()
    self.player.velocity.x = 0
    self.player.velocity.y = 0
    
    if keys[K_LEFT] or keys[K_a]:
        self.player.velocity.x = -self.player.speed
    if keys[K_RIGHT] or keys[K_d]:
        self.player.velocity.x = self.player.speed
    if keys[K_UP] or keys[K_w]:
        self.player.velocity.y = -self.player.speed
    if keys[K_DOWN] or keys[K_s]:
        self.player.velocity.y = self.player.speed

# ✅ One-time input (actions)
for event in pygame.event.get():
    if event.type == KEYDOWN:
        if event.key == K_SPACE:
            self.player.jump()
        elif event.key == K_ESCAPE:
            self.pause_game()
        elif event.key == K_p:
            self.shoot()

# ✅ Mouse input
if event.type == MOUSEBUTTONDOWN:
    mouse_pos = pygame.mouse.get_pos()
    print(f"Clicked at {mouse_pos}")
```

---

## Drawing Primitives

```python
# ✅ Lines
pygame.draw.line(screen, WHITE, (0, 0), (100, 100), 2)

# ✅ Circles
pygame.draw.circle(screen, RED, (400, 300), 50)

# ✅ Rectangles
pygame.draw.rect(screen, GREEN, (100, 100, 200, 100))

# ✅ Polygons
pygame.draw.polygon(screen, BLUE, [(0, 0), (100, 0), (50, 100)])

# ✅ Text
font = pygame.font.Font(None, 36)  # Default font, size 36
text = font.render("Score: 0", True, WHITE)
screen.blit(text, (10, 10))
```

---

## Game States

```python
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class Game:
    def __init__(self):
        self.state = GameState.MENU
    
    def update(self):
        if self.state == GameState.MENU:
            self.update_menu()
        elif self.state == GameState.PLAYING:
            self.update_game()
        elif self.state == GameState.PAUSED:
            self.update_paused()
    
    def update_menu(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.state = GameState.PLAYING
    
    def update_game(self):
        # Normal game loop
        pass
    
    def update_paused(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = GameState.PLAYING
```

---

## Sound

```python
pygame.mixer.init()

# Load sounds
jump_sound = pygame.mixer.Sound("jump.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Play sounds
jump_sound.play()
explosion_sound.play()

# Background music
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)  # Loop forever
pygame.mixer.music.pause()
pygame.mixer.music.unpause()
```

---

## Resources

- https://www.pygame.org/docs/
- https://pygame.readthedocs.io/
