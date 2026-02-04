import pygame
import numpy as np
import random
from gym import Env
from gym.spaces import Discrete, Box
from stable_baselines3 import PPO

# Initialize Pygame
pygame.init()

# Constants
SCREEN_SIZE = 600
GRID_ROWS = 8
GRID_COLS = 10
CELL_SIZE = SCREEN_SIZE // GRID_COLS

# Power hierarchy
ELEMENT_POWER = {
    "Earth": "Water",
    "Water": "Fire",
    "Fire": "Air",
    "Air": "Earth"
}

# Colors
COLORS = {
    "Neutral": (200, 200, 200),
    "Creationist_Earth": (34, 139, 34),
    "Creationist_Water": (0, 0, 255),
    "Creationist_Fire": (255, 0, 0),
    "Creationist_Air": (255, 255, 0),
    "Creationist_Man": (255, 165, 0),
    "Creationist_Woman": (255, 140, 0),
    "Evolutionist_Earth": (34, 139, 34),
    "Evolutionist_Water": (0, 0, 255),
    "Evolutionist_Fire": (255, 0, 0),
    "Evolutionist_Air": (255, 255, 0),
    "Evolutionist_Man": (128, 0, 128),
    "Evolutionist_Woman": (147, 112, 219),
}

class OriginsEnv(Env):
    def __init__(self):
        super(OriginsEnv, self).__init__()
        self.action_space = Discrete(GRID_ROWS * GRID_COLS)
        self.turn = "Creationist"  # AI starts first
        self.observation_space = Box(
            low=-3, high=3, shape=(GRID_ROWS * GRID_COLS + 20,), dtype=np.int32
        )
        self.reset()

    def reset(self):
        self.board = [["Neutral"] * GRID_COLS for _ in range(GRID_ROWS)]
        
        # Creationist pieces (top row - AI controlled)
        self.board[0][0], self.board[0][9] = "Creationist_Earth", "Creationist_Earth"
        self.board[0][1], self.board[0][8] = "Creationist_Water", "Creationist_Water"
        self.board[0][2], self.board[0][7] = "Creationist_Fire", "Creationist_Fire"
        self.board[0][3], self.board[0][6] = "Creationist_Air", "Creationist_Air"
        self.board[0][4], self.board[0][5] = "Creationist_Woman", "Creationist_Man"
        
        # Evolutionist pieces (bottom row - human controlled)
        self.board[7][0], self.board[7][9] = "Evolutionist_Earth", "Evolutionist_Earth"
        self.board[7][1], self.board[7][8] = "Evolutionist_Water", "Evolutionist_Water"
        self.board[7][2], self.board[7][7] = "Evolutionist_Fire", "Evolutionist_Fire"
        self.board[7][3], self.board[7][6] = "Evolutionist_Air", "Evolutionist_Air"
        self.board[7][4], self.board[7][5] = "Evolutionist_Woman", "Evolutionist_Man"
        
        # Track positions and destination rows
        self.creationist_male_pos = (0, 5)
        self.creationist_female_pos = (0, 4)
        self.creationist_male_dest = 6  # Day 6 for Creationist
        self.creationist_female_dest = 6
        
        self.evolutionist_male_pos = (7, 5)
        self.evolutionist_female_pos = (7, 4)
        self.evolutionist_male_dest = 1  # 6 million years for Evolutionist
        self.evolutionist_female_dest = 1
        
        # Track if male/female have reached destination
        self.creationist_male_arrived = False
        self.creationist_female_arrived = False
        self.evolutionist_male_arrived = False
        self.evolutionist_female_arrived = False
        
        return self.get_observation()

    def get_observation(self):
        observation = np.zeros((GRID_ROWS * GRID_COLS + 20,), dtype=np.int32)
        piece_encoding = {
            "Neutral": 0,
            "Creationist_Earth": 1, "Creationist_Water": 2, 
            "Creationist_Fire": 3, "Creationist_Air": 4,
            "Creationist_Woman": 5, "Creationist_Man": 6,
            "Evolutionist_Earth": -1, "Evolutionist_Water": -2,
            "Evolutionist_Fire": -3, "Evolutionist_Air": -4,
            "Evolutionist_Woman": -5, "Evolutionist_Man": -6
        }
        
        index = 0
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                observation[index] = piece_encoding.get(self.board[row][col], 0)
                index += 1
        
        # Add game state information
        observation[index] = 1 if self.turn == "Creationist" else -1
        index += 1
        observation[index] = 1 if self.creationist_male_arrived else 0
        index += 1
        observation[index] = 1 if self.creationist_female_arrived else 0
        index += 1
        observation[index] = 1 if self.evolutionist_male_arrived else 0
        index += 1
        observation[index] = 1 if self.evolutionist_female_arrived else 0
        
        return observation

    def step(self, action):
        # Decode action into row and column
        row = action // GRID_COLS
        col = action % GRID_COLS
        
        # Ensure action is within bounds
        if not (0 <= row < GRID_ROWS and 0 <= col < GRID_COLS):
            return self.get_observation(), -1, False, {}
        
        # Only proceed if it's a valid piece for the current player
        piece = self.board[row][col]
        if (self.turn == "Creationist" and not piece.startswith("Creationist")) or \
           (self.turn == "Evolutionist" and not piece.startswith("Evolutionist")):
            return self.get_observation(), -1, False, {}
        
        valid_moves = self.get_valid_moves(row, col)
        
        if valid_moves:
            # Choose the first valid move
            end_row, end_col = valid_moves[0]
            self.move_piece((row, col), (end_row, end_col))
            reward = 1
        else:
            reward = -1
        
        done = self.check_game_over()
        if done:
            reward = 100 if "Creationist" in self.turn else -100
        
        # Switch turns
        self.turn = "Evolutionist" if self.turn == "Creationist" else "Creationist"
        return self.get_observation(), reward, done, {}

    def move_piece(self, start, end):
        sr, sc = start
        er, ec = end
        piece = self.board[sr][sc]
        faction = "Creationist" if piece.startswith("Creationist") else "Evolutionist"
    
    # Convert neutral squares along path for elements
        if any(el in piece for el in ["Earth", "Water", "Fire", "Air"]):
            dr = 1 if er > sr else -1 if er < sr else 0
            dc = 1 if ec > sc else -1 if ec < sc else 0
            r, c = sr + dr, sc + dc
        
            element_type = piece.split("_")[-1]
        
            while (r, c) != (er, ec):
                if self.board[r][c] == "Neutral":
                    self.board[r][c] = f"{faction}_{element_type}"
                r += dr
                c += dc
    
    # Check if male/female reached destination
        if piece.endswith("Man"):
            if faction == "Creationist" and er == self.creationist_male_dest:
                self.creationist_male_arrived = True
            elif faction == "Evolutionist" and er == self.evolutionist_male_dest:
                self.evolutionist_male_arrived = True
            
        elif piece.endswith("Woman"):
            if faction == "Creationist" and er == self.creationist_female_dest:
                self.creationist_female_arrived = True
            elif faction == "Evolutionist" and er == self.evolutionist_female_dest:
                self.evolutionist_female_arrived = True
    
    # Handle male/female position tracking
        if piece.endswith("Man") or piece.endswith("Woman"):
            if piece == "Creationist_Man":
                self.creationist_male_pos = (er, ec)
            elif piece == "Creationist_Woman":
                self.creationist_female_pos = (er, ec)
            elif piece == "Evolutionist_Man":
                self.evolutionist_male_pos = (er, ec)
            elif piece == "Evolutionist_Woman":
                self.evolutionist_female_pos = (er, ec)
    
    # Handle captures along the path
        self.capture_elements(start, end)
    
    # Move the piece
        self.board[er][ec] = piece
        self.board[sr][sc] = "Neutral"
    
    def capture_elements(self, start, end):
        sr, sc = start
        er, ec = end
        moving_piece = self.board[sr][sc]
    
    # Only elemental pieces can capture
        if not any(el in moving_piece for el in ["Earth", "Water", "Fire", "Air"]):
            return

        piece_element = moving_piece.split("_")[-1]
        faction = "Creationist" if moving_piece.startswith("Creationist") else "Evolutionist"
    
        dr = 1 if er > sr else -1 if er < sr else 0
        dc = 1 if ec > sc else -1 if ec < sc else 0
        r, c = sr + dr, sc + dc
    
        while (r, c) != (er, ec):
            target = self.board[r][c]
        
        # Handle male/female capture
            if target.endswith("Man") or target.endswith("Woman"):
            # Get the element under the male/female
                element_under = None
            # Check if the square itself is an element (for starting positions)
                if any(el in self.board[r][c] for el in ["Earth", "Water", "Fire", "Air"]):
                    element_under = self.board[r][c].split("_")[-1]
                else:
                # Check adjacent squares for the element
                    for dr_check, dc_check in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nr, nc = r + dr_check, c + dc_check
                        if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                            adjacent = self.board[nr][nc]
                            if any(el in adjacent for el in ["Earth", "Water", "Fire", "Air"]):
                                element_under = adjacent.split("_")[-1]
                                break
            
            # Only capture if moving element is dominant over the element under
                if element_under and ELEMENT_POWER[piece_element] == element_under:
                # Neutralize the square (convert to Neutral)
                    self.board[r][c] = "Neutral"
                # Remove the male/female piece
                    if target == "Creationist_Man":
                        self.creationist_male_pos = None
                    elif target == "Creationist_Woman":
                        self.creationist_female_pos = None
                    elif target == "Evolutionist_Man":
                        self.evolutionist_male_pos = None
                    elif target == "Evolutionist_Woman":
                        self.evolutionist_female_pos = None
        
        # Handle regular element capture
            elif target != "Neutral":
                target_element = None
                for el in ["Earth", "Water", "Fire", "Air"]:
                    if el in target:
                        target_element = el
                        break
            
                if target_element:
                # Stronger element captures weaker
                    if ELEMENT_POWER[piece_element] == target_element:
                        self.board[r][c] = "Neutral"
        
            r += dr
            c += dc
    
    def check_game_over(self):
        # Check if either side has won
        if self.creationist_male_arrived and self.creationist_female_arrived:
            print("Creationists win by reaching destination!")
            return True
        if self.evolutionist_male_arrived and self.evolutionist_female_arrived:
            print("Evolutionists win by reaching destination!")
            return True
            
        # Check if either side has lost their male or female
        creationist_alive = (self.creationist_male_pos is not None or self.creationist_male_arrived) and \
                          (self.creationist_female_pos is not None or self.creationist_female_arrived)
        evolutionist_alive = (self.evolutionist_male_pos is not None or self.evolutionist_male_arrived) and \
                            (self.evolutionist_female_pos is not None or self.evolutionist_female_arrived)
        
        if not creationist_alive:
            if not evolutionist_alive:
                print("Game is a draw - both sides lost male or female!")
            else:
                print("Evolutionists win - Creationists lost male or female!")
            return True
            
        if not evolutionist_alive:
            print("Creationists win - Evolutionists lost male or female!")
            return True
            
        # Check for stalemate (no valid moves)
        if not self.has_valid_moves():
            print("Game is a draw - no valid moves!")
            return True
            
        return False

    def has_valid_moves(self):
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                piece = self.board[row][col]
                if (self.turn == "Creationist" and piece.startswith("Creationist")) or \
                   (self.turn == "Evolutionist" and piece.startswith("Evolutionist")):
                    if self.get_valid_moves(row, col):
                        return True
        return False

    def get_valid_moves(self, row, col):
        moves = []
        if not (0 <= row < GRID_ROWS and 0 <= col < GRID_COLS):
            return moves
        
        piece = self.board[row][col]
        faction = "Creationist" if piece.startswith("Creationist") else "Evolutionist"
        starting_row = 0 if faction == "Creationist" else 7
    
    # Male/Female pieces can move to adjacent elemental squares
        if piece.endswith("Man") or piece.endswith("Woman"):
        # Check if already arrived at destination
            if (piece == "Creationist_Man" and self.creationist_male_arrived) or \
            (piece == "Creationist_Woman" and self.creationist_female_arrived) or \
            (piece == "Evolutionist_Man" and self.evolutionist_male_arrived) or \
            (piece == "Evolutionist_Woman" and self.evolutionist_female_arrived):
                return moves  # Can't move after arriving at destination
        
            for dr, dc in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                nr, nc = row + dr, col + dc
            
            # Check bounds
                if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                    target = self.board[nr][nc]
                
                # Can only move to elemental squares (not neutral)
                    if any(el in target for el in ["Earth", "Water", "Fire", "Air"]):
                    # Strict no-backwards movement (except when capturing bases)
                        if (faction == "Creationist" and nr <= row and nr != 7) or \
                        (faction == "Evolutionist" and nr >= row and nr != 0):
                            continue
                        
                    # Can't move through arrived pieces
                        if ((nr, nc) == self.creationist_male_pos and self.creationist_male_arrived) or \
                        ((nr, nc) == self.creationist_female_pos and self.creationist_female_arrived) or \
                        ((nr, nc) == self.evolutionist_male_pos and self.evolutionist_male_arrived) or \
                        ((nr, nc) == self.evolutionist_female_pos and self.evolutionist_female_arrived):
                            continue
                        
                        moves.append((nr, nc))
    
    # Elemental pieces move according to their rules
        elif any(el in piece for el in ["Earth", "Water", "Fire", "Air"]):
            directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                path_clear = True
            
                while 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS and path_clear:
                    target = self.board[nr][nc]
                
                # Can't move through arrived pieces
                    if ((nr, nc) == self.creationist_male_pos and self.creationist_male_arrived) or \
                    ((nr, nc) == self.creationist_female_pos and self.creationist_female_arrived) or \
                    ((nr, nc) == self.evolutionist_male_pos and self.evolutionist_male_arrived) or \
                    ((nr, nc) == self.evolutionist_female_pos and self.evolutionist_female_arrived):
                        path_clear = False
                        break
                
                # Check if target is neutral or same element
                    if target == "Neutral":
                        moves.append((nr, nc))
                        nr += dr
                        nc += dc
                        continue
                
                # Check if target is same element
                    if target == piece:
                        moves.append((nr, nc))
                        nr += dr
                        nc += dc
                        continue
                
                # Check if target is another element
                    target_element = None
                    for el in ["Earth", "Water", "Fire", "Air"]:
                        if el in target:
                            target_element = el
                            break
                
                    if target_element:
                        piece_element = piece.split("_")[-1]
                    
                    # Check element hierarchy
                        if ELEMENT_POWER[piece_element] == target_element:
                        # Can capture/neutralize weaker element (including at bases)
                            moves.append((nr, nc))
                    # Equal elements block movement
                        elif ELEMENT_POWER[target_element] == piece_element or target_element == piece_element:
                            path_clear = False
                        else:
                        # Weaker element, can't move here
                            path_clear = False
                        break
                
                # If target is male/female, can move through if we can neutralize the element
                    if target.endswith("Man") or target.endswith("Woman"):
                    # Need to check the element under the male/female
                    # For simplicity, we'll assume they're on an element (not neutral)
                        moves.append((nr, nc))
                        nr += dr
                        nc += dc
                    else:
                        path_clear = False
    
        return moves

# Game setup
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Origins Game")
game_env = OriginsEnv()
model = PPO("MlpPolicy", game_env, verbose=1)

def draw_board():
    screen.fill((255, 255, 255))
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            piece = game_env.board[row][col]
            color = COLORS.get(piece, (200, 200, 200))
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
            font = pygame.font.SysFont(None, 24)
            text_content = piece.split("_")[-1] if "_" in piece else piece
            text = font.render(text_content, True, (0, 0, 0))
            screen.blit(text, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
    
    # Draw grid
    for i in range(GRID_ROWS + 1):
        pygame.draw.line(screen, (0, 0, 0), (0, i * CELL_SIZE), (SCREEN_SIZE, i * CELL_SIZE))
    for i in range(GRID_COLS + 1):
        pygame.draw.line(screen, (0, 0, 0), (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_SIZE))
    
    # Draw turn indicator
    font = pygame.font.SysFont(None, 36)
    turn_text = font.render(f"Current Turn: {game_env.turn}", True, (0, 0, 0))
    screen.blit(turn_text, (10, SCREEN_SIZE - 30))
    
    # Draw destination indicators
    dest_font = pygame.font.SysFont(None, 24)
    creationist_dest = dest_font.render("Creationist Dest: Row 6", True, (255, 165, 0))
    evolutionist_dest = dest_font.render("Evolutionist Dest: Row 1", True, (128, 0, 128))
    screen.blit(creationist_dest, (SCREEN_SIZE - 200, SCREEN_SIZE - 60))
    screen.blit(evolutionist_dest, (SCREEN_SIZE - 200, SCREEN_SIZE - 30))
    
    pygame.display.flip()

# Main game loop
# ... (keep all your existing code the same until the main game loop)

# Main game loop
running = True
selected_piece = None
valid_moves = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col, row = x // CELL_SIZE, y // CELL_SIZE
            
            # Human player's turn (Evolutionist)
            if game_env.turn == "Evolutionist":
                piece = game_env.board[row][col]
                
                # If no piece selected yet, try to select an Evolutionist piece
                if selected_piece is None:
                    if piece.startswith("Evolutionist"):
                        selected_piece = (row, col)
                        valid_moves = game_env.get_valid_moves(row, col)
                        print(f"Selected {piece} at ({row},{col})")
                        print(f"Valid moves: {valid_moves}")
                
                # If we have a selected piece, try to move it
                elif selected_piece:
                    if (row, col) in valid_moves:
                        print(f"Moving from {selected_piece} to ({row},{col})")
                        game_env.move_piece(selected_piece, (row, col))
                        game_env.turn = "Creationist"  # Switch to AI's turn
                        selected_piece = None
                        valid_moves = []
                    else:
                        # Clicked on invalid square - reset selection
                        selected_piece = None
                        valid_moves = []
    
    # AI's turn (Creationist)
    if game_env.turn == "Creationist":
        # Get all possible Creationist pieces with valid moves
        possible_moves = []
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                piece = game_env.board[row][col]
                if piece.startswith("Creationist"):
                    moves = game_env.get_valid_moves(row, col)
                    if moves:
                        for move in moves:
                            possible_moves.append(((row, col), move))
        
        if possible_moves:
            # Randomly select a move from all possible moves
            start, end = random.choice(possible_moves)
            game_env.move_piece(start, end)
            print(f"AI (Creationist) moved {game_env.board[end[0]][end[1]]} from {start} to {end}")
            game_env.turn = "Evolutionist"
        else:
            print("AI (Creationist) couldn't find a valid move! Passing turn.")
            game_env.turn = "Evolutionist"
    
    # Draw the board
    draw_board()
    
    # Highlight selected piece and valid moves
    if selected_piece:
        row, col = selected_piece
        pygame.draw.rect(screen, (0, 255, 0), 
                         (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
        
        for move_row, move_col in valid_moves:
            pygame.draw.rect(screen, (0, 255, 255), 
                             (move_col * CELL_SIZE, move_row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
    
    pygame.display.flip()
    pygame.time.delay(100)  # Small delay to prevent high CPU usage

pygame.quit()