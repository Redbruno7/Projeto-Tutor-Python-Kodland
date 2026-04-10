import tkinter as tk
import random
import os
from PIL import Image, ImageTk


class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Memória")
        self.root.configure(bg="#1e1e2f")
        self.root.state("zoomed")

        self.after_id = None

        self.show_menu()

    # ---------------- MENU ----------------
    def show_menu(self):
        self.clear_screen()

        container = tk.Frame(self.root, bg="#1e1e2f")
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.configure(padx=40, pady=30)

        tk.Label(
            container,
            text="Jogo da Memória",
            font=("Arial", 32, "bold"),
            bg="#1e1e2f",
            fg="white"
        ).pack(pady=20)

        tk.Label(
            container,
            text="Escolha o nível",
            font=("Arial", 18),
            bg="#1e1e2f",
            fg="white"
        ).pack(pady=10)

        self.create_menu_button("Fácil (4 pares)", 4, container)
        self.create_menu_button("Médio (6 pares)", 6, container)
        self.create_menu_button("Difícil (8 pares)", 8, container)

    def create_menu_button(self, text, pairs, parent):
        tk.Button(
            parent,
            text=text,
            width=20,
            font=("Arial", 14, "bold"),
            bg="#2d2d44",
            fg="white",
            activebackground="#444466",
            command=lambda: self.start_game(pairs)
        ).pack(pady=8)

    # ---------------- INICIAR JOGO ----------------
    def start_game(self, pairs):
        self.pairs = pairs
        self.setup_game()
        self.create_widgets()

    # ---------------- CONFIGURAÇÃO ----------------
    def setup_game(self):
        all_images = [
            "images/arcade.png",
            "images/block.png",
            "images/bomba.png",
            "images/escudo.png",
            "images/espada.png",
            "images/fone.png",
            "images/joystick.png",
            "images/pc.png"
        ]

        selected = all_images[:self.pairs]

        self.cards = selected * 2
        random.shuffle(self.cards)

        base_path = os.path.dirname(__file__)

        self.images = {}
        for path in set(self.cards):
            full_path = os.path.join(base_path, path)
            img = Image.open(full_path)
            img = img.resize((120, 120))
            self.images[path] = ImageTk.PhotoImage(img)

        back_path = os.path.join(base_path, "images", "back.png")
        img = Image.open(back_path)
        img = img.resize((120, 120))
        self.back_image = ImageTk.PhotoImage(img)

        self.buttons = []
        self.first = None
        self.second = None
        self.lock = False
        self.moves = 0
        self.matches = 0

    # ---------------- INTERFACE ----------------
    def create_widgets(self):
        self.clear_screen()

        container = tk.Frame(self.root, bg="#1e1e2f")
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.configure(padx=20, pady=20)

        self.label_moves = tk.Label(
            container,
            text="Jogadas: 0",
            font=("Arial", 18, "bold"),
            bg="#1e1e2f",
            fg="white"
        )
        self.label_moves.grid(row=0, column=0, columnspan=4, pady=15)

        cols = 4
        rows = len(self.cards) // cols

        for i in range(len(self.cards)):
            btn = tk.Button(
                container,
                image=self.back_image,
                width=120,
                height=120,
                bg="#2d2d44",
                command=lambda i=i: self.reveal(i)
            )
            btn.grid(row=1 + i // cols, column=i % cols, padx=10, pady=10)
            self.buttons.append(btn)

        tk.Button(
            container,
            text="Reiniciar",
            bg="#2d2d44",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.restart_game
        ).grid(row=rows + 2, column=0, columnspan=2, pady=15)

        tk.Button(
            container,
            text="Voltar",
            bg="#2d2d44",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.show_menu
        ).grid(row=rows + 2, column=2, columnspan=2, pady=15)

    # ---------------- LÓGICA ----------------
    def reveal(self, index):
        if self.lock:
            return

        btn = self.buttons[index]
        if btn["state"] == "disabled":
            return

        btn.config(image=self.images[self.cards[index]])

        if self.first is None:
            self.first = index
        elif self.second is None and index != self.first:
            self.second = index
            self.moves += 1
            self.label_moves.config(text=f"Jogadas: {self.moves}")

            self.lock = True
            self.after_id = self.root.after(800, self.check_match)

    def check_match(self):
        if self.cards[self.first] == self.cards[self.second]:
            self.buttons[self.first].config(bg="#4CAF50")
            self.buttons[self.second].config(bg="#4CAF50")

            self.buttons[self.first].config(state="disabled")
            self.buttons[self.second].config(state="disabled")

            self.matches += 1

            self.first = None
            self.second = None
            self.lock = False

        else:
            self.buttons[self.first].config(bg="#F44336")
            self.buttons[self.second].config(bg="#F44336")

            self.after_id = self.root.after(500, self.reset_cards)

        if self.matches == self.pairs:
            self.show_victory()

    def reset_cards(self):
        if self.first is None or self.second is None:
            return

        self.buttons[self.first].config(image=self.back_image, bg="#2d2d44")
        self.buttons[self.second].config(image=self.back_image, bg="#2d2d44")

        self.first = None
        self.second = None
        self.lock = False

    # ---------------- RESULTADO ----------------
    def show_victory(self):
        tk.Label(
            self.root,
            text=f"Você venceu em {self.moves} jogadas!",
            font=("Arial", 18, "bold"),
            bg="#1e1e2f",
            fg="#4CAF50"
        ).place(relx=0.5, rely=0.85, anchor="center")

    # ---------------- UTIL ----------------
    def restart_game(self):
        self.start_game(self.pairs)

    def clear_screen(self):
        if self.after_id:
            try:
                self.root.after_cancel(self.after_id)
            except:
                pass
            self.after_id = None

        for widget in self.root.winfo_children():
            widget.destroy()


root = tk.Tk()
game = MemoryGame(root)
root.mainloop()
