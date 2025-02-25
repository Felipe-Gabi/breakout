import tkinter as tk

# Constants
MARGIN = 10
BALL_RADIUS = 20
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 30
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
BALL_SPEED = 6
REFRESH_RATE = 30  # in milliseconds


class BallGame:
    def __init__(self):
        # Initialize game state
        self.root = tk.Tk()
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.title("Ball Collision with Player - Diagonal Rebound")

        self.canvas = tk.Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack()

        self.ball_velocity_x = BALL_SPEED
        self.ball_velocity_y = BALL_SPEED
        self.game_over = False

        self.player = self.canvas.create_rectangle(
            MARGIN, WINDOW_HEIGHT - MARGIN - PLAYER_HEIGHT,
                    MARGIN + PLAYER_WIDTH, WINDOW_HEIGHT - MARGIN,
            fill="blue"
        )

        self.ball = self.canvas.create_oval(
            WINDOW_WIDTH // 2 - BALL_RADIUS, WINDOW_HEIGHT // 2 - BALL_RADIUS,
            WINDOW_WIDTH // 2 + BALL_RADIUS, WINDOW_HEIGHT // 2 + BALL_RADIUS,
            fill="black"
        )

        self.all_rectangles = self.create_rectangles()

        self.canvas.bind("<Motion>", self.move_player)
        self.root.bind("<Configure>", self.on_resize)
        self.move_ball()

    def create_rectangles(self):
        def create_rectangle_line(y_position, rect_width, rect_height, gap, num_rectangles):
            rectangles = []
            for i in range(num_rectangles):
                x_position = MARGIN + i * (rect_width + gap)
                color = '#{:02x}{:02x}{:02x}'.format(
                    int(255 - (255 * i / num_rectangles)), 0, int(255 * i / num_rectangles)
                )
                rect = self.canvas.create_rectangle(
                    x_position, y_position,
                    x_position + rect_width, y_position + rect_height,
                    fill=color
                )
                rectangles.append((x_position, y_position, x_position + rect_width, y_position + rect_height, rect))
            return rectangles

        rectangles_1 = create_rectangle_line(MARGIN + 30, 100, 30, 10, 7)
        rectangles_2 = create_rectangle_line(MARGIN + 70, 100, 30, 10, 7)
        rectangles_3 = create_rectangle_line(MARGIN + 110, 100, 30, 10, 7)

        return rectangles_1 + rectangles_2 + rectangles_3

    def check_margin_collision(self, ball_x, ball_y):
        if ball_x - BALL_RADIUS <= MARGIN:
            return "left"
        elif ball_x + BALL_RADIUS >= WINDOW_WIDTH - MARGIN:
            return "right"
        elif ball_y - BALL_RADIUS <= MARGIN:
            return "top"
        elif ball_y + BALL_RADIUS >= WINDOW_HEIGHT - MARGIN:
            return "bottom"
        return None

    def check_player_collision(self, ball_x, ball_y):
        player_coords = self.canvas.coords(self.player)
        player_x1, player_y1, player_x2, player_y2 = player_coords

        return (
                ball_x + BALL_RADIUS > player_x1 and ball_x - BALL_RADIUS < player_x2 and
                ball_y + BALL_RADIUS > player_y1 and ball_y - BALL_RADIUS < player_y2
        )

    def check_rectangles_collision(self, ball_x, ball_y):
        for rect in self.all_rectangles:
            rect_x1, rect_y1, rect_x2, rect_y2, rect_id = rect
            if (
                    ball_x + BALL_RADIUS > rect_x1 and ball_x - BALL_RADIUS < rect_x2 and
                    ball_y + BALL_RADIUS > rect_y1 and ball_y - BALL_RADIUS < rect_y2
            ):
                self.canvas.delete(rect_id)
                self.all_rectangles = [r for r in self.all_rectangles if r[4] != rect_id]
                return True
        return False

    def move_ball(self):
        if self.game_over:
            return

        ball_coords = self.canvas.coords(self.ball)
        ball_x = (ball_coords[0] + ball_coords[2]) / 2
        ball_y = (ball_coords[1] + ball_coords[3]) / 2

        margin_collision = self.check_margin_collision(ball_x, ball_y)
        if margin_collision in ["left", "right"]:
            self.ball_velocity_x = -self.ball_velocity_x
        if margin_collision in ["top", "bottom"]:
            self.ball_velocity_y = -self.ball_velocity_y

        if self.check_player_collision(ball_x, ball_y):
            self.ball_velocity_y = -self.ball_velocity_y
            if ball_x < (self.canvas.coords(self.player)[0] + self.canvas.coords(self.player)[2]) / 2:
                self.ball_velocity_x = -abs(self.ball_velocity_x)
            else:
                self.ball_velocity_x = abs(self.ball_velocity_x)

        if self.check_rectangles_collision(ball_x, ball_y):
            self.ball_velocity_y = -self.ball_velocity_y

        if ball_y + BALL_RADIUS >= WINDOW_HEIGHT - MARGIN:
            self.game_over = True
            self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="Game Over", font=("Arial", 24),
                                    fill="red")
            return

        self.canvas.move(self.ball, self.ball_velocity_x, self.ball_velocity_y)

        if not self.all_rectangles:
            self.game_over = True
            self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="You Win!", font=("Arial", 24),
                                    fill="green")
            return

        self.root.after(REFRESH_RATE, self.move_ball)

    def move_player(self, event):
        new_x = max(MARGIN, min(event.x - PLAYER_WIDTH / 2, WINDOW_WIDTH - MARGIN - PLAYER_WIDTH))
        self.canvas.coords(
            self.player, new_x, WINDOW_HEIGHT - MARGIN - PLAYER_HEIGHT,
                                new_x + PLAYER_WIDTH, WINDOW_HEIGHT - MARGIN
        )

    def on_resize(self, event):
        global WINDOW_WIDTH, WINDOW_HEIGHT
        WINDOW_WIDTH, WINDOW_HEIGHT = event.width, event.height
        self.canvas.config(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = BallGame()
    game.run()
