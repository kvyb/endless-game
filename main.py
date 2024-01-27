import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
BALL_SIZE = 20
BALL_SPEED = 5
SQUARE_SIZE = 20

# Colors
LEFT_COLOR = (128, 0, 128)  # Purple
RIGHT_COLOR = (255, 165, 0)  # Orange
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Domain Game")

class Ball:
    def __init__(self, x, y, color, paint_color):
        self.x = x
        self.y = y
        self.color = WHITE
        self.paint_color = paint_color
        self.dx = BALL_SPEED if color == LEFT_COLOR else -BALL_SPEED
        self.dy = BALL_SPEED if random.choice([True, False]) else -BALL_SPEED

    def bounce(self, collision_type):
        # Convert the current velocity into an angle
        angle = math.atan2(self.dy, self.dx)

        # Adjust the angle by a small random amount within ±2 degrees
        angle_adjustment = random.uniform(-math.radians(3), math.radians(3))

        if collision_type == 'horizontal':
            # Reflect the angle horizontally and apply the adjustment
            new_angle = math.pi - angle + angle_adjustment
        elif collision_type == 'vertical':
            # Reflect the angle vertically and apply the adjustment
            new_angle = -angle + angle_adjustment
        else:
            # For other types of collisions, randomly adjust both components
            new_angle = angle + angle_adjustment

        # Update the velocity components while maintaining speed
        self.dx = BALL_SPEED * math.cos(new_angle)
        self.dy = BALL_SPEED * math.sin(new_angle)

    def move(self, squares):
        # Calculate new position
        new_x = self.x + self.dx
        new_y = self.y + self.dy

        # Check for collision with a square
        if self.will_collide(new_x, new_y, squares):
            # Change the color of the collided square
            self.change_square_color(squares, new_x, new_y)
            # Determine the collision type for bouncing
            if new_x != self.x:
                collision_type = 'horizontal'
            else:
                collision_type = 'vertical'
            self.bounce(collision_type)
            return

        # Check if new position is not valid (hitting the boundaries)
        if new_x < 0 or new_x > WIDTH - BALL_SIZE:  # Hitting left or right boundary
            self.bounce('horizontal')
            return
        elif new_y < 0 or new_y > HEIGHT - BALL_SIZE:  # Hitting top or bottom boundary
            self.bounce('vertical')
            return

        # Move to the new position if no collision
        self.x = new_x
        self.y = new_y

    def will_collide(self, x, y, squares):
        ball_rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        row = int(y // SQUARE_SIZE)  # Ensure it's an integer
        col = int(x // SQUARE_SIZE)  # Ensure it's an integer

        if 0 <= row < len(squares) and 0 <= col < len(squares[0]):
            return ball_rect.colliderect(squares[row][col]['rect']) and squares[row][col]['color'] != self.paint_color
        return False

    def change_square_color(self, squares, x, y):
        # Ensure x and y are within bounds
        x = max(0, min(x, WIDTH - 1))
        y = max(0, min(y, HEIGHT - 1))

        row = int(y // SQUARE_SIZE)
        col = int(x // SQUARE_SIZE)
        if 0 <= row < len(squares) and 0 <= col < len(squares[0]):
            squares[row][col]['color'] = self.paint_color

    def is_valid_position(self, x, y, squares):
        row = int(y // SQUARE_SIZE)  # Explicitly convert to integer
        col = int(x // SQUARE_SIZE)  # Explicitly convert to integer

        if x < 0 or x > WIDTH - BALL_SIZE or y < 0 or y > HEIGHT - BALL_SIZE:
            return False

        if 0 <= row < len(squares) and 0 <= col < len(squares[0]):
            square_color = squares[row][col]['color']
            return square_color == self.paint_color or square_color in [LEFT_COLOR, RIGHT_COLOR]

        return False

    def check_square_collision(self, squares, new_x, new_y):
        collision_occurred = False
        ball_rect = pygame.Rect(new_x, new_y, BALL_SIZE, BALL_SIZE)
        for row in squares:
            for square in row:
                if ball_rect.colliderect(square['rect']):
                    square['color'] = self.paint_color
                    collision_occurred = True
        return collision_occurred

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, BALL_SIZE, BALL_SIZE))

# Create squares
def create_squares():
    squares = []
    for y in range(0, HEIGHT, SQUARE_SIZE):
        row = []
        for x in range(0, WIDTH, SQUARE_SIZE):
            color = LEFT_COLOR if x < WIDTH / 2 else RIGHT_COLOR
            square = {'rect': pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE), 'color': color}
            row.append(square)
        squares.append(row)
    return squares

# Initialize balls and squares
left_ball = Ball(WIDTH // 4, HEIGHT // 2, WHITE, LEFT_COLOR)
right_ball = Ball(3 * WIDTH // 4, HEIGHT // 2, WHITE, RIGHT_COLOR)
squares = create_squares()

# Main game loop
running = True
while running:
    screen.fill((255, 255, 255))  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw squares
    for row in squares:
        for square in row:
            pygame.draw.rect(screen, square['color'], square['rect'])

    # Move and draw balls
    left_ball.move(squares)
    right_ball.move(squares)
    left_ball.draw()
    right_ball.draw()

    # Update the display
    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()