import random
import tkinter as tk
from tkinter import messagebox

class PokdengGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Pokdeng Game")

        self.suits = ['♥', '♦', '♣', '♠']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = []

        self.player1_cards = []
        self.player1_points = 0
        self.player2_cards = []
        self.player2_points = 0
        self.extra_card_drawn_p2 = False

        self.create_widgets()

    def calculate_points(self, cards):
        total = sum(self.card_value(card[0]) for card in cards)
        return total % 10

    def card_value(self, rank):
        if rank in ['K', 'Q', 'J']:
            return 10
        elif rank == 'A':
            return 1
        else:
            return int(rank)

    def deal_cards(self, num_cards=2):
        return [self.deck.pop() for _ in range(num_cards)]

    def initialize_deck(self):
        self.deck = [(rank, suit) for rank in self.ranks for suit in self.suits]
        random.shuffle(self.deck)

    def display_cards(self, player, cards, total_points, show_all=True):
        if show_all or player == "Player 1":
            self.output_text.insert(tk.END, f"{player} cards: {self.format_cards(cards)}, Total Points: {total_points}\n")

    def format_cards(self, cards):
        return ', '.join(f'{rank}{suit}' for rank, suit in cards)

    def should_draw_extra_card_p2(self):
        return not self.extra_card_drawn_p2 and self.player2_points <= 5

    def draw_extra_card(self):
        extra_card = self.deal_cards(1).pop()
        self.player2_cards.append(extra_card)
        self.player2_points = self.calculate_points(self.player2_cards)
        self.display_cards("Player 2", self.player2_cards, self.player2_points)

    def play(self):
        self.initialize_deck()

        self.player1_cards = self.deal_cards()
        self.player1_points = self.calculate_points(self.player1_cards)

        self.player2_cards = self.deal_cards()
        self.player2_points = self.calculate_points(self.player2_cards)
        self.extra_card_drawn_p2 = False

        self.display_cards("Player 1", self.player1_cards, self.player1_points)
        self.display_cards("Player 2", [], 0, show_all=False)

        if self.player1_points == 8 or self.player1_points == 9:
            messagebox.showinfo("Result", "Player 1 Pokdeng!")
        elif self.player2_points == 8 or self.player2_points == 9:
            messagebox.showinfo("Result", "Player 2 Pokdeng!")
        else:
            choice = messagebox.askyesno("Draw Card", "Do you want to draw another card, Player 1?")

            extra_card_drawn_p1 = False

            while choice:
                if extra_card_drawn_p1:
                    messagebox.showinfo("Error", "You can only draw one extra card. No more cards can be drawn.")
                    break

                extra_card_p1 = self.deal_cards(1).pop()
                self.player1_cards.append(extra_card_p1)
                self.player1_points = self.calculate_points(self.player1_cards)

                self.display_cards("Player 1", self.player1_cards, self.player1_points)

                extra_card_drawn_p1 = True

                if self.player1_points >= 8:
                    break

                choice = messagebox.askyesno("Draw Card", "Do you want to draw another card, Player 1?")

            self.output_text.insert(tk.END, f"Player 1 final points: {self.player1_points}\n")

            # Announce Player 2's cards
            self.display_cards("Player 2", self.player2_cards, self.player2_points, show_all=True)

            # Decision for Player 2 (bot)
            draw_extra_card_p2 = self.should_draw_extra_card_p2()
            num_cards_drawn_p2 = 0

            while draw_extra_card_p2:
                self.draw_extra_card()

                num_cards_drawn_p2 += 1
                self.extra_card_drawn_p2 = True

                if num_cards_drawn_p2 >= 1 or self.player2_points >= 8:
                    break

                draw_extra_card_p2 = self.should_draw_extra_card_p2()

            self.output_text.insert(tk.END, f"Player 2 final points: {self.player2_points}\n")

        # Determine the winner
        if self.player1_points > self.player2_points:
            messagebox.showinfo("Winner", "Player 1 wins!")
        elif self.player2_points > self.player1_points:
            messagebox.showinfo("Winner", "Player 2 wins!")
        else:
            messagebox.showinfo("Result", "It's a tie!")

        play_again = messagebox.askyesno("Play Again", "Do you want to play again?")
        if play_again:
            self.output_text.insert(tk.END, "\n-------------------------\n")
            self.play()
        else:
            self.master.destroy()

    def create_widgets(self):
        self.output_text = tk.Text(self.master, height=20, width=50)
        self.output_text.pack()

        self.play_button = tk.Button(self.master, text="Play", command=self.play)
        self.play_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = PokdengGUI(root)
    root.mainloop()




