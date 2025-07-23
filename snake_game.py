#!/usr/bin/env python3
"""
Terminal Snake Game
A classic Snake game implementation using Python's curses library.

Controls:
- Arrow keys or WASD to move
- Q to quit
- R to restart after game over

"""

import curses
import random
import time
from enum import Enum
from typing import List, Tuple


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_screen()
        self.reset_game()
        
    def setup_screen(self):
        """Initialize the screen and colors."""
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(1)  # Non-blocking input
        self.stdscr.timeout(100)  # Refresh rate (milliseconds)
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)    # Game Over
        
        # Get screen dimensions
        self.height, self.width = self.stdscr.getmaxyx()
        self.game_height = self.height - 4  # Leave space for score and borders
        self.game_width = self.width - 2
        
    def reset_game(self):
        """Reset the game to initial state."""
        # Initialize snake in the center
        center_y = self.game_height // 2
        center_x = self.game_width // 2
        self.snake: List[Tuple[int, int]] = [
            (center_y, center_x),
            (center_y, center_x - 1),
            (center_y, center_x - 2)
        ]
        
        self.direction = Direction.RIGHT
        self.score = 0
        self.food = self.generate_food()
        self.game_over = False
        
    def generate_food(self) -> Tuple[int, int]:
        """Generate a random food position that's not on the snake."""
        while True:
            food_y = random.randint(1, self.game_height - 1)
            food_x = random.randint(1, self.game_width - 1)
            if (food_y, food_x) not in self.snake:
                return (food_y, food_x)
    
    def handle_input(self):
        """Handle user input for controlling the snake."""
        key = self.stdscr.getch()
        
        # Quit game
        if key in [ord('q'), ord('Q')]:
            return False
            
        # Restart game after game over
        if self.game_over and key in [ord('r'), ord('R')]:
            self.reset_game()
            return True
        
        if self.game_over:
            return True
            
        # Movement controls
        new_direction = None
        if key == curses.KEY_UP or key in [ord('w'), ord('W')]:
            new_direction = Direction.UP
        elif key == curses.KEY_DOWN or key in [ord('s'), ord('S')]:
            new_direction = Direction.DOWN
        elif key == curses.KEY_LEFT or key in [ord('a'), ord('A')]:
            new_direction = Direction.LEFT
        elif key == curses.KEY_RIGHT or key in [ord('d'), ord('D')]:
            new_direction = Direction.RIGHT
            
        # Prevent snake from reversing into itself
        if new_direction:
            current_dir = self.direction.value
            new_dir = new_direction.value
            if (current_dir[0] + new_dir[0] != 0 or 
                current_dir[1] + new_dir[1] != 0):
                self.direction = new_direction
        
        return True
    
    def update_snake(self):
        """Update snake position and handle collisions."""
        if self.game_over:
            return
            
        head = self.snake[0]
        new_head = (
            head[0] + self.direction.value[0],
            head[1] + self.direction.value[1]
        )
        
        # Check wall collision
        if (new_head[0] < 1 or new_head[0] >= self.game_height or
            new_head[1] < 1 or new_head[1] >= self.game_width):
            self.game_over = True
            return
            
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def draw(self):
        """Draw the game on the screen."""
        self.stdscr.clear()
        
        # Draw border
        for y in range(self.game_height + 1):
            self.stdscr.addch(y, 0, '|')
            self.stdscr.addch(y, self.game_width, '|')
        for x in range(self.game_width + 1):
            self.stdscr.addch(0, x, '-')
            self.stdscr.addch(self.game_height, x, '-')
        
        # Draw corners
        self.stdscr.addch(0, 0, '+')
        self.stdscr.addch(0, self.game_width, '+')
        self.stdscr.addch(self.game_height, 0, '+')
        self.stdscr.addch(self.game_height, self.game_width, '+')
        
        if not self.game_over:
            # Draw snake
            for i, (y, x) in enumerate(self.snake):
                char = '█' if i == 0 else '▓'  # Head is solid, body is lighter
                self.stdscr.addch(y, x, char, curses.color_pair(1))
            
            # Draw food
            self.stdscr.addch(self.food[0], self.food[1], '♦', curses.color_pair(2))
        
        # Draw score
        score_text = f"Score: {self.score}"
        self.stdscr.addstr(self.game_height + 1, 2, score_text, curses.color_pair(3))
        
        # Draw controls
        controls = "Controls: Arrow keys/WASD to move, Q to quit"
        self.stdscr.addstr(self.game_height + 2, 2, controls)
        
        if self.game_over:
            # Draw game over message
            game_over_msg = "GAME OVER!"
            restart_msg = "Press R to restart or Q to quit"
            
            msg_y = self.game_height // 2
            msg_x = (self.game_width - len(game_over_msg)) // 2
            restart_x = (self.game_width - len(restart_msg)) // 2
            
            self.stdscr.addstr(msg_y, msg_x, game_over_msg, curses.color_pair(4))
            self.stdscr.addstr(msg_y + 1, restart_x, restart_msg)
        
        self.stdscr.refresh()
    
    def run(self):
        """Main game loop."""
        while True:
            if not self.handle_input():
                break
                
            self.update_snake()
            self.draw()


def main(stdscr):
    """Main function to initialize and run the game."""
    try:
        game = SnakeGame(stdscr)
        game.run()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    # Check if terminal supports curses
    try:
        curses.wrapper(main)
    except curses.error:
        print("Error: This terminal doesn't support curses.")
        print("Try running the game in a standard terminal.")
    except Exception as e:
        print(f"An error occurred: {e}")
