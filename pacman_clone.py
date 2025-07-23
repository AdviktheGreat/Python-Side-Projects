import pygame
import sys
import random
import copy

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 20
MAZE_WIDTH = 30  # Width of our maze
MAZE_HEIGHT = 26  # Height of our maze
WINDOW_WIDTH = MAZE_WIDTH * CELL_SIZE
WINDOW_HEIGHT = MAZE_HEIGHT * CELL_SIZE

# Game States
GAME_PLAYING = 0
GAME_OVER = 1
GAME_WIN = 2

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)

# Maze layout (1 = wall, 0 = path, 2 = dot, 3 = power pellet)
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,2,1],
    [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1,2,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1,2,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,1,0,0,0,0,1,1,0,1,1,2,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,2,0,0,0,1,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1,2,1],
    [1,2,2,2,1,1,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,1,1,2,2,2,1,2,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1,1,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,3,1,1,2,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,2,1,1,1,1,2,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0  # 0=right, 1=down, 2=left, 3=up
        self.next_direction = 0
        self.speed = 8  # Higher number = slower movement
        self.move_counter = 0
        
    def update(self):
        # Check if we can change direction
        if self.move_counter == 0:
            next_x, next_y = self.get_next_position(self.next_direction)
            if self.can_move_to(next_x, next_y):
                self.direction = self.next_direction
        
        # Move in current direction
        if self.move_counter <= 0:
            next_x, next_y = self.get_next_position(self.direction)
            if self.can_move_to(next_x, next_y):
                self.x, self.y = next_x, next_y
                self.move_counter = self.speed
        
        if self.move_counter > 0:
            self.move_counter -= 1
    
    def get_next_position(self, direction):
        if direction == 0:  # right
            return (self.x + 1) % MAZE_WIDTH, self.y
        elif direction == 1:  # down
            return self.x, self.y + 1
        elif direction == 2:  # left
            return (self.x - 1) % MAZE_WIDTH, self.y
        elif direction == 3:  # up
            return self.x, self.y - 1
        
    def can_move_to(self, x, y):
        if y < 0 or y >= MAZE_HEIGHT:
            return False
        return MAZE[y][x] != 1
    
    def set_direction(self, direction):
        self.next_direction = direction

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.randint(0, 3)
        self.speed = 8
        self.move_counter = 0
        self.mode = "chase"  # chase, scatter, frightened
        self.frightened_timer = 0
        
    def update(self, player_x, player_y):
        if self.frightened_timer > 0:
            self.frightened_timer -= 1
            if self.frightened_timer == 0:
                self.mode = "chase"
        
        if self.move_counter <= 0:
            if self.mode == "frightened":
                # Random movement when frightened
                directions = []
                for d in range(4):
                    next_x, next_y = self.get_next_position(d)
                    if self.can_move_to(next_x, next_y):
                        directions.append(d)
                if directions:
                    self.direction = random.choice(directions)
            else:
                # Simple AI: try to move toward player
                self.chase_player(player_x, player_y)
            
            next_x, next_y = self.get_next_position(self.direction)
            if self.can_move_to(next_x, next_y):
                self.x, self.y = next_x, next_y
                self.move_counter = self.speed
            else:
                # Change direction if blocked
                self.direction = random.randint(0, 3)
        
        if self.move_counter > 0:
            self.move_counter -= 1
    
    def chase_player(self, player_x, player_y):
        # Simple pathfinding - move toward player
        dx = player_x - self.x
        dy = player_y - self.y
        
        possible_directions = []
        
        # Try horizontal movement first
        if abs(dx) > abs(dy):
            if dx > 0:
                possible_directions.append(0)  # right
            elif dx < 0:
                possible_directions.append(2)  # left
            if dy > 0:
                possible_directions.append(1)  # down
            elif dy < 0:
                possible_directions.append(3)  # up
        else:
            if dy > 0:
                possible_directions.append(1)  # down
            elif dy < 0:
                possible_directions.append(3)  # up
            if dx > 0:
                possible_directions.append(0)  # right
            elif dx < 0:
                possible_directions.append(2)  # left
        
        # Try each direction in order of preference
        for direction in possible_directions:
            next_x, next_y = self.get_next_position(direction)
            if self.can_move_to(next_x, next_y):
                self.direction = direction
                return
        
        # If no good direction found, try any valid direction
        for d in range(4):
            next_x, next_y = self.get_next_position(d)
            if self.can_move_to(next_x, next_y):
                self.direction = d
                return
    
    def get_next_position(self, direction):
        if direction == 0:  # right
            return (self.x + 1) % MAZE_WIDTH, self.y
        elif direction == 1:  # down
            return self.x, self.y + 1
        elif direction == 2:  # left
            return (self.x - 1) % MAZE_WIDTH, self.y
        elif direction == 3:  # up
            return self.x, self.y - 1
    
    def can_move_to(self, x, y):
        if y < 0 or y >= MAZE_HEIGHT:
            return False
        return MAZE[y][x] != 1
    
    def set_frightened(self):
        self.mode = "frightened"
        self.frightened_timer = 300  # 5 seconds at 60 FPS

def generate_maze(level):
    """Generate different maze layouts for each level"""
    maze = copy.deepcopy(MAZE)
    
    if level == 1:
        # Level 2: Add more walls randomly
        for y in range(2, MAZE_HEIGHT-2):
            for x in range(2, MAZE_WIDTH-2):
                if maze[y][x] == 2 and random.randint(0, 4) == 0:
                    maze[y][x] = 1
    elif level == 2:
        # Level 3: Create a more complex pattern
        for y in range(3, MAZE_HEIGHT-3, 3):
            for x in range(3, MAZE_WIDTH-3, 4):
                if maze[y][x] == 2:
                    maze[y][x] = 1
                    if x+1 < MAZE_WIDTH-1:
                        maze[y][x+1] = 1
    
    # Add power pellets in corners
    maze[3][1] = 3
    maze[3][MAZE_WIDTH-2] = 3
    maze[MAZE_HEIGHT-4][1] = 3
    maze[MAZE_HEIGHT-4][MAZE_WIDTH-2] = 3
    
    return maze

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 32)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pac-Man Clone")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 48)
        
        self.reset_game()
        
    def reset_game(self):
        """Reset game to initial state"""
        global MAZE
        self.level = 1
        self.max_levels = 3
        self.score = 0
        self.lives = 3
        self.game_state = GAME_PLAYING
        
        # Reset to original maze for level 1
        MAZE = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,2,1],
            [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,3,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1,2,1],
            [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1,2,1],
            [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,2,1,1,0,1,1,0,0,0,0,1,1,0,1,1,2,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,2,0,0,0,1,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1,2,1],
            [1,2,2,2,1,1,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,1,1,2,2,2,1,2,1],
            [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1,1,1],
            [1,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,3,1,1,2,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,2,1,1,1,1,2,3,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
        
        self.setup_level()
        
    def setup_level(self):
        """Setup a new level"""
        # Reset player and ghosts
        self.player = Player(14, 23)
        self.ghosts = [
            Ghost(14, 11, RED),
            Ghost(13, 11, PINK),
            Ghost(15, 11, CYAN),
            Ghost(16, 11, ORANGE)
        ]
        
        self.dots_collected = 0
        self.total_dots = sum(row.count(2) + row.count(3) for row in MAZE)
        
        # Create buttons for game over/win screens
        button_width, button_height = 150, 50
        button_y = WINDOW_HEIGHT // 2 + 50
        self.restart_button = Button(WINDOW_WIDTH // 2 - button_width - 10, button_y, 
                                   button_width, button_height, "Restart", GRAY, WHITE)
        self.quit_button = Button(WINDOW_WIDTH // 2 + 10, button_y, 
                                button_width, button_height, "Quit", GRAY, WHITE)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == GAME_PLAYING:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.set_direction(0)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.set_direction(1)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.set_direction(2)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.set_direction(3)
                elif event.key == pygame.K_r:
                    # Restart game
                    self.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state in [GAME_OVER, GAME_WIN]:
                    if self.restart_button.is_clicked(event.pos):
                        self.reset_game()
                    elif self.quit_button.is_clicked(event.pos):
                        return False
        return True
    
    def update(self):
        if self.game_state != GAME_PLAYING:
            return
            
        self.player.update()
        
        # Check dot collection
        cell_value = MAZE[self.player.y][self.player.x]
        if cell_value == 2:  # Regular dot
            MAZE[self.player.y][self.player.x] = 0
            self.score += 10
            self.dots_collected += 1
        elif cell_value == 3:  # Power pellet
            MAZE[self.player.y][self.player.x] = 0
            self.score += 50
            self.dots_collected += 1
            # Make ghosts frightened
            for ghost in self.ghosts:
                ghost.set_frightened()
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.player.x, self.player.y)
            
            # Check collision with player
            if ghost.x == self.player.x and ghost.y == self.player.y:
                if ghost.mode == "frightened":
                    # Ghost eaten
                    self.score += 200
                    ghost.x, ghost.y = 14, 11  # Reset ghost position
                    ghost.mode = "chase"
                    ghost.frightened_timer = 0
                else:
                    # Player loses life
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_state = GAME_OVER
                    else:
                        # Reset positions
                        self.player.x, self.player.y = 14, 23
                        for i, g in enumerate(self.ghosts):
                            g.x, g.y = 14 + i - 2, 11
        
        # Check win condition
        if self.dots_collected >= self.total_dots:
            self.level_complete()
    
    def level_complete(self):
        """Handle level completion"""
        global MAZE
        self.level += 1
        
        if self.level > self.max_levels:
            # All levels completed!
            self.game_state = GAME_WIN
        else:
            # Generate new maze for next level
            MAZE = generate_maze(self.level - 1)
            self.setup_level()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.game_state == GAME_PLAYING:
            # Draw maze
            for y in range(MAZE_HEIGHT):
                for x in range(MAZE_WIDTH):
                    cell = MAZE[y][x]
                    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    
                    if cell == 1:  # Wall
                        pygame.draw.rect(self.screen, BLUE, rect)
                    elif cell == 2:  # Dot
                        center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
                        pygame.draw.circle(self.screen, WHITE, center, 2)
                    elif cell == 3:  # Power pellet
                        center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
                        pygame.draw.circle(self.screen, WHITE, center, 6)
            
            # Draw player
            player_rect = pygame.Rect(
                self.player.x * CELL_SIZE + 2,
                self.player.y * CELL_SIZE + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4
            )
            pygame.draw.ellipse(self.screen, YELLOW, player_rect)
            
            # Draw ghosts
            for ghost in self.ghosts:
                ghost_rect = pygame.Rect(
                    ghost.x * CELL_SIZE + 2,
                    ghost.y * CELL_SIZE + 2,
                    CELL_SIZE - 4,
                    CELL_SIZE - 4
                )
                color = (0, 0, 128) if ghost.mode == "frightened" else ghost.color
                pygame.draw.ellipse(self.screen, color, ghost_rect)
            
            # Draw UI
            small_font = pygame.font.Font(None, 24)
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
            level_text = self.font.render(f"Level: {self.level}", True, WHITE)
            instructions1 = small_font.render("Use Arrow Keys or WASD to move", True, WHITE)
            instructions2 = small_font.render("Press R to restart", True, WHITE)
            
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))
            self.screen.blit(level_text, (10, 90))
            self.screen.blit(instructions1, (WINDOW_WIDTH - 250, 10))
            self.screen.blit(instructions2, (WINDOW_WIDTH - 250, 35))
            
        elif self.game_state == GAME_OVER:
            # Game Over Screen
            title = self.big_font.render("GAME OVER", True, RED)
            subtitle = self.font.render("Bad luck! Better luck next time!", True, WHITE)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
            subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            
            self.screen.blit(title, title_rect)
            self.screen.blit(subtitle, subtitle_rect)
            self.screen.blit(score_text, score_rect)
            
            # Draw buttons
            self.restart_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            
        elif self.game_state == GAME_WIN:
            # Win Screen
            title = self.big_font.render("CONGRATULATIONS!", True, GREEN)
            subtitle = self.font.render("You've completed all 3 levels!", True, WHITE)
            subtitle2 = self.font.render("You are a Pac-Man master!", True, YELLOW)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
            subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
            subtitle2_rect = subtitle2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            
            self.screen.blit(title, title_rect)
            self.screen.blit(subtitle, subtitle_rect)
            self.screen.blit(subtitle2, subtitle2_rect)
            self.screen.blit(score_text, score_rect)
            
            # Draw buttons
            self.restart_button.draw(self.screen)
            self.quit_button.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
