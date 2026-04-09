import tkinter as tk
import random

# símbolos das cartas (pares)
symbols = ["🍎", "🍌", "🍇", "🍉", "🍒", "🥝"]
cards = symbols * 2
random.shuffle(cards)

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Memória")

        self.buttons = []
        self.first = None
        self.second = None
        self.lock = False

        self.create_board()

    def create_board(self):
        for i in range(12):
            btn = tk.Button(self.root, text="?", width=10, height=4,
                            command=lambda i=i: self.reveal(i))
            btn.grid(row=i//4, column=i%4)
            self.buttons.append(btn)

    def reveal(self, index):
        if self.lock:
            return

        btn = self.buttons[index]
        btn.config(text=cards[index])

        if self.first is None:
            self.first = index
        elif self.second is None and index != self.first:
            self.second = index
            self.root.after(1000, self.check_match)

    def check_match(self):
        if cards[self.first] == cards[self.second]:
            self.buttons[self.first].config(state="disabled")
            self.buttons[self.second].config(state="disabled")
        else:
            self.buttons[self.first].config(text="?")
            self.buttons[self.second].config(text="?")

        self.first = None
        self.second = None

root = tk.Tk()
game = MemoryGame(root)
root.mainloop()