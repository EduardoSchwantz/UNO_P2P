import random

COLORS = ["red", "yellow", "green", "blue"]
VALUES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
          "skip", "reverse", "+2"]

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __repr__(self):
        return f"{self.color.upper()}-{self.value.upper()}"

    def to_dict(self):
        return {"color": self.color, "value": self.value}

    @staticmethod
    def from_dict(data):
        return Card(data['color'], data['value'])

    def is_playable_on(self, top_card):
        return (
            self.color == top_card.color or
            self.value == top_card.value or
            self.color == "wild" or
            self.value in ["wild", "+4"]
        )

def generate_deck():
    deck = []
    for color in COLORS:
        for value in VALUES:
            deck.append(Card(color, value))
            if value != "0":
                deck.append(Card(color, value))
    for _ in range(4):
        deck.append(Card("wild", "wild"))
        deck.append(Card("wild", "+4"))
    random.shuffle(deck)
    return deck

class GameState:
    def play_card(self, player, card, chosen_color=None):
        hand = self.players[player]
        for i, c in enumerate(hand):
            if c.color == card.color and c.value == card.value:
                self.top_card = hand.pop(i)
                # Se for coringa, aplica a cor escolhida
                if self.top_card.value in ["wild", "+4"] and chosen_color:
                    self.top_card.color = chosen_color
                self.handle_special_card(self.top_card)
                self.next_turn()
                return True
        return False
    def __init__(self, players):
        self.deck = generate_deck()
        self.players = {name: [] for name in players}
        self.current_turn = players[0]
        self.turn_order = players[:]
        self.top_card = None
        self.direction = 1

    def start_game(self):
        for player in self.players:
            self.players[player] = [self.deck.pop() for _ in range(7)]
        self.top_card = self.deck.pop()

    def to_dict(self):
        return {
            "deck": [c.to_dict() for c in self.deck],
            "players": {p: [c.to_dict() for c in cards] for p, cards in self.players.items()},
            "current_turn": self.current_turn,
            "top_card": self.top_card.to_dict() if self.top_card else None,
            "direction": self.direction,
            "turn_order": self.turn_order
        }
    @staticmethod
    def from_dict(data):
        gs = GameState(data['turn_order'])
        gs.deck = [Card.from_dict(c) for c in data.get('deck', [])]
        gs.players = {p: [Card.from_dict(c) for c in cards] for p, cards in data['players'].items()}
        gs.current_turn = data['current_turn']
        gs.top_card = Card.from_dict(data['top_card']) if data['top_card'] else None
        gs.direction = data.get('direction', 1)
        gs.turn_order = data['turn_order']
        return gs

    def next_turn(self):
        idx = self.turn_order.index(self.current_turn)
        next_idx = (idx + self.direction) % len(self.turn_order)
        self.current_turn = self.turn_order[next_idx]

    def handle_special_card(self, card):
        if card.value == "reverse":
            self.direction *= -1
        elif card.value == "skip":
            self.next_turn()
        elif card.value == "+2":
            self.next_turn()
            self.draw_cards(self.current_turn, 2)
        elif card.value == "+4":
            self.next_turn()
            self.draw_cards(self.current_turn, 4)

    def draw_cards(self, player, count):
        drawn_cards = []
        for _ in range(count):
            if self.deck:
                card = self.deck.pop()
                self.players[player].append(card)
                drawn_cards.append(card)
        return drawn_cards

    def has_valid_play(self, player):
        hand = self.players[player]
        top = self.top_card
        for card in hand:
            if card.is_playable_on(top):
                return True
        return False

    def auto_draw_if_no_valid_play(self, player):
        if not self.has_valid_play(player):
            drawn_cards = self.draw_cards(player, 1)
            if drawn_cards:
                print(f"[{player}] não tinha jogada válida e comprou: {drawn_cards[0]}")
            else:
                print(f"[{player}] não tinha jogada válida e não há cartas para comprar.")
            return drawn_cards
        return []

    def is_game_over(self):
        for player, cards in self.players.items():
            if len(cards) == 0:
                return True, player
        return False, None