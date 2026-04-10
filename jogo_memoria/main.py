import tkinter as tk
import random

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Memória")

        self.setup_game()
        self.create_widgets()

    def setup_game(self):
        symbols = ["🍎", "🍌", "🍇", "🍉", "🍒", "🥝"]
        self.cards = symbols * 2
        random.shuffle(self.cards)

        self.buttons = []
        self.first = None
        self.second = None
        self.lock = False
        self.moves = 0
        self.matches = 0

    def create_widgets(self):
        # Label de jogadas
        self.label_moves = tk.Label(self.root, text="Jogadas: 0", font=("Arial", 14))
        self.label_moves.grid(row=0, column=0, columnspan=4)

        # Tabuleiro
        for i in range(12):
            btn = tk.Button(self.root, text="?", width=10, height=4,
                            command=lambda i=i: self.reveal(i))
            btn.grid(row=1 + i//4, column=i%4)
            self.buttons.append(btn)

        # Botão de reiniciar
        self.btn_restart = tk.Button(self.root, text="🔁 Reiniciar", command=self.restart_game)
        self.btn_restart.grid(row=5, column=0, columnspan=4, pady=10)

    def reveal(self, index):
        if self.lock:
            return

        btn = self.buttons[index]
        if btn["state"] == "disabled":
            return

        btn.config(text=self.cards[index])

        if self.first is None:
            self.first = index
        elif self.second is None and index != self.first:
            self.second = index
            self.moves += 1
            self.label_moves.config(text=f"Jogadas: {self.moves}")

            self.lock = True
            self.root.after(1000, self.check_match)

    def check_match(self):
        if self.cards[self.first] == self.cards[self.second]:
            self.buttons[self.first].config(state="disabled")
            self.buttons[self.second].config(state="disabled")
            self.matches += 1
        else:
            self.buttons[self.first].config(text="?")
            self.buttons[self.second].config(text="?")

        self.first = None
        self.second = None
        self.lock = False

        # Verificar vitória
        if self.matches == 6:
            self.show_victory()

    def show_victory(self):
        victory_label = tk.Label(self.root, text="🎉 Você venceu!", font=("Arial", 16))
        victory_label.grid(row=6, column=0, columnspan=4)

    def restart_game(self):
        # limpar tela
        for widget in self.root.winfo_children():
            widget.destroy()

        # resetar jogo
        self.setup_game()
        self.create_widgets()


root = tk.Tk()
game = MemoryGame(root)
root.mainloop()