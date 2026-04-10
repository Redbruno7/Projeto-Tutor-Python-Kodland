import tkinter as tk
import random


class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Memória")

        self.show_menu()

    # ---------------- MENU ----------------
    def show_menu(self):
        self.clear_screen()

        tk.Label(self.root, text="Escolha o nível",
                 font=("Arial", 16)).pack(pady=20)

        tk.Button(self.root, text="Fácil (4 pares)", width=20,
                  command=lambda: self.start_game(4)).pack(pady=5)

        tk.Button(self.root, text="Médio (6 pares)", width=20,
                  command=lambda: self.start_game(6)).pack(pady=5)

        tk.Button(self.root, text="Difícil (8 pares)", width=20,
                  command=lambda: self.start_game(8)).pack(pady=5)

    # ---------------- INICIAR JOGO ----------------
    def start_game(self, pairs):
        self.pairs = pairs
        self.setup_game()
        self.create_widgets()

    # ---------------- CONFIGURAÇÃO ----------------
    def setup_game(self):
        all_symbols = ["🍎", "🍌", "🍇", "🍉", "🍒", "🥝", "🍍", "🍓"]
        symbols = all_symbols[:self.pairs]

        self.cards = symbols * 2
        random.shuffle(self.cards)

        self.buttons = []
        self.first = None
        self.second = None
        self.lock = False
        self.moves = 0
        self.matches = 0

    # ---------------- INTERFACE ----------------
    def create_widgets(self):
        self.clear_screen()

        # Label de jogadas
        self.label_moves = tk.Label(
            self.root, text="Jogadas: 0", font=("Arial", 14))
        self.label_moves.grid(row=0, column=0, columnspan=4)

        # Definir colunas dinamicamente
        cols = 4
        rows = len(self.cards) // cols

        for i in range(len(self.cards)):
            btn = tk.Button(self.root, text="?", width=10, height=4,
                            command=lambda i=i: self.reveal(i))
            btn.grid(row=1 + i // cols, column=i % cols)
            self.buttons.append(btn)

        # Botões extras
        tk.Button(self.root, text="🔁 Reiniciar", command=self.restart_game)\
            .grid(row=rows + 2, column=0, columnspan=2, pady=10)

        tk.Button(self.root, text="⬅ Voltar", command=self.show_menu)\
            .grid(row=rows + 2, column=2, columnspan=2, pady=10)

    # ---------------- LÓGICA ----------------
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
            self.root.after(800, self.check_match)

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

        if self.matches == self.pairs:
            self.show_victory()

    # ---------------- RESULTADO ----------------
    def show_victory(self):
        tk.Label(self.root, text="🎉 Você venceu!", font=("Arial", 16))\
            .grid(row=10, column=0, columnspan=4)

    # ---------------- UTIL ----------------
    def restart_game(self):
        self.start_game(self.pairs)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


root = tk.Tk()
game = MemoryGame(root)
root.mainloop()
