import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman")

# Colores
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)

# Clase Pacman
class Pacman:
    def _init_(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 20
        self.speed = 5
        self.direction = 0  # 0: derecha, 1: arriba, 2: izquierda, 3: abajo
        self.mouth_angle = 45
        self.mouth_change = 3
        self.mouth_direction = -1
        
    def draw(self):
        # Dibujar Pacman
        start_angle = self.direction * 90 + self.mouth_angle
        end_angle = self.direction * 90 - self.mouth_angle
        
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)
        pygame.draw.polygon(screen, BLACK, [
            (self.x, self.y),
            (self.x + self.radius * math.cos(math.radians(start_angle)), 
             self.y - self.radius * math.sin(math.radians(start_angle))),
            (self.x + self.radius * math.cos(math.radians(end_angle)), 
             self.y - self.radius * math.sin(math.radians(end_angle)))
        ])
        
    def update(self):
        # Actualizar animación de la boca
        self.mouth_angle += self.mouth_change * self.mouth_direction
        if self.mouth_angle <= 0 or self.mouth_angle >= 45:
            self.mouth_direction *= -1
            
    def move(self, walls):
        # Guardar posición anterior
        old_x, old_y = self.x, self.y
        
        # Mover según la dirección
        if self.direction == 0:  # Derecha
            self.x += self.speed
        elif self.direction == 1:  # Arriba
            self.y -= self.speed
        elif self.direction == 2:  # Izquierda
            self.x -= self.speed
        elif self.direction == 3:  # Abajo
            self.y += self.speed
            
        # Verificar colisiones con paredes
        for wall in walls:
            if self.check_collision(wall):
                self.x, self.y = old_x, old_y
                break
                
        # Mantener dentro de los límites de la pantalla
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))
        
    def check_collision(self, wall):
        # Verificar colisión con una pared
        return (self.x + self.radius > wall.x and 
                self.x - self.radius < wall.x + wall.width and
                self.y + self.radius > wall.y and 
                self.y - self.radius < wall.y + wall.height)

# Clase Fantasma
class Ghost:
    def _init_(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 15
        self.speed = 2
        self.direction = random.randint(0, 3)
        self.change_direction_counter = 0
        
    def draw(self):
        # Dibujar cuerpo del fantasma
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        
        # Dibujar parte inferior del fantasma
        points = [
            (self.x - self.radius, self.y),
            (self.x - self.radius, self.y + self.radius),
            (self.x - self.radius//2, self.y + self.radius//2),
            (self.x, self.y + self.radius),
            (self.x + self.radius//2, self.y + self.radius//2),
            (self.x + self.radius, self.y + self.radius),
            (self.x + self.radius, self.y)
        ]
        pygame.draw.polygon(screen, self.color, points)
        
        # Dibujar ojos
        eye_offset = 5
        pygame.draw.circle(screen, WHITE, (self.x - eye_offset, self.y - 5), 4)
        pygame.draw.circle(screen, WHITE, (self.x + eye_offset, self.y - 5), 4)
        pygame.draw.circle(screen, BLACK, (self.x - eye_offset, self.y - 5), 2)
        pygame.draw.circle(screen, BLACK, (self.x + eye_offset, self.y - 5), 2)
        
    def move(self, walls):
        self.change_direction_counter += 1
        
        # Cambiar dirección aleatoriamente
        if self.change_direction_counter > 60:
            self.direction = random.randint(0, 3)
            self.change_direction_counter = 0
            
        # Guardar posición anterior
        old_x, old_y = self.x, self.y
        
        # Mover según la dirección
        if self.direction == 0:  # Derecha
            self.x += self.speed
        elif self.direction == 1:  # Arriba
            self.y -= self.speed
        elif self.direction == 2:  # Izquierda
            self.x -= self.speed
        elif self.direction == 3:  # Abajo
            self.y += self.speed
            
        # Verificar colisiones con paredes
        for wall in walls:
            if self.check_collision(wall):
                self.x, self.y = old_x, old_y
                self.direction = random.randint(0, 3)
                break
                
        # Mantener dentro de los límites de la pantalla
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))
        
    def check_collision(self, wall):
        # Verificar colisión con una pared
        return (self.x + self.radius > wall.x and 
                self.x - self.radius < wall.x + wall.width and
                self.y + self.radius > wall.y and 
                self.y - self.radius < wall.y + wall.height)

# Clase Pared
class Wall:
    def _init_(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

# Clase Punto
class Dot:
    def _init_(self, x, y):
        self.x = x
        self.y = y
        self.radius = 3
        self.collected = False
        
    def draw(self):
        if not self.collected:
            pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)
            
    def check_collision(self, pacman):
        if self.collected:
            return False
            
        distance = math.sqrt((self.x - pacman.x)*2 + (self.y - pacman.y)*2)
        return distance < pacman.radius + self.radius

# Crear objetos del juego
pacman = Pacman()

# Crear fantasmas
ghosts = [
    Ghost(100, 100, RED),
    Ghost(700, 100, PINK),
    Ghost(100, 500, CYAN),
    Ghost(700, 500, ORANGE)
]

# Crear paredes (laberinto simple)
walls = [
    Wall(0, 0, WIDTH, 20),
    Wall(0, 0, 20, HEIGHT),
    Wall(0, HEIGHT-20, WIDTH, 20),
    Wall(WIDTH-20, 0, 20, HEIGHT),
    
    # Paredes internas
    Wall(100, 100, 200, 20),
    Wall(400, 100, 200, 20),
    Wall(100, 200, 20, 150),
    Wall(200, 200, 150, 20),
    Wall(400, 200, 150, 20),
    Wall(600, 200, 20, 150),
    Wall(100, 400, 200, 20),
    Wall(400, 400, 200, 20),
    Wall(300, 300, 20, 100)
]

# Crear puntos
dots = []
for i in range(50):
    x = random.randint(40, WIDTH - 40)
    y = random.randint(40, HEIGHT - 40)
    
    # Verificar que no esté muy cerca de una pared
    valid_position = True
    for wall in walls:
        if (x > wall.x - 20 and x < wall.x + wall.width + 20 and
            y > wall.y - 20 and y < wall.y + wall.height + 20):
            valid_position = False
            break
            
    if valid_position:
        dots.append(Dot(x, y))

# Variables del juego
score = 0
game_over = False
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pacman.direction = 0
            elif event.key == pygame.K_UP:
                pacman.direction = 1
            elif event.key == pygame.K_LEFT:
                pacman.direction = 2
            elif event.key == pygame.K_DOWN:
                pacman.direction = 3
            elif event.key == pygame.K_r and game_over:
                # Reiniciar juego
                pacman = Pacman()
                ghosts = [
                    Ghost(100, 100, RED),
                    Ghost(700, 100, PINK),
                    Ghost(100, 500, CYAN),
                    Ghost(700, 500, ORANGE)
                ]
                for dot in dots:
                    dot.collected = False
                score = 0
                game_over = False
    
    if not game_over:
        # Actualizar juego
        pacman.update()
        pacman.move(walls)
        
        for ghost in ghosts:
            ghost.move(walls)
            
        # Verificar colisiones con puntos
        for dot in dots:
            if dot.check_collision(pacman) and not dot.collected:
                dot.collected = True
                score += 10
                
        # Verificar colisiones con fantasmas
        for ghost in ghosts:
            distance = math.sqrt((ghost.x - pacman.x)*2 + (ghost.y - pacman.y)*2)
            if distance < pacman.radius + ghost.radius:
                game_over = True
                
        # Verificar si se han recolectado todos los puntos
        if all(dot.collected for dot in dots):
            game_over = True
    
    # Dibujar
    screen.fill(BLACK)
    
    # Dibujar paredes
    for wall in walls:
        wall.draw()
        
    # Dibujar puntos
    for dot in dots:
        dot.draw()
        
    # Dibujar Pacman y fantasmas
    pacman.draw()
    for ghost in ghosts:
        ghost.draw()
        
    # Dibujar puntuación
    score_text = font.render(f"Puntuación: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Dibujar mensaje de game over
    if game_over:
        if all(dot.collected for dot in dots):
            game_over_text = font.render("¡GANASTE! Presiona R para reiniciar", True, WHITE)
        else:
            game_over_text = font.render("GAME OVER - Presiona R para reiniciar", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 180, HEIGHT//2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
