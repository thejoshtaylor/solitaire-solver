# Solitaire solver
# Copyright (c) 2026 Joshua Taylor

import cards


def solve(deck):
    return None


class Solitaire:
    def __init__(self, deck):
        # The game state consists of the tableau (7 piles),
        # the foundation (4 piles), and the stock

        # The tableau is represented as a list of 7 tuples, where each tuple contains
        # a list of face-down cards and a list of face-up cards, respectively.
        self.tableau = [([], []) for _ in range(7)]
        self.foundation = [[] for _ in range(4)]
        self.stock = []

        self.build_game_state(deck[:])

    def __repr__(self):
        # Create a string representation of the game state for debugging
        foundation_str = " | ".join(
            f"{cards.SUITS[i]}{self.foundation[i][-1] if self.foundation[i] else '  '}"
            for i in range(4)
        )
        tableau_str = ""
        for i in range(
            max(len(self.tableau[i][0]) + len(self.tableau[i][1]) for i in range(7))
        ):
            for j in range(7):
                if i < len(self.tableau[j][0]):
                    tableau_str += f"[gray]{self.tableau[j][1][i - len(self.tableau[j][0])]}[/gray] | "
                elif i - len(self.tableau[j][0]) < len(self.tableau[j][1]):
                    is_red = cards.is_red(
                        self.tableau[j][1][i - len(self.tableau[j][0])]
                    )
                    if is_red:
                        tableau_str += f"[red]{self.tableau[j][1][i - len(self.tableau[j][0])]}[/red] | "
                    else:
                        tableau_str += f"[white]{self.tableau[j][1][i - len(self.tableau[j][0])]}[/white] | "
                else:
                    tableau_str += "   | "
            tableau_str = tableau_str[:-3] + "\n"

        return f"{foundation_str}\n\n{tableau_str}"

    def build_game_state(self, deck):
        # Build the initial tableau from the deck
        for i in range(7, 0, -1):
            for x in range(i - 1):
                self.tableau[7 - x][0].append(deck.pop(0))
            self.tableau[7 - i][1].append(deck.pop(0))
        self.stock = deck[:]

    def step(self):
        # Implement the logic to perform one step of the game
        pass

    def can_move_to_foundation(self, card):
        # Check if we can move this card to the foundation

        # If the foundation pile for this suit has a rank
        # that is one less than this card's rank, we can move it
        # or if the foundation pile is empty and this card is an Ace,
        # we can move it
        return (
            self.foundation[cards.SUITS.index(card[1])][-1][0]
            == cards.RANKS.index(card[0]) - 1
        ) or (not self.foundation[cards.SUITS.index(card[1])] and card[0] == "A")

    def move_to_foundation(self, tableau_index):
        # Move the top card of the specified tableau pile to the foundation
        card = self.tableau[tableau_index][1].pop()
        self.foundation[cards.SUITS.index(card[1])].append(card)

    def move_to_tableau(self, from_index, to_index):
        # Move the top stack of the specified tableau pile to another tableau pile
        stack = self.tableau[from_index][1][:]
        self.tableau[to_index][1].extend(stack)
        self.tableau[from_index][1] = []

    def new_top_card(self, tableau_index):
        # If there are no face-up cards in this tableau pile, flip the top face-down card
        if not self.tableau[tableau_index][1] and self.tableau[tableau_index][0]:
            self.tableau[tableau_index][1].append(self.tableau[tableau_index][0].pop())

    def solve_immediate(self):
        # Implement logic to solve any moves available on the tableau
        for i in range(7):
            face_up = self.tableau[i][1]
            if not face_up:
                continue

            # If there is only one face-up card, we need to do
            # everything we can to move it immediately
            if len(face_up) == 1:
                card = face_up[0]

                # Check if we can move this card to the foundation

                # If the foundation pile for this suit has a rank
                # that is one less than this card's rank, we can move it
                # or if the foundation pile is empty and this card is an Ace,
                # we can move it
                if self.can_move_to_foundation(card):
                    self.move_to_foundation(i)
                    self.new_top_card(i)
                    continue

                # Check if we can move this card to another tableau pile
                for j in range(7):
                    if j == i:
                        continue
                    other_face_up = self.tableau[j][1]
                    if not other_face_up:
                        continue
                    other_top_card = other_face_up[-1]
                    # We can move this card to another tableau pile if the top card of that pile is one rank higher and of opposite color
                    if cards.RANKS.index(other_top_card[0]) == cards.RANKS.index(
                        card[0]
                    ) + 1 and cards.is_red(other_top_card) != cards.is_red(card):
                        self.move_to_tableau(i, j)
                        self.new_top_card(i)
                        break

            # More than one face-up card
            else:
                bottom_card = face_up[0]
                top_card = face_up[-1]

                # Check if we can move this stack to another tableau pile
                for j in range(7):
                    if j == i:
                        continue
                    other_face_up = self.tableau[j][1]
                    if not other_face_up:
                        continue
                    other_top_card = other_face_up[-1]
                    # We can move this stack to another tableau pile if the top card of that pile is one rank higher and of opposite color than the bottom card of this stack
                    if cards.RANKS.index(other_top_card[0]) == cards.RANKS.index(
                        bottom_card[0]
                    ) + 1 and cards.is_red(other_top_card) != cards.is_red(bottom_card):
                        self.move_to_tableau(i, j)
                        self.new_top_card(i)
                        break
