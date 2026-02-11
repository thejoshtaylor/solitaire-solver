# Solitaire solver
# Copyright (c) 2026 Joshua Taylor

SUITS = ["♥", "♦", "♣", "♠"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]


def standard_deck():
    """
    Generate a standard deck of 52 playing cards.

    :return: A list representing a standard deck of cards
    :rtype: list
    """
    return [f"{rank}{suit}" for suit in SUITS for rank in RANKS]


def is_red(card):
    """
    Check if a card is red (hearts or diamonds).

    :param card: The card to check
    :return: True if the card is red, False otherwise
    :rtype: bool
    """
    return card[1] in ["♥", "♦"]


def shuffled(deck, num_decks=1):
    """
    Generate num_decks shuffled versions of a given deck of cards.

    :param deck: The deck of cards to shuffle
    :param num_decks: The number of shuffled decks to generate
    :return: A generator yielding each shuffled deck
    :rtype: Generator[list, None, None]
    """
    import random

    for _ in range(num_decks):
        shuffled_deck = deck[:]
        random.shuffle(shuffled_deck)
        yield shuffled_deck
