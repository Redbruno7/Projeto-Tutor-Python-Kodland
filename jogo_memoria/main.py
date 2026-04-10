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
        self.timer_id = None

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
        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, "images")

        all_images = [
            "arcade.png", "block.png", "bomba.png", "escudo.png",
            "espada.png", "fone.png", "joystick.png", "pc.png"
        ]

        selected = all_images[:self.pairs]

        self.cards = selected * 2
        random.shuffle(self.cards)

        self.images = {}
        for name in set(self.cards):
            img = Image.open(os.path.join(image_path, name))
            img = img.resize((120, 120))
            self.images[name] = ImageTk.PhotoImage(img)

        back_img = Image.open(os.path.join(image_path, "back.png"))
        back_img = back_img.resize((120, 120))
        self.back_image = ImageTk.PhotoImage(back_img)

        self.buttons = []
        self.first = None
        self.second = None
        self.lock = False
        self.moves = 0
        self.matches = 0

        # TIMER
        self.seconds = 0
        self.timer_running = False

    # ---------------- INTERFACE ----------------
    def create_widgets(self):
        self.clear_screen()

        container = tk.Frame(self.root, bg="#1e1e2f")
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.configure(padx=20, pady=20)

        self.label_timer = tk.Label(
            container,
            text="Tempo: 0s",
            font=("Arial", 16),
            bg="#1e1e2f",
            fg="white"
        )
        self.label_timer.grid(row=0, column=0, columnspan=2)

        self.label_moves = tk.Label(
            container,
            text="Jogadas: 0",
            font=("Arial", 16, "bold"),
            bg="#1e1e2f",
            fg="white"
        )
        self.label_moves.grid(row=0, column=2, columnspan=2)

        cols = 4

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
        ).grid(row=(len(self.cards)//4) + 2, column=0, columnspan=2, pady=15)

        tk.Button(
            container,
            text="Voltar",
            bg="#2d2d44",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.show_menu
        ).grid(row=(len(self.cards)//4) + 2, column=2, columnspan=2, pady=15)

        # inicia timer
        self.timer_running = True
        self.update_timer()

    # ---------------- TIMER ----------------
    def update_timer(self):
        if self.timer_running:
            self.seconds += 1
            self.label_timer.config(text=f"Tempo: {self.seconds}s")
            self.timer_id = self.root.after(1000, self.update_timer)

    # ---------------- ANIMAÇÃO ----------------
    def animate_flip(self, button, new_image):
        def shrink(width):
            if width > 20:
                button.config(width=width)
                self.root.after(10, lambda: shrink(width - 10))
            else:
                button.config(image=new_image)
                expand(20)

        def expand(width):
            if width < 120:
                button.config(width=width)
                self.root.after(10, lambda: expand(width + 10))
            else:
                button.config(width=120)

        shrink(120)

    # ---------------- LÓGICA ----------------
    def reveal(self, index):
        if self.lock:
            return

        btn = self.buttons[index]
        if btn["state"] == "disabled":
            return

        self.animate_flip(btn, self.images[self.cards[index]])

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
            self.buttons[self.first].config(bg="#4CAF50", state="disabled")
            self.buttons[self.second].config(bg="#4CAF50", state="disabled")

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

        self.animate_flip(self.buttons[self.first], self.back_image)
        self.animate_flip(self.buttons[self.second], self.back_image)

        self.buttons[self.first].config(bg="#2d2d44")
        self.buttons[self.second].config(bg="#2d2d44")

        self.first = None
        self.second = None
        self.lock = False

    # ---------------- RESULTADO ----------------
    def show_victory(self):
        self.timer_running = False

        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        tk.Label(
            self.root,
            text=f"Você venceu em {self.moves} jogadas e {self.seconds}s!",
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

        if self.timer_id:
            try:
                self.root.after_cancel(self.timer_id)
            except:
                pass
            self.timer_id = None

        for widget in self.root.winfo_children():
            widget.destroy()


root = tk.Tk()
game = MemoryGame(root)
root.mainloop()
