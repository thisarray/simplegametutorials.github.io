import pygame
import random

def take_card(hand):
    hand.append(deck.pop(random.randrange(len(deck))))

def reset():
    global deck
    global player_hand
    global dealer_hand
    global round_over

    deck = []
    for suit in ('club', 'diamond', 'heart', 'spade'):
        for rank in range(1, 14):
            deck.append({'suit': suit, 'rank': rank})

    player_hand = []
    take_card(player_hand)
    take_card(player_hand)

    dealer_hand = []
    take_card(dealer_hand)
    take_card(dealer_hand)

    round_over = False

reset()

def get_total(hand):
    total = 0
    has_ace = False

    for card in hand:
        if card['rank'] > 10:
            total += 10
        else:
            total += card['rank']

        if card['rank'] == 1:
            has_ace = True

    if has_ace and total <= 11:
        total += 10

    return total

button_y = 230
button_height = 25
text_offset_y = 6

button_hit = {
    'x': 10,
    'y': button_y,
    'width': 53,
    'height': 25,
    'text': 'Hit!',
    'text_offset_x': 13,
    'text_offset_y': text_offset_y,
}

button_stand = {
    'x': 70,
    'y': button_y,
    'width': 53,
    'height': 25,
    'text': 'Stand',
    'text_offset_x': 4,
    'text_offset_y': text_offset_y,
}

button_play_again = {
    'x': 10,
    'y': button_y,
    'width': 113,
    'height': 25,
    'text': 'Play again',
    'text_offset_x': 17,
    'text_offset_y': text_offset_y,
}

def is_mouse_in_button(button):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    return (
        mouse_x >= button['x']
        and mouse_x < button['x'] + button['width']
        and mouse_y >= button['y']
        and mouse_y < button['y'] + button['height']
    )

def update():
    pass

def on_mouse_up():
    global round_over

    if not round_over:
        if is_mouse_in_button(button_hit):
            take_card(player_hand)
            if get_total(player_hand) >= 21:
                round_over = True
        elif is_mouse_in_button(button_stand):
            round_over = True

        if round_over:
            while get_total(dealer_hand) < 17:
                take_card(dealer_hand)
    elif is_mouse_in_button(button_play_again):
        reset()

def draw():
    screen.fill((255, 255, 255))

    card_spacing = 60
    margin_x = 10

    for card_index, card in enumerate(dealer_hand):
        image = card['suit'] + '_' + str(card['rank'])
        if not round_over and card_index == 0:
            image = 'card_face_down'
        screen.blit(image, (card_index * card_spacing + margin_x, 30))

    for card_index, card in enumerate(player_hand):
        screen.blit(card['suit'] + '_' + str(card['rank']),
            (card_index * card_spacing + margin_x, 140))

    if round_over:
        screen.draw.text('Total: ' + str(get_total(dealer_hand)),
            (margin_x, 10), color=(0, 0, 0))
    else:
        screen.draw.text('Total: ?', (margin_x, 10), color=(0, 0, 0))

    screen.draw.text('Total: ' + str(get_total(player_hand)),
        (margin_x, 120), color=(0, 0, 0))

    if round_over:
        def has_hand_won(this_hand, other_hand):
            return (
                get_total(this_hand) <= 21
                and (
                    get_total(other_hand) > 21
                    or get_total(this_hand) > get_total(other_hand)
                )
            )

        def draw_winner(message):
            screen.draw.text(message, (margin_x, 268), color=(0, 0, 0))

        if has_hand_won(player_hand, dealer_hand):
            draw_winner('Player wins')
        elif has_hand_won(dealer_hand, player_hand):
            draw_winner('Dealer wins')
        else:
            draw_winner('Draw')

    def draw_button(button):
        if is_mouse_in_button(button):
            color = (255, 202, 75)
        else:
            color = (255, 127, 57)

        screen.draw.filled_rect(
            Rect(button['x'], button['y'], button['width'], button['height']),
            color=color
        )
        screen.draw.text(
            button['text'],
            (button['x'] + button['text_offset_x'],
            button['y'] + button['text_offset_y'])
        )

    if not round_over:
        draw_button(button_hit)
        draw_button(button_stand)
    else:
        draw_button(button_play_again)

WIDTH = 500
HEIGHT = 300
