print("Iniciando simulacion")
import pygame
import math
import sys

# Inicializar Pygame
pygame.init()

# Constantes
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 68, 68)
YELLOW = (255, 255, 0)
GREEN = (40, 167, 69)
BLUE = (30, 60, 114)
GRAY = (128, 128, 128)
DARK_GREEN = (45, 90, 39)

class RacingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🏁 CIRCUITO SERPENTEANTE F1 🏁")
        self.clock = pygame.time.Clock()
        
        # Variables del juego
        self.running = True
        self.race_active = False
        self.speed = 5
        self.current_distance = 0
        self.laps = 0
        self.has_completed_lap = False
        
        # Crear la pista (puntos de la curva)
        self.track_points = self.create_track()
        self.total_track_length = len(self.track_points)
        
        # Posición del auto
        self.car_x = 150
        self.car_y = 100
        self.car_angle = 0
        
        # Fuentes
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
    def create_track(self):
        """Crear puntos de la pista basados en la curva original"""
        points = []
        
        # Parámetros de la pista serpenteante
        for t in range(360):
            angle = math.radians(t * 3)  # Múltiples vueltas
            
            # Crear forma serpenteante similar al original
            center_x = 400
            center_y = 300
            
            # Radio variable para crear la forma serpenteante
            base_radius = 150 + 50 * math.sin(angle * 0.7)
            radius_variation = 20 * math.sin(angle * 2.3)
            radius = base_radius + radius_variation
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            # Asegurar que los puntos estén dentro de la pantalla
            x = max(100, min(700, x))
            y = max(100, min(500, y))
            
            points.append((x, y))
        
        return points
    
    def draw_track(self):
        """Dibujar la pista"""
        # Dibujar bordes de la pista
        for i in range(len(self.track_points)):
            current_point = self.track_points[i]
            next_point = self.track_points[(i + 1) % len(self.track_points)]
            
            # Calcular puntos para los bordes de la pista
            dx = next_point[0] - current_point[0]
            dy = next_point[1] - current_point[1]
            length = math.sqrt(dx*dx + dy*dy)
            
            if length > 0:
                # Normalizar y crear perpendicular
                nx = -dy / length * 30  # Ancho de la pista
                ny = dx / length * 30
                
                # Puntos del borde exterior
                outer1 = (current_point[0] + nx, current_point[1] + ny)
                outer2 = (next_point[0] + nx, next_point[1] + ny)
                
                # Puntos del borde interior
                inner1 = (current_point[0] - nx, current_point[1] - ny)
                inner2 = (next_point[0] - nx, next_point[1] - ny)
                
                # Dibujar segmentos de la pista
                pygame.draw.polygon(self.screen, GRAY, [outer1, outer2, inner2, inner1])
        
        # Dibujar línea central amarilla discontinua
        for i in range(0, len(self.track_points), 10):
            point = self.track_points[i]
            pygame.draw.circle(self.screen, YELLOW, (int(point[0]), int(point[1])), 2)
    
    def draw_car(self):
        """Dibujar el auto"""
        # Crear rectángulo del auto
        car_rect = pygame.Rect(0, 0, 25, 15)
        car_rect.center = (self.car_x, self.car_y)
        
        # Dibujar auto principal
        pygame.draw.rect(self.screen, RED, car_rect)
        pygame.draw.rect(self.screen, BLACK, car_rect, 2)
        
        # Dibujar ventana (amarillo)
        window_rect = pygame.Rect(0, 0, 19, 4)
        window_rect.center = (self.car_x, self.car_y - 3)
        pygame.draw.rect(self.screen, YELLOW, window_rect)
    
    def update_car_position(self):
        """Actualizar posición del auto"""
        if not self.race_active:
            return
        
        # Incrementar distancia basada en velocidad
        self.current_distance += self.speed * 0.8
        
        # Verificar si completó una vuelta
        if self.current_distance >= self.total_track_length:
            if not self.has_completed_lap:
                self.laps += 1
                self.has_completed_lap = True
            self.current_distance = self.current_distance % self.total_track_length
        else:
            self.has_completed_lap = False
        
        # Obtener posición actual
        current_index = int(self.current_distance) % len(self.track_points)
        next_index = (current_index + 1) % len(self.track_points)
        
        # Interpolación entre puntos
        t = self.current_distance - int(self.current_distance)
        current_point = self.track_points[current_index]
        next_point = self.track_points[next_index]
        
        self.car_x = current_point[0] + t * (next_point[0] - current_point[0])
        self.car_y = current_point[1] + t * (next_point[1] - current_point[1])
        
        # Calcular ángulo del auto
        dx = next_point[0] - current_point[0]
        dy = next_point[1] - current_point[1]
        self.car_angle = math.atan2(dy, dx)
    
    def draw_ui(self):
        """Dibujar interfaz de usuario"""
        # Título
        title_text = self.font_large.render("🏁 CIRCUITO SERPENTEANTE F1 🏁", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 30))
        pygame.draw.rect(self.screen, BLACK, title_rect.inflate(20, 10))
        pygame.draw.rect(self.screen, WHITE, title_rect.inflate(20, 10), 3)
        self.screen.blit(title_text, title_rect)
        
        # Control de velocidad
        speed_bg = pygame.Rect(650, 80, 120, 80)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), speed_bg)
        pygame.draw.rect(self.screen, WHITE, speed_bg, 2)
        
        speed_text = self.font_medium.render("Velocidad:", True, WHITE)
        self.screen.blit(speed_text, (660, 90))
        speed_value = self.font_medium.render(str(self.speed), True, WHITE)
        self.screen.blit(speed_value, (720, 110))
        
        # Contador de vueltas
        lap_bg = pygame.Rect(30, 80, 100, 80)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), lap_bg)
        pygame.draw.rect(self.screen, WHITE, lap_bg, 2)
        
        lap_text = self.font_medium.render("Vuelta:", True, WHITE)
        self.screen.blit(lap_text, (40, 90))
        lap_value = self.font_large.render(str(self.laps), True, WHITE)
        self.screen.blit(lap_value, (70, 110))
        
        # Botones
        button_y = WINDOW_HEIGHT - 60
        
        # Botón Iniciar
        start_btn = pygame.Rect(250, button_y, 100, 40)
        color = GREEN if not self.race_active else GRAY
        pygame.draw.rect(self.screen, color, start_btn)
        pygame.draw.rect(self.screen, WHITE, start_btn, 2)
        start_text = self.font_medium.render("Iniciar", True, WHITE)
        text_rect = start_text.get_rect(center=start_btn.center)
        self.screen.blit(start_text, text_rect)
        
        # Botón Pausar
        pause_btn = pygame.Rect(360, button_y, 100, 40)
        color = YELLOW if self.race_active else GRAY
        pygame.draw.rect(self.screen, color, pause_btn)
        pygame.draw.rect(self.screen, WHITE, pause_btn, 2)
        pause_text = self.font_medium.render("Pausar", True, BLACK)
        text_rect = pause_text.get_rect(center=pause_btn.center)
        self.screen.blit(pause_text, text_rect)
        
        # Botón Reiniciar
        reset_btn = pygame.Rect(470, button_y, 100, 40)
        pygame.draw.rect(self.screen, RED, reset_btn)
        pygame.draw.rect(self.screen, WHITE, reset_btn, 2)
        reset_text = self.font_medium.render("Reiniciar", True, WHITE)
        text_rect = reset_text.get_rect(center=reset_btn.center)
        self.screen.blit(reset_text, text_rect)
        
        return start_btn, pause_btn, reset_btn
    
    def handle_click(self, pos, start_btn, pause_btn, reset_btn):
        """Manejar clics en botones"""
        if start_btn.collidepoint(pos):
            self.race_active = True
        elif pause_btn.collidepoint(pos):
            self.race_active = False
        elif reset_btn.collidepoint(pos):
            self.reset_race()
    
    def reset_race(self):
        """Reiniciar la carrera"""
        self.race_active = False
        self.current_distance = 0
        self.laps = 0
        self.has_completed_lap = False
        if self.track_points:
            self.car_x, self.car_y = self.track_points[0]
        self.car_angle = 0
    
    def handle_events(self):
        """Manejar eventos"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.race_active = not self.race_active
                elif event.key == pygame.K_r:
                    self.reset_race()
                elif event.key == pygame.K_UP and self.speed < 10:
                    self.speed += 1
                elif event.key == pygame.K_DOWN and self.speed > 1:
                    self.speed -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_btn, pause_btn, reset_btn = self.draw_ui()
                self.handle_click(event.pos, start_btn, pause_btn, reset_btn)
    
    def run(self):
        """Bucle principal del juego"""
        # Inicializar posición del auto
        self.reset_race()
        
        while self.running:
            self.handle_events()
            self.update_car_position()
            
            # Dibujar todo
            self.screen.fill(DARK_GREEN)
            self.draw_track()
            self.draw_car()
            start_btn, pause_btn, reset_btn = self.draw_ui()
            
            # Instrucciones
            instructions = [
                "CONTROLES:",
                "ESPACIO: Iniciar/Pausar",
                "R: Reiniciar",
                "↑/↓: Velocidad",
                "Click en botones"
            ]
            
            for i, instruction in enumerate(instructions):
                text = self.font_small.render(instruction, True, WHITE)
                self.screen.blit(text, (10, WINDOW_HEIGHT - 120 + i * 20))
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Ejecutar el juego
if __name__ == "__main__":
    game = RacingGame()
    
    while game.running:
        game.handle_events()
        game.update_car_position()

        game.screen.fill(DARK_GREEN)  # Fondo
        game.draw_track()
        game.draw_car()
        start_btn, pause_btn, reset_btn = game.draw_ui()
        
        pygame.display.flip()
        game.clock.tick(FPS)
    
    pygame.quit()
    sys.exit()
    
