import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition des dimensions de la fenêtre et de la zone de jeu
GAME_WIDTH = 600
GAME_HEIGHT = 400
SEGMENT_SIZE = 20
WINDOW_WIDTH = GAME_WIDTH
WINDOW_HEIGHT = GAME_HEIGHT + 100  # Espace supplémentaire pour afficher le score et les instructions

# Couleurs
BACKGROUND_COLOR = (0, 0, 0)  # Noir pour le fond
SNAKE_COLOR = (56, 142, 60)  # Vert foncé du serpent
APPLE_COLOR = (244, 67, 54)  # Rouge vif pomme
LEAF_COLOR = (118, 255, 3)  # Vert clair feuille pomme
SCORE_BACKGROUND = (0, 0, 0)  # Noir fond
SCORE_TEXT_COLOR = (0, 255, 0)  # Vert fluo texte
BORDER_COLOR = (0, 255, 0)  # Vert fluo pour le contour
DIVIDER_COLOR = (0, 255, 0)  # Vert fluo pour la délimitation

# Police pour le score
pygame.font.init()
arcade_font = pygame.font.Font(None, 36)

class SnakeGame:
    def __init__(self):
        """On initialise le jeu du serpent avec les paramètres de base."""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = "Right"
        self.apple_position = self.set_new_apple_position()
        self.game_over = False
        self.paused = False
        self.score = 0

        self.run_game()

    def set_new_apple_position(self):
        """On définit une nouvelle position pour la pomme qui ne chevauche pas le serpent."""
        while True:
            x = random.randint(0, (GAME_WIDTH - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE
            y = random.randint(0, (GAME_HEIGHT - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE
            apple_position = (x, y)
            if apple_position not in self.snake:
                return apple_position

    def draw_snake(self):
        """On dessine le serpent sur l'écran."""
        for i, segment in enumerate(self.snake):
            x, y = segment
            if i == 0:  # On dessine la tête du serpent
                head_x, head_y = x, y
                if self.snake_direction == "Right":
                    points = [(head_x, head_y), (head_x + SEGMENT_SIZE, head_y + SEGMENT_SIZE // 2), (head_x, head_y + SEGMENT_SIZE)]
                    tongue = [(head_x + SEGMENT_SIZE, head_y + SEGMENT_SIZE // 2), (head_x + SEGMENT_SIZE + SEGMENT_SIZE // 2, head_y + SEGMENT_SIZE // 4), (head_x + SEGMENT_SIZE + SEGMENT_SIZE // 2, head_y + 3 * SEGMENT_SIZE // 4)]
                elif self.snake_direction == "Left":
                    points = [(head_x + SEGMENT_SIZE, head_y), (head_x, head_y + SEGMENT_SIZE // 2), (head_x + SEGMENT_SIZE, head_y + SEGMENT_SIZE)]
                    tongue = [(head_x, head_y + SEGMENT_SIZE // 2), (head_x - SEGMENT_SIZE // 2, head_y + SEGMENT_SIZE // 4), (head_x - SEGMENT_SIZE // 2, head_y + 3 * SEGMENT_SIZE // 4)]
                elif self.snake_direction == "Down":
                    points = [(head_x, head_y), (head_x + SEGMENT_SIZE // 2, head_y + SEGMENT_SIZE), (head_x + SEGMENT_SIZE, head_y)]
                    tongue = [(head_x + SEGMENT_SIZE // 2, head_y + SEGMENT_SIZE), (head_x + SEGMENT_SIZE // 4, head_y + SEGMENT_SIZE + SEGMENT_SIZE // 2), (head_x + 3 * SEGMENT_SIZE // 4, head_y + SEGMENT_SIZE + SEGMENT_SIZE // 2)]
                else:  # self.snake_direction == "Up"
                    points = [(head_x, head_y + SEGMENT_SIZE), (head_x + SEGMENT_SIZE // 2, head_y), (head_x + SEGMENT_SIZE, head_y + SEGMENT_SIZE)]
                    tongue = [(head_x + SEGMENT_SIZE // 2, head_y), (head_x + SEGMENT_SIZE // 4, head_y - SEGMENT_SIZE // 2), (head_x + 3 * SEGMENT_SIZE // 4, head_y - SEGMENT_SIZE // 2)]
                pygame.draw.polygon(self.screen, SNAKE_COLOR, points)
                pygame.draw.lines(self.screen, (255, 0, 0), False, tongue, 2)
            else:  # Dessiner le corps
                pygame.draw.rect(self.screen, SNAKE_COLOR, (x, y, SEGMENT_SIZE, SEGMENT_SIZE))

    def draw_apple(self):
        """On dessine la pomme sur l'écran."""
        x, y = self.apple_position
        pygame.draw.ellipse(self.screen, APPLE_COLOR, (x, y, SEGMENT_SIZE, SEGMENT_SIZE))
        # On dessine une feuille sur la pomme
        leaf_offset_x = SEGMENT_SIZE // 3
        leaf_offset_y = SEGMENT_SIZE // 4
        pygame.draw.ellipse(self.screen, LEAF_COLOR, (x + leaf_offset_x, y - leaf_offset_y, SEGMENT_SIZE // 4, SEGMENT_SIZE // 4))

    def draw_divider(self):
        """On dessine la ligne de délimitation entre la zone de jeu et la zone de score."""
        pygame.draw.line(self.screen, DIVIDER_COLOR, (0, GAME_HEIGHT), (GAME_WIDTH, GAME_HEIGHT), 2)

    def draw_score(self):
        """On écrit le score dans la zone du score"""
        score_text = arcade_font.render(f"Score: {self.score}", True, SCORE_TEXT_COLOR)
        self.screen.blit(score_text, (10, GAME_HEIGHT + 10))
        pause_text = arcade_font.render("Pause: touche ESPACE", True, SCORE_TEXT_COLOR)
        self.screen.blit(pause_text, (GAME_WIDTH - 300, GAME_HEIGHT + 10))

    def move_snake(self):
        """On gère les déplacements du serpent"""
        if self.game_over or self.paused:
            return

        head_x, head_y = self.snake[0]

        # On calcule la nouvelle direction pour aller vers la pomme
        apple_x, apple_y = self.apple_position
        if head_x < apple_x and self.snake_direction != "Left":
            self.snake_direction = "Right"
        elif head_x > apple_x and self.snake_direction != "Right":
            self.snake_direction = "Left"
        elif head_y < apple_y and self.snake_direction != "Up":
            self.snake_direction = "Down"
        elif head_y > apple_y and self.snake_direction != "Down":
            self.snake_direction = "Up"

        if self.snake_direction == "Right":
            new_head = (head_x + SEGMENT_SIZE, head_y)
        elif self.snake_direction == "Left":
            new_head = (head_x - SEGMENT_SIZE, head_y)
        elif self.snake_direction == "Down":
            new_head = (head_x, head_y + SEGMENT_SIZE)
        elif self.snake_direction == "Up":
            new_head = (head_x, head_y - SEGMENT_SIZE)

        if new_head in self.snake or not (0 <= new_head[0] < GAME_WIDTH and 0 <= new_head[1] < GAME_HEIGHT):
            self.game_over = True
            return

        self.snake = [new_head] + self.snake[:-1]

        if new_head == self.apple_position:
            self.snake.append(self.snake[-1])
            self.apple_position = self.set_new_apple_position()
            self.score += 100

    def update_direction(self):
        """On met à jour les directions du serpent"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.snake_direction != "Left":
            self.snake_direction = "Right"
        elif keys[pygame.K_LEFT] and self.snake_direction != "Right":
            self.snake_direction = "Left"
        elif keys[pygame.K_DOWN] and self.snake_direction != "Up":
            self.snake_direction = "Down"
        elif keys[pygame.K_UP] and self.snake_direction != "Down":
            self.snake_direction = "Up"

    def toggle_pause(self):
        """Pour pouvoir mettre en pause le jeu"""
        self.paused = not self.paused

    def run_game(self):
        """Pour lancer le jeu"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.toggle_pause()

            if not self.paused and not self.game_over:
                self.update_direction()
                self.move_snake()

            self.screen.fill(BACKGROUND_COLOR)
            self.draw_snake()
            self.draw_apple()
            self.draw_divider()
            self.draw_score()

            if self.game_over:
                game_over_text = arcade_font.render("GAME OVER", True, (255, 255, 255))
                self.screen.blit(game_over_text, (GAME_WIDTH / 2 - 100, GAME_HEIGHT / 2 - 20))

            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()

if __name__ == "__main__":
    SnakeGame()
