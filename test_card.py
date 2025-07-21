#!/usr/bin/env python
"""
Test Module for Card Class

This module contains comprehensive unit tests for the Card class functionality,
including initialization, comparison operators, trump card logic, and various
card attributes and methods.

Classes:
    TestCard: A test class containing all unit tests for the Card class.

Programmer: Michelle Talley
Copyright (c) 2025 Michelle Talley
"""

import unittest
from card import Card


class TestCard(unittest.TestCase):
    """
    Test class for the Card class containing comprehensive unit tests.
    """

    def setUp(self):
        """
        Set up test fixtures before each test method.
        Creates common Card objects used across multiple tests.
        """
        self.ace_spades = Card('Ace', 'Spades')
        self.king_hearts = Card('King', 'Hearts')
        self.ten_diamonds = Card('10', 'Diamonds')
        self.jack_clubs = Card('Jack', 'Clubs')
        self.jack_diamonds = Card('Jack', 'Diamonds')
        self.jack_hearts = Card('Jack', 'Hearts')
        self.jack_spades = Card('Jack', 'Spades')
        self.big_joker = Card('Big', 'Joker')
        self.little_joker = Card('Little', 'Joker')
        self.four_clubs = Card('4', 'Clubs')
        self.three_spades = Card('3', 'Spades')

    def test_card_initialization_valid(self):
        """Test that cards are initialized correctly with valid parameters."""
        card = Card('Ace', 'Spades')
        self.assertEqual(card.name, 'Ace')
        self.assertEqual(card.suit, 'Spades')
        self.assertEqual(card.short_name, 'A♠')
        self.assertEqual(card.symbol, 'A')
        self.assertEqual(card.rank, 17)
        self.assertEqual(card.points, 0)
        self.assertIsNone(card.trump_suit)

    def test_card_initialization_with_short_names(self):
        """Test card initialization with short name variants."""
        card_a = Card('A', 'Hearts')
        self.assertEqual(card_a.name, 'Ace')
        self.assertEqual(card_a.short_name, 'A♥')

        card_k = Card('K', 'Diamonds')
        self.assertEqual(card_k.name, 'King')
        self.assertEqual(card_k.short_name, 'K♦')

    def test_card_initialization_invalid_name(self):
        """Test that invalid card names raise ValueError."""
        with self.assertRaises(ValueError) as context:
            Card('Invalid', 'Spades')
        self.assertIn("Invalid card name", str(context.exception))

    def test_card_initialization_invalid_suit(self):
        """Test that invalid suits raise ValueError."""
        with self.assertRaises(ValueError) as context:
            Card('Ace', 'InvalidSuit')
        self.assertIn("Invalid suit", str(context.exception))

    def test_str_representation(self):
        """Test the string representation of cards."""
        self.assertEqual(str(self.ace_spades), ' A♠')
        self.assertEqual(str(self.king_hearts), ' K♥')
        self.assertEqual(str(self.ten_diamonds), '10♦')
        self.assertEqual(str(self.big_joker), ' BJ')
        self.assertEqual(str(self.little_joker), ' LJ')

    def test_repr_representation(self):
        """Test the repr representation of cards."""
        self.assertEqual(repr(self.ace_spades), ' A♠')
        self.assertEqual(repr(self.king_hearts), ' K♥')
        self.assertEqual(repr(self.big_joker), ' BJ')
        self.assertEqual(repr(self.little_joker), ' LJ')

    def test_base_symbol(self):
        """Test the base_symbol method."""
        self.assertEqual(self.ace_spades.base_symbol('Ace'), 'A')
        self.assertEqual(self.ace_spades.base_symbol('King'), 'K')
        self.assertEqual(self.ace_spades.base_symbol('10'), '10')
        self.assertEqual(self.ace_spades.base_symbol('Queen'), 'Q')
        self.assertEqual(self.ace_spades.base_symbol('Jack'), 'J')

    def test_desc(self):
        """Test the desc method returns correct descriptions."""
        self.assertEqual(self.ace_spades.desc(), 'Ace')
        self.assertEqual(self.king_hearts.desc(), 'King')
        self.assertEqual(self.ten_diamonds.desc(), '10')
        self.assertEqual(self.big_joker.desc(), 'Big Joker')
        self.assertEqual(self.little_joker.desc(), 'Little Joker')

    def test_state(self):
        """Test the state method returns card attributes."""
        state = self.ace_spades.state()
        self.assertIsInstance(state, dict)
        self.assertIn('name', state)
        self.assertIn('suit', state)
        self.assertIn('rank', state)

    def test_comparison_operators_no_trump(self):
        """Test comparison operators without trump suit set."""
        # Ace (rank 17) > King (rank 16)
        self.assertTrue(self.ace_spades > self.king_hearts)
        self.assertFalse(self.ace_spades < self.king_hearts)

        # King (rank 16) > 10 (rank 10)
        self.assertTrue(self.king_hearts > self.ten_diamonds)
        self.assertFalse(self.king_hearts < self.ten_diamonds)

    def test_comparison_operators_with_trump(self):
        """Test comparison operators with trump suit set."""
        # Set Spades as trump suit
        self.ace_spades.set_trump('Hearts')
        self.king_hearts.set_trump('Hearts')
        self.jack_diamonds.set_trump('Hearts')
        self.jack_hearts.set_trump('Hearts')

        self.assertFalse(self.ace_spades > self.king_hearts)
        self.assertTrue(self.ace_spades < self.king_hearts)

        self.assertTrue(self.jack_diamonds < self.jack_hearts)
        self.assertFalse(self.jack_diamonds > self.jack_hearts)

    def test_equality_operator(self):
        """Test the equality operator."""
        ace_spades_2 = Card('Ace', 'Spades')
        self.assertTrue(self.ace_spades == ace_spades_2)
        self.assertFalse(self.ace_spades == self.king_hearts)

    def test_is_trump_no_trump_suit(self):
        """Test is_trump method when no trump suit is set."""
        self.assertFalse(self.ace_spades.is_trump())
        self.assertFalse(self.jack_clubs.is_trump())

    def test_is_trump_with_trump_suit(self):
        """Test is_trump method with various trump suits."""
        # Test with Spades as trump
        self.assertTrue(self.ace_spades.is_trump('Spades'))
        self.assertFalse(self.king_hearts.is_trump('Spades'))

    def test_is_trump_off_jacks(self):
        """Test is_trump method for off jacks."""
        # Jack of Clubs should be trump when Spades is trump (off jack)
        self.assertTrue(self.jack_clubs.is_trump('Spades'))
        # Jack of Diamonds should be trump when Hearts is trump (off jack)
        self.assertTrue(self.jack_diamonds.is_trump('Hearts'))
        # Jack of Spades should be trump when Clubs is trump (off jack)
        self.assertTrue(self.jack_spades.is_trump('Clubs'))

    def test_is_trump_jokers(self):
        """Test is_trump method for jokers."""
        self.assertTrue(self.big_joker.is_trump('Spades'))
        self.assertTrue(self.little_joker.is_trump('Hearts'))

    def test_is_nontrump(self):
        """Test is_nontrump method."""
        self.assertTrue(self.ace_spades.is_nontrump('Hearts'))
        self.assertFalse(self.ace_spades.is_nontrump('Spades'))

    def test_get_trump_symbol(self):
        """Test get_trump_symbol method."""
        # Regular trump card
        self.assertEqual(self.ace_spades.get_trump_symbol('Spades'), 'A')
        # Non-trump card
        self.assertEqual(self.ace_spades.get_trump_symbol('Hearts'), 'N')
        # Off jack
        self.assertEqual(self.jack_clubs.get_trump_symbol('Spades'), 'X')
        # Regular jack
        self.assertEqual(self.jack_spades.get_trump_symbol('Spades'), 'J')
        self.jack_clubs.set_trump('Spades')
        self.assertEqual(self.jack_clubs.symbol, 'X')
        # Non-trump jack
        self.jack_diamonds.set_trump('Spades')
        self.assertEqual(self.jack_diamonds.symbol, 'N')

    def test_set_trump_no_suit(self):
        """Test set_trump method with no suit (reset)."""
        # First set trump, then reset
        self.ace_spades.set_trump('Spades')
        self.ace_spades.set_trump(None)

        self.assertEqual(self.ace_spades.symbol, 'A')
        self.assertEqual(self.ace_spades.rank, 17)
        self.assertEqual(self.ace_spades.points, 0)
        self.assertIsNone(self.ace_spades.trump_suit)

        self.jack_diamonds.set_trump('Spades')
        self.jack_diamonds.set_trump(None)

        self.assertEqual(self.jack_diamonds.symbol, 'J')
        self.assertEqual(self.jack_diamonds.rank, 14)
        self.assertEqual(self.jack_diamonds.points, 0)
        self.assertIsNone(self.jack_diamonds.trump_suit)

    def test_set_trump_with_suit(self):
        """Test set_trump method with a specific suit."""
        self.ace_spades.set_trump('Spades')

        self.assertEqual(self.ace_spades.symbol, 'A')
        self.assertEqual(self.ace_spades.rank, 17)
        self.assertEqual(self.ace_spades.points, 1)  # Trump cards get points
        self.assertEqual(self.ace_spades.trump_suit, 'Spades')

        self.jack_diamonds.set_trump('Spades')
        self.assertEqual(self.jack_diamonds.symbol, 'N')
        self.assertEqual(self.jack_diamonds.rank, 1)
        self.assertEqual(self.jack_diamonds.points, 0)
        self.assertEqual(self.jack_diamonds.trump_suit, 'Spades')

    def test_set_trump_off_jack(self):
        """Test set_trump method with off jack scenarios."""
        # Jack of Clubs when Spades is trump becomes off jack
        self.jack_clubs.set_trump('Spades')

        self.assertEqual(self.jack_clubs.symbol, 'X')
        self.assertEqual(self.jack_clubs.rank, 13)  # Off jack rank
        self.assertEqual(self.jack_clubs.points, 1)
        self.assertEqual(self.jack_clubs.trump_suit, 'Spades')

        self.jack_diamonds.set_trump('Spades')  # Non trump Jack for Spades
        self.assertEqual(self.jack_diamonds.symbol, 'N')  # Non-trump symbol
        self.assertEqual(self.jack_diamonds.rank, 1)      # Non-trump rank
        # No points for non-trump
        self.assertEqual(self.jack_diamonds.points, 0)
        self.assertEqual(self.jack_diamonds.trump_suit, 'Spades')

    def test_set_trump_regular_jack(self):
        """Test set_trump method with regular jack (same suit as trump)."""
        self.jack_spades.set_trump('Spades')

        self.assertEqual(self.jack_spades.symbol, 'J')
        self.assertEqual(self.jack_spades.rank, 14)  # Regular jack rank
        self.assertEqual(self.jack_spades.points, 1)
        self.assertEqual(self.jack_spades.trump_suit, 'Spades')

    def test_set_trump_non_trump_card(self):
        """Test set_trump method with non-trump card."""
        self.king_hearts.set_trump('Spades')

        self.assertEqual(self.king_hearts.symbol, 'N')  # Non-trump symbol
        self.assertEqual(self.king_hearts.rank, 1)      # Non-trump rank
        # No points for non-trump
        self.assertEqual(self.king_hearts.points, 0)
        self.assertEqual(self.king_hearts.trump_suit, 'Spades')

    def test_jokers_always_trump(self):
        """Test that jokers are always considered trump cards."""
        for suit in ['Spades', 'Hearts', 'Diamonds', 'Clubs']:
            self.assertTrue(self.big_joker.is_trump(suit))
            self.assertTrue(self.little_joker.is_trump(suit))

    def test_comparison_with_trump_set(self):
        """Test card comparisons after setting trump suit."""
        # Set trump suit for both cards
        self.jack_clubs.set_trump('Spades')  # Becomes off jack (rank 13)
        self.jack_spades.set_trump('Spades')  # Remains jack (rank 14)

        # Jack of Spades should be higher than off jack (Jack of Clubs)
        self.assertTrue(self.jack_spades > self.jack_clubs)
        self.assertFalse(self.jack_spades < self.jack_clubs)

    def test_ten_card_special_case(self):
        """Test the special case for '10' cards."""
        ten_card = Card('10', 'Hearts')
        self.assertEqual(ten_card.base_symbol('10'), '10')
        self.assertEqual(ten_card.symbol, '10')

    def test_card_reference_integrity(self):
        """Test that card reference data is consistent."""
        # Test that all expected keys exist in card_reference
        essential_cards = ['Ace', 'King', 'Queen', 'Jack',
                           '10', '9', '8', '7', '6', '5', '4', '3', '2']
        for card_name in essential_cards:
            self.assertIn(card_name, Card.card_reference)
            self.assertIn('rank', Card.card_reference[card_name])
            self.assertIn('points', Card.card_reference[card_name])
            self.assertIn('desc', Card.card_reference[card_name])

    def test_suit_to_symbol_mapping(self):
        """Test that suit to symbol mapping is correct."""
        expected_symbols = {
            'Spades': '♠',
            'Diamonds': '♦',
            'Clubs': '♣',
            'Hearts': '♥',
            'Joker': 'J'
        }

        for suit, symbol in expected_symbols.items():
            self.assertEqual(Card.suit_to_symbol[suit], symbol)

    def test_all_off_jack_combinations(self):
        """Test all valid off jack combinations."""
        off_jack_combinations = [
            ('Jack', 'Clubs', 'Spades'),   # Jack of Clubs when Spades is trump
            ('Jack', 'Spades', 'Clubs'),   # Jack of Spades when Clubs is trump
            # Jack of Diamonds when Hearts is trump
            ('Jack', 'Diamonds', 'Hearts'),
            # Jack of Hearts when Diamonds is trump
            ('Jack', 'Hearts', 'Diamonds')
        ]

        for jack_name, jack_suit, trump_suit in off_jack_combinations:
            jack = Card(jack_name, jack_suit)
            self.assertTrue(jack.is_trump(trump_suit),
                            f"Jack of {jack_suit} should be trump when {trump_suit} is trump")

            jack.set_trump(trump_suit)
            self.assertEqual(jack.symbol, 'X',
                             f"Jack of {jack_suit} should have symbol 'X'\
                               when {trump_suit} is trump")


if __name__ == '__main__':
    unittest.main()
