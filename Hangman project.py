import tkinter as tk
from pathlib import Path
import random


def load_words():
    word_file = Path(__file__).parent / "HangManWords.txt"

    with word_file.open("r", encoding="utf-8") as file:
        return [
            line.strip().lower()
            for line in file
            if line.strip()
        ]


class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.geometry("500x700")
        self.master.minsize(400, 600)
        self.master.configure(bg="lightblue")
        self.words = load_words()
        self.word = random.choice(self.words)
        self.guessed_letters = []
        self.incorrect_guesses = 0
        self.max_incorrect_guesses = 6
        self.create_widgets()
        

    def create_widgets(self):
        self.hangman_canvas = tk.Canvas(
            self.master,
            width=180,
            height=180,
            bg="lightblue",
            highlightthickness=0
        )
        self.hangman_canvas.pack(pady=5)

        self.word_label = tk.Label(self.master, text=self.get_display_word(), bg="lightblue")
        self.word_label.pack(pady=(5, 5))

        controls_frame = tk.Frame(self.master, bg="lightblue")
        controls_frame.pack(pady=5)

        self.guess_entry = tk.Entry(self.master)
        self.guess_entry.pack(in_=controls_frame)

        main_buttons_frame = tk.Frame(controls_frame, bg="lightblue")
        main_buttons_frame.pack(pady=(5, 0))

        self.letter_buttons = {}
        self.alphabet_frame = tk.Frame(self.master, bg="lightblue")
        self.alphabet_frame.pack(pady=20)

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        rows_per_column = 9
        for number, letter in enumerate(alphabet):
            row = number % rows_per_column
            column = number // rows_per_column

            button = tk.Button(
                self.alphabet_frame,
                text=letter.upper(),
                width=3,
                bg="#E7F3FA",
                activebackground="#B7D9EC",
                disabledforeground="#404040",
                command=lambda chosen_letter=letter: self.show_letter(chosen_letter)
            )
            button.grid(row=row, column=column, padx=2, pady=2)
            self.letter_buttons[letter] = button

        self.guess_button = tk.Button(main_buttons_frame, text="Guess", command=self.make_guess)
        self.guess_button.pack(side=tk.LEFT, padx=3)
        self.reset_button = tk.Button(main_buttons_frame, text="Reset", command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT, padx=3)
        self.quit_button = tk.Button(main_buttons_frame, text="Quit", command=self.master.quit)
        self.quit_button.pack(side=tk.LEFT, padx=3)
        self.incorrect_label = tk.Label(controls_frame, bg="lightblue", text=f"Incorrect guesses: {self.incorrect_guesses}/{self.max_incorrect_guesses}")
        self.incorrect_label.pack(pady=(5, 0))
        self.words_used_label = tk.Label(controls_frame, bg="lightblue", text=f"Letters used: {self.words_used_list()}")
        self.words_used_label.pack()
        self.result_label = tk.Label(controls_frame, bg="lightblue", text="Congratulations! You won!" if self.is_word_guessed() else "Congratulations! You lost!" if self.incorrect_guesses >= self.max_incorrect_guesses else "")
        self.result_label.pack()
        self.update_display()
        self.guess_entry.bind("<Return>", lambda event: self.make_guess())
        self.guess_entry.focus_set()
        self.master.bind("<Escape>", lambda event: self.master.quit())
        self.control_bindings(None)

    def show_letter(self, letter):
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.insert(0, letter)

    def control_bindings(self, event):
        self.master.bind("<Control-r>", lambda event: self.reset_game())
        self.master.bind("<Control-q>", lambda event: self.master.quit())
        # self.master.bind("<Control-n>", lambda event: self.new_game())
        # self.master.bind("<Control-h>", lambda event: self.show_help())
        # self.master.bind("<Control-s>", lambda event: self.save_game())
        # self.master.bind("<Control-l>", lambda event: self.load_game())
        # self.master.bind("<Control-p>", lambda event: self.show_stats())
        # self.master.bind("<Control-t>", lambda event: self.show_tips())
        # self.master.bind("<Control-a>", lambda event: self.show_about())
        # self.master.bind("<Control-f>", lambda event: self.show_feedback())
        


    def get_display_word(self):
        display = ""

        for letter in self.word:
            if letter.lower() in self.guessed_letters:
                display += letter
            else:
                display += "_"

        return display


    def is_word_guessed(self):
        return all(
            letter.lower() in self.guessed_letters
            for letter in self.word
        )

    def make_guess(self):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                self.result_label.config(text="You already guessed that letter.")
            elif guess in self.word.lower():
                self.guessed_letters.append(guess)
                self.result_label.config(text="Correct guess!")
            else:
                self.guessed_letters.append(guess)
                self.incorrect_guesses += 1
                self.result_label.config(text="Incorrect guess!")

            self.update_display()

    def words_used_list(self):
        return ", ".join(self.guessed_letters) or "None"

    def update_hangman(self):
        self.hangman_canvas.delete("all")

        # Draw the gallows first so it is visible from the beginning.
        self.hangman_canvas.create_line(25, 160, 155, 160, width=3)
        self.hangman_canvas.create_line(55, 160, 55, 20, width=3)
        self.hangman_canvas.create_line(55, 20, 125, 20, width=3)
        self.hangman_canvas.create_line(125, 20, 125, 45, width=3)

        if self.incorrect_guesses >= 1:
            self.hangman_canvas.create_oval(110, 45, 140, 75, width=3)
        if self.incorrect_guesses >= 2:
            self.hangman_canvas.create_line(125, 75, 125, 115, width=3)
        if self.incorrect_guesses >= 3:
            self.hangman_canvas.create_line(125, 85, 105, 105, width=3)
        if self.incorrect_guesses >= 4:
            self.hangman_canvas.create_line(125, 85, 145, 105, width=3)
        if self.incorrect_guesses >= 5:
            self.hangman_canvas.create_line(125, 115, 105, 145, width=3)
        if self.incorrect_guesses >= 6:
            self.hangman_canvas.create_line(125, 115, 145, 145, width=3)


    def update_display(self):
        self.word_label.config(text=self.get_display_word())
        self.incorrect_label.config(text=f"Incorrect guesses: {self.incorrect_guesses}/{self.max_incorrect_guesses}")
        self.words_used_label.config(text=f"Letters used: {self.words_used_list()}")
        self.update_hangman()

        for letter, button in self.letter_buttons.items():
            if letter in self.guessed_letters:
                button.config(
                    state=tk.DISABLED,
                    bg="#9E9E9E",
                    relief=tk.SUNKEN
                )
            else:
                button.config(
                    state=tk.NORMAL,
                    bg="#E7F3FA",
                    relief=tk.RAISED
                )

        if self.is_word_guessed():
            self.result_label.config(text="Congratulations! You won!")
            self.guess_button.config(state=tk.DISABLED)
            self.guess_entry.config(state=tk.DISABLED)
        elif self.incorrect_guesses >= self.max_incorrect_guesses:
            self.result_label.config(text=f"Game over! The word was: {self.word}")
            self.guess_button.config(state=tk.DISABLED)
            self.guess_entry.config(state=tk.DISABLED)

    def reset_game(self):
        self.guessed_letters = []
        self.incorrect_guesses = 0
        self.word = random.choice(self.words)
        self.update_display()
        self.result_label.config(text="")
        self.guess_button.config(state=tk.NORMAL)
        self.guess_entry.config(state=tk.NORMAL)
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus_set()

root = tk.Tk()
game = HangmanGame(root)
root.mainloop()