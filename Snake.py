import tkinter as tk
import random
from collections import deque

# Définition des dimensions de la fenêtre
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
SEGMENT_SIZE = 20

# Classe pour représenter le jeu Snake
class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
        self.canvas.pack()

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = "Right"
        self.apple_position = self.set_new_apple_position()
        self.game_over = False
        self.score = 0

        self.score_text = self.canvas.create_text(50, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 14))

        self.draw_snake()
        self.draw_apple()

        self.move_snake()
        
    def set_new_apple_position(self):
        while True:
            x = random.randint(0, (WINDOW_WIDTH - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE
            apple_position = (x, y)
            if apple_position not in self.snake:
                return apple_position

    def draw_snake(self):
        self.canvas.delete("snake")
        for i, segment in enumerate(self.snake):
            x, y = segment
            self.canvas.create_rectangle(x, y, x + SEGMENT_SIZE, y + SEGMENT_SIZE, fill="green", tag="snake")
            if i == 0:  # Draw eyes for the head segment
                eye_size = SEGMENT_SIZE // 5
                offset = SEGMENT_SIZE // 3
                if self.snake_direction in ["Right", "Left"]:
                    self.canvas.create_oval(x + offset, y + offset, x + offset + eye_size, y + offset + eye_size, fill="white", tag="snake")
                    self.canvas.create_oval(x + offset, y + 2*offset, x + offset + eye_size, y + 2*offset + eye_size, fill="white", tag="snake")
                else:
                    self.canvas.create_oval(x + offset, y + offset, x + offset + eye_size, y + offset + eye_size, fill="white", tag="snake")
                    self.canvas.create_oval(x + 2*offset, y + offset, x + 2*offset + eye_size, y + offset + eye_size, fill="white", tag="snake")

    def draw_apple(self):
        self.canvas.delete("apple")
        x, y = self.apple_position
        self.canvas.create_oval(x, y, x + SEGMENT_SIZE, y + SEGMENT_SIZE, fill="red", tag="apple")

    def move_snake(self):
        if self.game_over:
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

        if new_head in self.snake or not (0 <= new_head[0] < WINDOW_WIDTH and 0 <= new_head[1] < WINDOW_HEIGHT):
            self.game_over = True
            self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, text="GAME OVER", fill="white", font=("Arial", 24))
            return

        self.snake = [new_head] + self.snake[:-1]

        if new_head == self.apple_position:
            self.snake.append(self.snake[-1])
            self.apple_position = self.set_new_apple_position()
            self.draw_apple()
            self.score += 100
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

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

                if (0 <= new_pos[0] < WINDOW_WIDTH and 0 <= new_pos[1] < WINDOW_HEIGHT and
                        new_pos not in self.snake and new_pos not in visited):
                    queue.append((new_pos, path + [direction]))
                    visited.add(new_pos)

        # Si aucun chemin sûr n'est trouvé, continue dans la direction actuelle
        current_direction_move = dir_dict[self.snake_direction]
        new_head = (head[0] + current_direction_move[0], head[1] + current_direction_move[1])
        if new_head in self.snake or not (0 <= new_head[0] < WINDOW_WIDTH and 0 <= new_head[1] < WINDOW_HEIGHT):
            self.snake_direction = random.choice([d for d in directions if d != self.snake_direction])

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Snake Game")
    game = SnakeGame(root)
    root.mainloop()
