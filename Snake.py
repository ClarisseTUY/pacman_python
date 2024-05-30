import tkinter as tk
import random
from collections import deque

# Définition des dimensions de la fenêtre et de la zone de jeu
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600  # Augmentée pour inclure la zone de score
GAME_WIDTH = 600
GAME_HEIGHT = 400  # Hauteur de la zone de jeu
SEGMENT_SIZE = 20

# Couleurs
BACKGROUND_COLOR = "black"  # Noir pour le fond
SNAKE_COLOR = "#388E3C"  # Vert foncé
APPLE_COLOR = "#F44336"  # Rouge vif
LEAF_COLOR = "#76FF03"  # Vert clair
SCORE_BACKGROUND = "black"  # Noir
SCORE_TEXT_COLOR = "#00FF00"  # Vert fluo
BORDER_COLOR = "#00FF00"  # Vert fluo pour le contour
DIVIDER_COLOR = "#00FF00"  # Vert fluo pour la délimitation

# Classe pour représenter le jeu Snake
class SnakeGame:
    def __init__(self, master):
        self.master = master

        # Cadre pour le score
        self.score_frame = tk.Frame(master, width=WINDOW_WIDTH, height=50, bg=SCORE_BACKGROUND)
        self.score_frame.pack_propagate(False)
        self.score_frame.pack()

        arcade_font = ("Pixelade", 24)  # Police de style arcade
        self.score_label = tk.Label(self.score_frame, text="Score:", font=arcade_font, bg=SCORE_BACKGROUND, fg=SCORE_TEXT_COLOR)
        self.score_label.pack(side=tk.LEFT)

        self.score_value = tk.Label(self.score_frame, text="0", font=arcade_font, bg=SCORE_BACKGROUND, fg=SCORE_TEXT_COLOR)
        self.score_value.pack(side=tk.LEFT)

        self.pause_label = tk.Label(self.score_frame, text="Pause : appuyez sur ESPACE", font=arcade_font, bg=SCORE_BACKGROUND, fg=SCORE_TEXT_COLOR)
        self.pause_label.pack(side=tk.RIGHT)

        # Cadre pour le jeu
        self.canvas = tk.Canvas(master, width=GAME_WIDTH, height=GAME_HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=2, highlightbackground=BORDER_COLOR)
        self.canvas.place(x=(WINDOW_WIDTH - GAME_WIDTH) / 2, y=(WINDOW_HEIGHT - GAME_HEIGHT) / 2 )  # Centrer le canvas dans la fenêtre

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = "Right"
        self.apple_position = self.set_new_apple_position()
        self.game_over = False
        self.paused = False
        self.score = 0

        self.draw_snake()
        self.draw_apple()
        self.draw_divider()

        self.master.bind("<space>", self.toggle_pause)
        self.move_snake()

    def toggle_pause(self, event):
        self.paused = not self.paused
        if not self.paused:
            self.move_snake()

    def set_new_apple_position(self):
        while True:
            x = random.randint(0, (GAME_WIDTH - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE
            y = random.randint(0, (GAME_HEIGHT - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE
            apple_position = (x, y)
            if apple_position not in self.snake:
                return apple_position

    def draw_snake(self):
        self.canvas.delete("snake")
        for i, segment in enumerate(self.snake):
            x, y = segment
            self.canvas.create_rectangle(x, y, x + SEGMENT_SIZE, y + SEGMENT_SIZE, fill=SNAKE_COLOR, tag="snake")
            if i == 0:  # Dessiner les yeux pour le segment de la tête
                eye_size = SEGMENT_SIZE // 5
                offset = SEGMENT_SIZE // 3
                if self.snake_direction in ["Right", "Left"]:
                    self.canvas.create_oval(x + offset, y + offset, x + offset + eye_size, y + offset + eye_size, fill="white", tag="snake")
                    self.canvas.create_oval(x + offset, y + 2 * offset, x + offset + eye_size, y + 2 * offset + eye_size, fill="white", tag="snake")
                else:
                    self.canvas.create_oval(x + offset, y + offset, x + offset + eye_size, y + offset + eye_size, fill="white", tag="snake")
                    self.canvas.create_oval(x + 2 * offset, y + offset, x + 2 * offset + eye_size, y + offset + eye_size, fill="white", tag="snake")

    def draw_apple(self):
        self.canvas.delete("apple")
        x, y = self.apple_position
        self.canvas.create_oval(x, y, x + SEGMENT_SIZE, y + SEGMENT_SIZE, fill=APPLE_COLOR, tag="apple")
        # Dessiner une feuille sur la pomme
        leaf_offset_x = SEGMENT_SIZE // 3
        leaf_offset_y = SEGMENT_SIZE // 4
        self.canvas.create_oval(x + leaf_offset_x, y - leaf_offset_y, x + leaf_offset_x + SEGMENT_SIZE // 4, y - leaf_offset_y + SEGMENT_SIZE // 4, fill=LEAF_COLOR, tag="apple")

    def draw_divider(self):
        # Dessiner la délimitation entre la zone de jeu et la zone de score
        self.canvas.create_line(0, 0, GAME_WIDTH, 0, fill=DIVIDER_COLOR, width=2)

    def move_snake(self):
        if self.game_over or self.paused:
            return

        head_x, head_y = self.snake[0]

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
            self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="GAME OVER", fill="white", font=("Pixelade", 24))
            return

        self.snake = [new_head] + self.snake[:-1]

        if new_head == self.apple_position:
            self.snake.append(self.snake[-1])
            self.apple_position = self.set_new_apple_position()
            self.draw_apple()
            self.score += 100
            self.score_value.config(text=str(self.score))

        self.draw_snake()
        self.master.after(100, self.move_snake)
        self.update_direction()

    def update_direction(self):
        head = self.snake[0]
        apple = self.apple_position

        directions = ["Right", "Left", "Down", "Up"]
        moves = [(SEGMENT_SIZE, 0), (-SEGMENT_SIZE, 0), (0, SEGMENT_SIZE), (0, -SEGMENT_SIZE)]
        dir_dict = dict(zip(directions, moves))

        queue = deque([(head, [])])
        visited = set()
        visited.add(head)

        while queue:
            current_pos, path = queue.popleft()

            if current_pos == apple:
                if path:
                    self.snake_direction = path[0]
                return

            for direction, move in dir_dict.items():
                new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])

                if (0 <= new_pos[0] < GAME_WIDTH and 0 <= new_pos[1] < GAME_HEIGHT and
                        new_pos not in self.snake and new_pos not in visited):
                    queue.append((new_pos, path + [direction]))
                    visited.add(new_pos)

        # Si aucun chemin sûr n'est trouvé, continue dans la direction actuelle
        current_direction_move = dir_dict[self.snake_direction]
        new_head = (head[0] + current_direction_move[0], head[1] + current_direction_move[1])
        if new_head in self.snake or not (0 <= new_head[0] < GAME_WIDTH and 0 <= new_head[1] < GAME_HEIGHT):
            self.snake_direction = random.choice([d for d in directions if d != self.snake_direction])

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Snake Game")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.configure(bg=BACKGROUND_COLOR)
    game = SnakeGame(root)
    root.mainloop()
