import tkinter as tk
import random
from functools import partial
from collections import Counter
from tkinter import messagebox
import json
import pygame

global play_again

pygame.init()

correto = pygame.mixer.Sound("correto.mp3")
errado = pygame.mixer.Sound("errado.mp3")
fim = pygame.mixer.Sound("fim.mp3")
inicio = pygame.mixer.Sound("inicio.mp3")

file = open("dictionary.json")
dictionary = json.load(file)
words = list(dictionary.keys())
random.shuffle(words)

def shuffle_word(word):
    word_list = list(word)
    random.shuffle(word_list)
    return ''.join(word_list)

def update_score():
    global score
    score += 1
    score_label.config(text="Guessed words: {}".format(score))
    correto.play()

def check_word():
    global current_word_index
    guess = guess_entry.get().lower()
    if guess == words[current_word_index]:
        update_score()
        current_word_index += 1
        if current_word_index == len(words):
            game_over()
        else:
            shuffle_word_label.config(text=shuffle_word(words[current_word_index]))
            hint_label.config(text="Tip: {}".format(dictionary[words[current_word_index]]))
            guess_entry.delete(0, tk.END)
    else:
        errado.play()
        messagebox.showinfo("Wrong answer", "The word entered is incorrect. Try again.")
        guess_entry.delete(0, tk.END)

def check_word_enter(event):
    check_word()

def game_over():
    global timer_running, play_again
    timer_running = False
    fim.play()
    messagebox.showinfo("Game Over", "Game Over! Guessed words: {}".format(score))
    play_again = messagebox.askyesno("Play again?", "Want to play again?")
    if play_again:
        reset_game()
    else:
        window.destroy()

def reset_game():
    global current_word_index, score, timer_running, time_left
    current_word_index = 0
    score = 0
    timer_running = True
    time_left = 90
    inicio.play()
    word = words[current_word_index]
    shuffle_word_label.config(text=shuffle_word(word))
    hint_label.config(text="Tip: {}".format(dictionary[word]))
    score_label.config(text="Guessed words: {}".format(score))
    start_timer()
    new_word_index = current_word_index
    while new_word_index == current_word_index:
        new_word_index = random.randint(0, len(words)-1)
    current_word_index = new_word_index
    word = words[current_word_index]
    shuffle_word_label.config(text=shuffle_word(word))
    hint_label.config(text="Tip: {}".format(dictionary[word]))

def start_timer():
    global timer_running, time_left
    if timer_running:
        if time_left > 0:
            time_left -= 1
            time_label.config(text="Time left: {} seconds".format(time_left))
            window.after(1000, start_timer)
        else:
            game_over()

window = tk.Tk()
window.title("Anagram Game")
window.geometry("1920x1080")
window.configure(bg='#F5F5F5')

shuffle_word_label = tk.Label(window, text=shuffle_word(words[0]), font=("Gotham Black", 36), bg="#F5F5F5", fg="#00A7E1")
shuffle_word_label.pack(pady=30)
hint_label = tk.Label(window, text="Tip: {}".format(dictionary[words[0]]), font=("Arial", 14), bg="#F5F5F5", fg="#00171F", wraplength=1000)
hint_label.pack(pady=30)
score_label = tk.Label(window, text="Guessed words: 0", font=("Arial", 18), bg="#F5F5F5", fg="#00171F")
score_label.pack(pady=5)
time_label = tk.Label(window, text="Time left: 90 seconds", font=("Arial", 18), bg="#F5F5F5", fg="#00171F")
time_label.pack(pady=5)

guess_entry = tk.Entry(window, font=("Arial", 24), bg="#F5F5F5", fg="#00171F")
guess_entry.pack(pady=25)
guess_entry.focus()

guess_entry.bind("<Return>", check_word_enter)

check_button = tk.Button(window, text="Check", font=("Gotham Black", 24), bg="#00A7E1", fg="#FFFFFF", command=check_word)
check_button.pack()

current_word_index = 0
score = 0
time_left = 90
timer_running = True

reset_game()

def close_game(event):
    window.destroy()

window.bind("<Control-d>", close_game)

window.mainloop()