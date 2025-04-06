import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Player vs AI")
        
        # Game state
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'  # Human is X, AI is O
        self.game_over = False
        
        # UI Setup
        self.setup_ui()
        
        # Start the game
        self.update_status()
    
    def setup_ui(self):
        """Initialize the game UI"""
        # Colors
        self.bg_color = "#f0f0f0"
        self.button_bg = "#ffffff"
        self.button_active_bg = "#e0e0e0"
        self.status_bg = "#e0e0e0"
        self.font = ("Arial", 12)
        self.button_font = ("Arial", 24, "bold")
        
        self.root.configure(bg=self.bg_color)
        
        # Status label
        self.status_label = tk.Label(
            self.root, 
            text="", 
            font=self.font, 
            bg=self.status_bg,
            height=2,
            relief=tk.SUNKEN
        )
        self.status_label.pack(fill=tk.X, padx=5, pady=5)
        
        # Game board frame
        self.board_frame = tk.Frame(self.root, bg=self.bg_color)
        self.board_frame.pack(padx=10, pady=10)
        
        # Create buttons for the game board
        self.buttons = []
        for i in range(9):
            row, col = divmod(i, 3)
            button = tk.Button(
                self.board_frame,
                text=" ",
                font=self.button_font,
                bg=self.button_bg,
                activebackground=self.button_active_bg,
                width=2,
                height=1,
                command=lambda idx=i: self.on_button_click(idx)
            )
            button.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(button)
        
        # Restart button
        self.restart_button = tk.Button(
            self.root,
            text="Restart Game",
            font=self.font,
            bg=self.button_bg,
            activebackground=self.button_active_bg,
            command=self.reset_game
        )
        self.restart_button.pack(fill=tk.X, padx=50, pady=10)
    
    def on_button_click(self, position):
        """Handle player move"""
        if self.game_over or self.current_player != 'X' or self.board[position] != ' ':
            return
        
        self.make_move(position, 'X')
        
        if not self.game_over:
            self.current_player = 'O'
            self.update_status()
            self.root.after(1000, self.ai_move)  # Small delay for AI move
    
    def ai_move(self):
        """AI makes a move"""
        if self.game_over or self.current_player != 'O':
            return
        
        # Simple AI logic (could be replaced with more complex logic)
        position = self.find_best_move()
        self.make_move(position, 'O')
        self.current_player = 'X'
        self.update_status()
    
    def find_best_move(self):
        """Find the best move for the AI using simple rules"""
        # 1. Check if AI can win in the next move
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                if self.check_winner() == 'O':
                    self.board[i] = ' '
                    return i
                self.board[i] = ' '
        
        # 2. Check if player can win in the next move and block them
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'X'
                if self.check_winner() == 'X':
                    self.board[i] = ' '
                    return i
                self.board[i] = ' '
        
        # 3. Try to take the center if available
        if self.board[4] == ' ':
            return 4
        
        # 4. Try to take a corner if available
        corners = [0, 2, 6, 8]
        available_corners = [i for i in corners if self.board[i] == ' ']
        if available_corners:
            return random.choice(available_corners)
        
        # 5. Take any available edge
        edges = [1, 3, 5, 7]
        available_edges = [i for i in edges if self.board[i] == ' ']
        if available_edges:
            return random.choice(available_edges)
        
        # Fallback (shouldn't happen if game isn't over)
        return random.choice([i for i in range(9) if self.board[i] == ' '])
    
    def make_move(self, position, player):
        """Make a move on the board"""
        self.board[position] = player
        self.buttons[position].config(text=player)
        
        winner = self.check_winner()
        if winner:
            self.game_over = True
            self.show_game_result(winner)
        elif ' ' not in self.board:
            self.game_over = True
            self.show_game_result(None)  # Draw
        else:
            self.update_status()
    
    def check_winner(self):
        """Check if there's a winner"""
        # Check rows
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != ' ':
                return self.board[i]
        
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != ' ':
                return self.board[i]
        
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != ' ':
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != ' ':
            return self.board[2]
        
        return None
    
    def show_game_result(self, winner):
        """Show game result message"""
        if winner:
            message = f"Player {'X' if winner == 'X' else 'AI (O)'} wins!"
        else:
            message = "It's a draw!"
        
        messagebox.showinfo("Game Over", message)
        self.update_status()
    
    def update_status(self):
        """Update the status label"""
        if self.game_over:
            winner = self.check_winner()
            if winner:
                status = f"Game Over - {'You (X)' if winner == 'X' else 'AI (O)'} wins!"
            else:
                status = "Game Over - It's a draw!"
        else:
            status = f"Your turn (X)" if self.current_player == 'X' else "AI is thinking..."
        
        self.status_label.config(text=status)
    
    def reset_game(self):
        """Reset the game state"""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        
        for button in self.buttons:
            button.config(text=' ')
        
        self.update_status()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()