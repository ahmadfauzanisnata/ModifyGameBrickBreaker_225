import tkinter as tk
import random


class Ball:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.item = canvas.create_oval(
            x - 10, y - 10, x + 10, y + 10, fill='yellow')
        self.dx = random.choice([-4, 4])
        self.dy = -4
        self.speed = 30

    def move(self):
        self.canvas.move(self.item, self.dx, self.dy)
        pos = self.canvas.coords(self.item)

        # Bounce on walls
        if pos[0] <= 0 or pos[2] >= self.canvas.winfo_width():
            self.dx *= -1
        if pos[1] <= 0:
            self.dy *= -1
        return pos

    def bounce(self, increase_speed=False):
        self.dy *= -1
        if increase_speed:
            self.dx *= 1.1
            self.dy *= 1.1


class Paddle:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.segments = []
        self.create_snake(x, y)

    def create_snake(self, x, y):
        """Create paddle as a segmented snake."""
        segment_width = 20
        for i in range(-3, 4):
            segment = self.canvas.create_rectangle(
                x + i * segment_width - 10, y - 5,
                x + i * segment_width + 10, y + 5,
                fill=random.choice(['green', 'lime', 'darkgreen']))
            self.segments.append(segment)

    def move(self, offset):
        width = self.canvas.winfo_width()
        head_pos = self.canvas.coords(self.segments[0])
        tail_pos = self.canvas.coords(self.segments[-1])

        # Check bounds
        if offset < 0 and head_pos[0] + offset < 0:
            return
        if offset > 0 and tail_pos[2] + offset > width:
            return

        for segment in self.segments:
            self.canvas.move(segment, offset, 0)


class Brick:
    COLORS = ['#FF5733', '#FFC300', '#DAF7A6', '#75C6FF', '#B36CFF']

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.item = canvas.create_rectangle(
            x - 35, y - 15, x + 35, y + 15,
            fill=random.choice(Brick.COLORS), tags="brick"
        )

    def destroy(self):
        self.canvas.delete(self.item)


class Game:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, bg='black', width=600, height=400)
        self.canvas.pack()
        self.lives = 5
        self.score = 0

        # Create objects
        self.ball = Ball(self.canvas, 300, 300)
        self.paddle = Paddle(self.canvas, 300, 350)
        self.bricks = [Brick(self.canvas, x, y)
                       for x in range(50, 600, 80) for y in range(50, 150, 30)]

        # HUD
        self.lives_text = self.canvas.create_text(
            50, 20, text=f'Lives: {self.lives}', fill='white', font=('times new roman', 14))
        self.score_text = self.canvas.create_text(
            550, 20, text=f'Score: {self.score}', fill='white', font=('times new roman', 14))

        # Game state
        self.running = False
        self.start_text = self.canvas.create_text(
            300, 200, text="Press SPACE to Start",
            fill="white", font=("times new roman", 20))

        # Bind keys
        self.canvas.bind_all('<Left>', lambda _: self.paddle.move(-20))
        self.canvas.bind_all('<Right>', lambda _: self.paddle.move(20))
        self.canvas.bind_all('<space>', lambda _: self.start_game())

    def start_game(self):
        """Start the game loop when SPACE is pressed."""
        if not self.running:
            self.running = True
            self.canvas.delete(self.start_text)
            self.loop()

    def loop(self):
        """Main game loop."""
        if self.running:
            pos = self.ball.move()
            self.check_collisions(pos)
            self.check_game_over()
            self.canvas.after(self.ball.speed, self.loop)

    def check_collisions(self, ball_pos):
        # Bounce off paddle
        for segment in self.paddle.segments:
            segment_pos = self.canvas.coords(segment)
            if (ball_pos[2] >= segment_pos[0] and ball_pos[0] <= segment_pos[2] and
                    ball_pos[3] >= segment_pos[1] and ball_pos[1] <= segment_pos[3]):
                self.ball.bounce(increase_speed=True)
                break

        # Check for brick collision
        overlapping = self.canvas.find_overlapping(*ball_pos)
        for obj_id in overlapping:
            if "brick" in self.canvas.gettags(obj_id):
                brick = next(
                    (brick for brick in self.bricks if brick.item == obj_id), None)
                if brick:
                    brick.destroy()
                    self.bricks.remove(brick)
                    self.ball.bounce()
                    self.update_score(10)

    def check_game_over(self):
        if self.ball.move()[3] >= self.canvas.winfo_height():
            self.lives -= 1
            self.update_lives()
            if self.lives == 0:
                self.running = False
                self.canvas.create_text(
                    300, 200, text="Game Over", fill='red', font=('times new roman', 24))
            else:
                self.reset_ball()

        if not self.bricks:
            self.running = False
            self.canvas.create_text(
                300, 200, text="You Win!", fill='green', font=('times new roman', 24))

    def reset_ball(self):
        self.canvas.delete(self.ball.item)
        self.ball = Ball(self.canvas, 300, 300)

    def update_lives(self):
        self.canvas.itemconfig(self.lives_text, text=f'Lives: {self.lives}')

    def update_score(self, points):
        self.score += points
        self.canvas.itemconfig(self.score_text, text=f'Score: {self.score}')


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Brick Breaker - Snake Style!")
    game = Game(root)
    root.mainloop()




