import time
import os
import random
import keyboard

class GameObject:
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char

class Ball(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 'O')
        self.vel_x = random.choice([-0.9, 0.9])  # Reduced initial velocity
        self.vel_y = 0.9  # Reduced initial velocity

class Cat(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, '^')
        self.width = 5
        self.speed = 2  # Increased cat speed

class Obstacle(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, '#')

class PowerUp(GameObject):
    def __init__(self, x, y, type):
        super().__init__(x, y, '*')
        self.type = type

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_frame(width, height, objects, score, lives):
    frame = [[' ' for _ in range(width)] for _ in range(height)]
    
    for obj in objects:
        if isinstance(obj, Cat):
            cat_art = [" /\\_/\\", " (o.o)", " > ^ <"]
            for i, row in enumerate(cat_art):
                for j, char in enumerate(row):
                    if 0 <= obj.x + j < width and obj.y + i < height:
                        frame[obj.y + i][obj.x + j] = char
        elif isinstance(obj, Ball):
            frame[int(obj.y)][int(obj.x)] = obj.char
        else:
            frame[obj.y][obj.x] = obj.char
    
    # Draw ground
    for i in range(width):
        frame[height-1][i] = "="
    
    frame_str = "\n".join("".join(row) for row in frame)
    frame_str += f"\nScore: {score} | Lives: {'❤' * lives}"
    return frame_str

def game_loop(width=40, height=25):
    ball = Ball(width // 2, 0)
    cat = Cat(width // 2 - 2, height - 4)
    objects = [ball, cat]
    score = 0
    lives = 3
    power_up_duration = 0
    power_up_type = None
    
    while lives > 0:
        # Handle input
        if keyboard.is_pressed('left') and cat.x > 0:
            cat.x -= cat.speed
        if keyboard.is_pressed('right') and cat.x < width - cat.width:
            cat.x += cat.speed
        if keyboard.is_pressed('q'):
            break

        # Update ball position
        ball.x += ball.vel_x
        ball.y += ball.vel_y

        # Bounce off walls
        if ball.x <= 0 or ball.x >= width - 1:
            ball.vel_x *= -1

        # Bounce off ceiling
        if ball.y <= 0:
            ball.vel_y *= -1

        # Check for catch
        if int(ball.y) == cat.y - 1 and cat.x <= int(ball.x) < cat.x + cat.width:
            score += 1
            ball.vel_y *= -1
            # Increase difficulty
            if score % 5 == 0:
                ball.vel_x *= 1.1  # Slightly increase speed
                ball.vel_y *= 1.1
                objects.append(Obstacle(random.randint(0, width-1), random.randint(5, height-6)))
            # Add power-up
            if random.random() < 0.2:
                power_up_type = random.choice(['wide', 'slow'])
                objects.append(PowerUp(random.randint(0, width-1), random.randint(5, height-6), power_up_type))

        # Check for miss
        if ball.y >= height - 1:
            lives -= 1
            ball.x, ball.y = width // 2, 0
            ball.vel_x = random.choice([-0.5, 0.5])
            ball.vel_y = 0.5

        # Handle obstacles and power-ups
        for obj in objects[:]:
            if isinstance(obj, Obstacle):
                if int(ball.x) == obj.x and int(ball.y) == obj.y:
                    ball.vel_x *= -1
                    ball.vel_y *= -1
            elif isinstance(obj, PowerUp):
                if int(ball.x) == obj.x and int(ball.y) == obj.y:
                    power_up_duration = 50
                    power_up_type = obj.type
                    objects.remove(obj)

        # Apply power-ups
        if power_up_duration > 0:
            if power_up_type == 'wide':
                cat.width = 7
            elif power_up_type == 'slow':
                ball.vel_x *= 0.5
                ball.vel_y *= 0.5
            power_up_duration -= 1
        else:
            cat.width = 5
            if power_up_type == 'slow':
                ball.vel_x *= 2
                ball.vel_y *= 2
                power_up_type = None

        # Draw and wait
        clear_console()
        print(draw_frame(width, height, objects, score, lives))
        time.sleep(0.1)

    print(f"Game Over! Final Score: {score}")

if __name__ == "__main__":
    print("Use left and right arrow keys to move the cat. Press 'q' to quit.")
    time.sleep(3)
    game_loop()