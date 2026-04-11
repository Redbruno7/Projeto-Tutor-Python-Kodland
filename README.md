# Jogo da Memória (Memory Game)

Um jogo da memória interativo desenvolvido em Python utilizando Tkinter, com interface gráfica moderna, múltiplos níveis de dificuldade e sistema de animação.

---

## Sobre o Projeto

Este projeto foi desenvolvido com o objetivo de praticar conceitos de:

- Programação orientada a objetos (POO)
- Manipulação de interface gráfica com Tkinter
- Controle de estado e lógica de jogo
- Manipulação de imagens com Pillow
- Organização e estruturação de código

O jogo permite ao usuário selecionar níveis de dificuldade e desafiar sua memória encontrando pares de cartas no menor tempo e com o menor número de jogadas possível.

---

## Funcionalidades

- Menu inicial com seleção de dificuldade:
  - Fácil (4 pares)
  - Médio (6 pares)
  - Difícil (8 pares)

- Sistema de jogo:
  - Cartas embaralhadas aleatoriamente
  - Contador de jogadas
  - Cronômetro em tempo real
  - Verificação automática de pares

- Interface:
  - Animação de flip nas cartas
  - Feedback visual (acerto/erro)
  - Layout centralizado e responsivo

- Controles:
  - Reiniciar jogo
  - Voltar ao menu principal

- Tela de vitória:
  - Exibição de desempenho (tempo + jogadas)

---

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Tkinter (interface gráfica)
- Pillow (manipulação de imagens)

---

## 📂 Estrutura do Projeto

```bash
memory-game/
│
├── images/
│   ├── arcade.png
│   ├── block.png
│   ├── bomba.png
│   ├── escudo.png
│   ├── espada.png
│   ├── fone.png
│   ├── joystick.png
│   ├── pc.png
│   └── back.png
│
├── main.py
├── requirements.txt
└── README.md