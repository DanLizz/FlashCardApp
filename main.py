import random
from tkinter import *
import random
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
fr_word = ""
en_word = ""
word_data = {}

# ---------------------------- WORD SETUP ------------------------------- #

try:
    data = pd.read_csv('data/words_to_learn.csv.csv')
except FileNotFoundError:
    original_data = pd.read_csv('data/french_words.csv')
    word_data = original_data.to_dict(orient="records")
else:
    word_data = data.to_dict(orient="records")


def next_card():
    global word_data, current_card, fr_word, en_word, flip_timer
    window.after_cancel(flip_timer)

    current_card = random.choice(word_data)
    fr_word = current_card["French"]
    en_word = current_card["English"]
    canvas.itemconfig(card_title, text="French")
    canvas.itemconfig(card_word, text=fr_word)

    canvas.itemconfig(card_background, image=card_image_fr)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=fr_word, fill="black")

    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_background, image=card_image_en)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=en_word, fill="white")


def is_known():
    word_data.remove(current_card)
    new_data = pd.DataFrame(word_data)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Language Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)


flip_timer = window.after(3000, func=flip_card)

fr = StringVar()
en = StringVar()

canvas = Canvas(width=800, height=526)
card_image_fr = PhotoImage(file="images/card_front.png")
card_image_en = PhotoImage(file="images/card_back.png")

canvas.grid(column=0, row=0, columnspan=2)
canvas.config(bd=0, highlightthickness=0, bg=BACKGROUND_COLOR)

card_background = canvas.create_image(400, 263, image=card_image_fr)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))

right = PhotoImage(file="images/right.png")
right_button = Button(image=right, bd=0, highlightthickness=0, relief="flat", command=is_known)
right_button.grid(column=0, row=1, sticky="n")

wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, bd=0, highlightthickness=0, relief="flat", command=next_card)
wrong_button.grid(column=1, row=1, sticky="n")

next_card()

window.mainloop()
