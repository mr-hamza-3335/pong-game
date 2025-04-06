import tkinter as tk
from tkinter import messagebox
import random
import pygame
import os
import sys

pygame.mixer.init()

# Correct Sound Path Handling
BASE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

def load_sound(filename):
    path = os.path.join(BASE_PATH, "assets", filename)
    return pygame.mixer.Sound(path)

# Load Sounds Properly
bounce_sound = load_sound("bounce.wav")
score_sound = load_sound("score.wav")
gameover_sound = load_sound("gameover.wav")

# Global Variables
player1_name = ""
player2_name = ""
difficulty = "Medium"
game_speed = 7
score1 = 0
score2 = 0
score_limit = 10
winner_text = None

root = tk.Tk()
root.title("🏓 Ultimate Pong Game")
root.geometry("800x600")
root.config(bg="#1e1e1e")

canvas = tk.Canvas(root, width=800, height=500, bg="#0f0f0f", highlightthickness=0)
canvas.pack()

# Paddle & Ball
paddle_height = 100
paddle_width = 15
ball_radius = 20

paddle1 = canvas.create_rectangle(20, 200, 20 + paddle_width, 200 + paddle_height, fill="cyan")
paddle2 = canvas.create_rectangle(765, 200, 765 + paddle_width, 200 + paddle_height, fill="magenta")

ball = canvas.create_oval(390, 240, 390 + ball_radius, 240 + ball_radius, fill="red", outline="red")

ball_dx = game_speed
ball_dy = game_speed

score_label = tk.Label(root, text="", font=("Courier", 18), fg="yellow", bg="#1e1e1e")
score_label.pack()

# ➕ Add your footer here
footer_label = tk.Label(root, text="Created by Ameer Hamza", font=("Courier", 10), fg="white", bg="#1e1e1e")
footer_label.pack(side="bottom", pady=5)

keys_pressed = set()

def key_press(event):
    keys_pressed.add(event.keysym)

def key_release(event):
    keys_pressed.discard(event.keysym)

def move_paddles():
    if "w" in keys_pressed and canvas.coords(paddle1)[1] > 0:
        canvas.move(paddle1, 0, -15)
    if "s" in keys_pressed and canvas.coords(paddle1)[3] < 500:
        canvas.move(paddle1, 0, 15)
    if "Up" in keys_pressed and canvas.coords(paddle2)[1] > 0:
        canvas.move(paddle2, 0, -15)
    if "Down" in keys_pressed and canvas.coords(paddle2)[3] < 500:
        canvas.move(paddle2, 0, 15)

def update_score():
    score_label.config(text=f"{player1_name}: {score1}     {player2_name}: {score2}")

def reset_ball():
    global ball_dx, ball_dy
    canvas.coords(ball, 390, 240, 390 + ball_radius, 240 + ball_radius)
    ball_dx *= random.choice([-1, 1])
    ball_dy *= random.choice([-1, 1])

def show_game_over(winner):
    global winner_text
    gameover_sound.play()
    winner_text = canvas.create_text(400, 250, text=f"🏆 {winner} Wins!", font=("Courier", 36, "bold"), fill="gold")
    response = messagebox.askquestion("Game Over", f"{winner} won the game!\nDo you want to play again?")
    if response == "yes":
        restart_game()
    else:
        root.destroy()

def restart_game():
    global score1, score2, ball_dx, ball_dy, winner_text
    score1 = 0
    score2 = 0
    update_score()
    canvas.coords(paddle1, 20, 200, 20 + paddle_width, 200 + paddle_height)
    canvas.coords(paddle2, 765, 200, 765 + paddle_width, 200 + paddle_height)
    reset_ball()
    if winner_text:
        canvas.delete(winner_text)
        winner_text = None
    move_ball()

def move_ball():
    global ball_dx, ball_dy, score1, score2

    move_paddles()
    canvas.move(ball, ball_dx, ball_dy)

    ball_coords = canvas.coords(ball)
    paddle1_coords = canvas.coords(paddle1)
    paddle2_coords = canvas.coords(paddle2)

    if ball_coords[1] <= 0 or ball_coords[3] >= 500:
        ball_dy *= -1
        bounce_sound.play()

    if ball_coords[0] <= 0:
        score2 += 1
        update_score()
        score_sound.play()
        if score2 >= score_limit:
            show_game_over(player2_name)
            return
        reset_ball()

    if ball_coords[2] >= 800:
        score1 += 1
        update_score()
        score_sound.play()
        if score1 >= score_limit:
            show_game_over(player1_name)
            return
        reset_ball()

    if (ball_coords[0] <= paddle1_coords[2] and
        paddle1_coords[1] < ball_coords[3] and
        paddle1_coords[3] > ball_coords[1]):
        ball_dx *= -1
        bounce_sound.play()

    if (ball_coords[2] >= paddle2_coords[0] and
        paddle2_coords[1] < ball_coords[3] and
        paddle2_coords[3] > ball_coords[1]):
        ball_dx *= -1
        bounce_sound.play()

    root.after(20, move_ball)

def start_game():
    global player1_name, player2_name, difficulty, game_speed, ball_dx, ball_dy

    player1_name = entry_p1.get().strip() or "Player 1"
    player2_name = entry_p2.get().strip() or "Player 2"
    difficulty = difficulty_var.get()

    if difficulty == "Low":
        game_speed = 4
    elif difficulty == "Medium":
        game_speed = 7
    else:
        game_speed = 10

    ball_dx = game_speed
    ball_dy = game_speed

    update_score()
    start_frame.destroy()
    move_ball()

# Start Frame
start_frame = tk.Frame(root, bg="#111")
start_frame.place(x=200, y=120)

tk.Label(start_frame, text="Enter Player 1 Name:", fg="white", bg="#111", font=("Courier", 12)).pack(pady=5)
entry_p1 = tk.Entry(start_frame, font=("Courier", 12))
entry_p1.pack()

tk.Label(start_frame, text="Enter Player 2 Name:", fg="white", bg="#111", font=("Courier", 12)).pack(pady=5)
entry_p2 = tk.Entry(start_frame, font=("Courier", 12))
entry_p2.pack()

tk.Label(start_frame, text="Select Difficulty:", fg="white", bg="#111", font=("Courier", 12)).pack(pady=5)
difficulty_var = tk.StringVar(value="Medium")
tk.OptionMenu(start_frame, difficulty_var, "Low", "Medium", "High").pack()

tk.Button(start_frame, text="Start Game 🎮", command=start_game, font=("Courier", 14), bg="lime", fg="black").pack(pady=15)

root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

root.mainloop()
