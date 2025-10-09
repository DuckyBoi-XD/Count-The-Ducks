#----Import Python Packages----#
#--Save File--#
import json
import base64
import codecs

#--Functions--#
import time

#--Os Check--#
import os
import sys

#----Import Python Packages----#

#----Preloaded function----#

if os.name == 'nt':
    try:
        import msvcrt
    except ImportError:
        pass                            #WINDOWS MAC IMPORT ERROR
elif os.name == 'posix':
    import termios
    import tty
else:
    pass                                    # OS NOT COMPATABLE

#----Preloaded variables----#

#----Colours----#
class Colours:
    '''colours for texts'''
    BLACK = '\033[38;5;0m'
    RED = '\033[38;5;1m'
    GREEN = '\033[38;5;2m'
    YELLOW = '\033[38;5;3m'
    BLUE = '\033[38;5;4m'
    MAGENTA = '\033[38;5;5m'
    CYAN = '\033[38;5;6m'
    WHITE = '\033[38;5;7m'
    GOLD = '\033[38;5;220m'
    
    BG_RED = '\033[48;5;196m'
    BG_GREEN = '\033[48;5;46m'
    BG_YELLOW = '\033[48;5;226m'
    BG_BLUE = '\033[48;5;21m'
    BG_WHITE = '\033[48;5;15m'
    BG_BLACK = '\033[48;5;0m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    
    RESET = '\033[0m'
#----Colours----#

#----Preloaded function----#

if os.name == 'nt':
    OS = "Windows"
elif os.name == 'posix':
    OS = "Unix"
else:
    OS = "Unknown"

#----Preloaded variables----#
FILE_STATUS = None

#--Save File Money--#

#-Binary Encoder-#
def to_binary_str(s):
    '''binary encoder'''
    return ''.join(format(ord(c), '08b') for c in s)

def from_binary_str(b):
    '''binary decoder'''
    # Validate binary string
    if len(b) % 8 != 0:
        raise ValueError("Binary string length must be divisible by 8")
    if not all(c in '01' for c in b):
        raise ValueError("Binary string must only contain 0s and 1s")
    
    chars = [chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8)]
    return ''.join(chars)

#--base64 + ROT13 encoder--#
def encode_save(json_str):
    '''encodes using method under'''
    # Base64 encode
    b64 = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    # Reverse
    rev = b64[::-1]
    # ROT13 encode
    rot = codecs.encode(rev, 'rot_13')
    # Binary encode
    binary = to_binary_str(rot)
    return binary.encode('utf-8')  # Write as bytes

#--base64 + ROT13 decoder--#
def decode_save(encoded_bytes):
    '''decodes using method under'''
    # grabs code
    binary_str = encoded_bytes.decode('utf-8')
    # Binary decode
    rot = from_binary_str(binary_str)
    # ROT13 decode
    rev = codecs.decode(rot, 'rot_13')
    # Reverse
    b64 = rev[::-1]
    # Base64 decode
    json_str = base64.b64decode(b64).decode('utf-8')
    return json_str

def get_config_dir():
    '''Return platform-appropriate config directory'''
    return os.path.expanduser("~/.config/duck-roulette")                        #CHANGE NAME

def load_game(): # access save file JSON
    '''loading save file - returns both money and name'''
    global FILE_STATUS
    config_dir = get_config_dir()
    save_path = os.path.join(config_dir, "DuckRouletteSaveFile.bin")                 #CHANGE GAME NAME
    try:
        with open(save_path, "rb") as f:                                           #ADD ITEMS TO SAVE FILE
            encoded_bytes = f.read()
            json_str = decode_save(encoded_bytes)
            data = json.loads(json_str)
            FILE_STATUS = 1
            return (data.get("money", 500),
                    data.get("name", None),
                    data.get("games played", 0),
                    data.get("money earnt", 0),
                    data.get("money lost", 0),
                    data.get("money borrowed", 0),
                    data.get("card roulette wins", 0),
                    data.get("card roulette loses", 0),
                    )
    except FileNotFoundError:
        FILE_STATUS = 2
        return 500, None, 0, 0, 0, 0, 0, 0                                              #ADD ITEMS TO SAVE FILE
    except (ValueError, json.JSONDecodeError):
        FILE_STATUS = 3
        return 500, None, 0, 0, 0, 0, 0, 0                                               #ADD ITEMS TO SAVE FILE

def save_game(money=None,
            name=None,
            game_played=None,
            money_earnt=None,
            money_lost=None,
            money_borrowed=None,
            card_roulette_wins=None,
            card_roulette_loses=None
            ):
    '''saving game data'''
    if money is None:
        money = USER_WALLET
    if name is None:
        name = USER_NAME
    if game_played is None:
        game_played = GAMES_PLAYED
    if money_earnt is None:
        money_earnt = MONEY_EARNT
    if money_lost is None:
        money_lost = MONEY_LOST
    if money_borrowed is None:
        money_borrowed = MONEY_BORROWED
    if card_roulette_wins is None:
        card_roulette_wins = CARD_ROULETTE_WINS
    if card_roulette_loses is None:
        card_roulette_loses = CARD_ROULETTE_LOSES
    data = {
        "money": money,
        "name": name,
        "games played": game_played,
        "money earnt": money_earnt,
        "money lost": money_lost,
        "money borrowed": money_borrowed,
        "card roulette wins": card_roulette_wins,
        "card roulette loses": card_roulette_loses
    }
    json_str = json.dumps(data)
    encoded_bytes = encode_save(json_str)
    config_dir = get_config_dir()
    os.makedirs(config_dir, exist_ok=True)
    save_path = os.path.join(config_dir, "DuckRouletteSaveFile.bin")
    with open(save_path, "wb") as f:
        f.write(encoded_bytes)
#--Save File Money--#

#----Preloaded function----#

#---Variables---#
USER_WALLET, USER_NAME, GAMES_PLAYED, MONEY_EARNT, MONEY_LOST, MONEY_BORROWED, CARD_ROULETTE_WINS, CARD_ROULETTE_LOSES = load_game()  # Load both money and name from save file
CARD_SUITS = ("♠", "♦", "♥", "♣") # creates suits for card deck creation
USER_NAME_KNOWLEDGE = False

Confirm_Redo = ["✅ Confirm", "🔄 Redo"]
Confirm_Cancel = ["✅ Confirm", "❌ Cancel"]
Confirm_Redo_Cancel = ["✅ Confirm", "🔄 Redo", "❌ Cancel"]

card_output = ""
bet_amount = None
user_bet = None
bet_confirm = False
user_bet_check = None

CRPick = [
    "🟥 ⬛ Card Colour",
    "♠️ ♦️ ♣️ ♥️  Card Suit",
    "👑 [A] 🔟 Group cards",
    "🃏 Certain Cards",
    "🃏 ♠️ ♦️ ♣️ ♥️  Specific Cards",
    "❌ Quit Game"

]
CRRedBlackPick = [
    f"🟥 Red Cards {Colours.GREEN}x2{Colours.RESET} {Colours.YELLOW}[50%]{Colours.RESET}",
    f"⬛ Black Cards {Colours.GREEN}x2{Colours.RESET} {Colours.YELLOW}[50%]{Colours.RESET}",
    "↩️ Back"
]
CRSuitsPick = [
    f"♠️ Spades {Colours.GREEN}x4{Colours.RESET} {Colours.YELLOW}[25%]{Colours.RESET}",
    f"♦️ Diamonds {Colours.GREEN}x4{Colours.RESET} {Colours.YELLOW}[25%]{Colours.RESET}",
    f"♥️ Hearts {Colours.GREEN}x4{Colours.RESET} {Colours.YELLOW}[25%]{Colours.RESET}",
    f"♣️ Clubs {Colours.GREEN}x4{Colours.RESET} {Colours.YELLOW}[25%]{Colours.RESET}",
    "↩️ Back"
]
CRGroupPick = [
    f"👑 Face Cards {Colours.GREEN}x5{Colours.RESET} {Colours.YELLOW}[23.08%]{Colours.RESET}",
    f"🔟 Number Cards {Colours.GREEN}x1.5{Colours.RESET} {Colours.YELLOW}[76.92%]{Colours.RESET}",
    f"🔟 👑 👑 👑 [A] Royal Straight Cards {Colours.GREEN}x3{Colours.RESET} {Colours.YELLOW}[38.46%]{Colours.RESET}",
    f"[A] [2] [3] [4] [5] Bicycle Cards {Colours.GREEN}x3{Colours.RESET} {Colours.YELLOW}[38.46%]{Colours.RESET}"
    "↩️ Back"
]
CRCertainPick = [ #This can be done way more simpler but it eaiser to see all the options
    f"2 {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[7.69%]{Colours.RESET}",
    f"3 {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[7.69%]{Colours.RESET}",
    f"4 {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[7.69%]{Colours.RESET}",
    f"5 {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[7.69%]{Colours.RESET}",
    f"6 {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[7.69%]{Colours.RESET}",
    f"7 {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[7.69%]{Colours.RESET}",
    f"8 {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[7.69%]{Colours.RESET}",
    f"9 {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[7.69%]{Colours.RESET}",
    f"10 {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[7.69%]{Colours.RESET}",
    f"Duck {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[7.69%]{Colours.RESET}",
    f"Queen {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[7.69%]{Colours.RESET}",
    f"King {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[7.69%]{Colours.RESET}",
    f"Ace {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[7.69%]{Colours.RESET}",
    "↩️ Back"
]
CRSpecificPick = [
    "♠️ Spades",
    "♦️ Diamonds",
    "♥️ Hearts",
    "♣️ Clubs",
    "↩️ Back"
]
CRSuitsSpades = [
    f"2 ♠️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"3 ♠️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"4 ♠️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"5 ♠️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"6 ♠️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"7 ♠️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"8 ♠️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"9 ♠️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"10 ♠️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"Duck ♠️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"Queen ♠️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"King ♠️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"Ace ♠️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    "↩️ Back"
]
CRSuitsDiamonds = [
    f"2 ♦️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"3 ♦️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"4 ♦️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"5 ♦️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"6 ♦️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"7 ♦️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"8 ♦️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"9 ♦️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"10 ♦️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"Duck ♦️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"Queen ♦️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"King ♦️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"Ace ♦️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    "↩️ Back"
]
CRSuitsHearts = [
    f"2 ♥️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"3 ♥️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"4 ♥️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"5 ♥️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"6 ♥️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"7 ♥️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"8 ♥️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"9 ♥️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"10 ♥️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"Duck ♥️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"Queen ♥️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"King ♥️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"Ace ♥️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    "↩️ Back"
]
CRSuitsClubs = [
    f"2 ♣️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"3 ♣️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"4 ♣️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"5 ♣️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"6 ♣️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"7 ♣️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"8 ♣️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"9 ♣️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"10 ♣️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"Duck ♣️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"Queen ♣️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"King ♣️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    f"Ace ♣️ {Colours.GREEN}x20{Colours.RESET} {Colours.YELLOW}[1.92%]{Colours.RESET}",
    "↩️ Back"
]
PlayOptions = [
    "🔄 Play Again",
    "🎰 Menu"
    ]
Win_Continue = [
    "✅ Continue",
    "💵 Cash Out"
    ]
Lose_Continue = [
    "🔄 Play Again",
    "🎰 Menu"
    ]
OverUnderPick = [
    "⬆️  Over",
    "⬇️  Under"
    ] 
InOutPick = [
    "➡️ ⬅️  Inside",
    "⬅️ ➡️  Outside"
    ]
SuitPick = [
    "♠️ Spades",
    "♦️ Diamonds",
    "♥️ Hearts",
    "♣️ Clubs"
    ]
CashOut = [
    "💵 Cash Out & 🔄 Play Again",
    "💵 Cash Out"
]

top = ""
mid_top = ""
top_mid = ""
bottom_mid = ""
mid_bottom = ""
bottom = ""

#----Variable----#

#----Function Variables----#
def LINE():
    ''''creates line spacing'''
    print(f"{Colours.BOLD}{Colours.MAGENTA}======----------================----------======{Colours.RESET}")

def clear_screen():
    ''''clear screen function'''
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        print("\n" * 50)
    print('\033[2J\033[H', end='')
    sys.stdout.flush()

def is_float(variable):
    '''check if value is a float'''
    try:
        float(variable)
        return True
    except ValueError:
        return False

def money_valid(money_value):
    """check if value has 2 decimal or less"""
    if '.' in money_value:
        decimal_part = money_value.split('.')[1]
        return len(decimal_part) <= 2
    else:
        return True

def print_tw(sentence, type_delay=0.01):
    '''creates a type writer effect'''
    for char in sentence:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(type_delay)
    sys.stdout.write('\n')
    sys.stdout.flush()
#----Function Variables----#

#----Card Deck----#
CardDeck = {}

for suit in CARD_SUITS:
    for value_card in range(2, 11):
        CardDeck[f"{value_card}{suit}"] = value_card

for suit in CARD_SUITS:
    CardDeck[f"D{suit}"] = 11
    CardDeck[f"Q{suit}"] = 12
    CardDeck[f"K{suit}"] = 13
    CardDeck[f"A{suit}"] = 14
#----Card Deck----#

#----Single Key Track----#
def key_press(option):
    """Waits for a single key press"""
    try:
        if option == 0:
            print(f"{Colours.RED}Press any key to continue{Colours.RESET}")
        elif option == 1:
            print(f"{Colours.RED}Press any key to return to menu{Colours.RESET}")
        elif option == 2:
            print(f"{Colours.GREEN}Your ${user_bet} is returned to you\n\n{Colours.RESET}{Colours.RED}Press any key to return to menu{Colours.RESET}")

        if os.name == "nt":
            msvcrt.getwch()
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return True
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
        sys.exit()
#----Single Key Track----#

#----Arrow Key Track----#
def arrow_key():
    """Read one key or arrow key"""
    try:
        if os.name == "nt":
            ch = msvcrt.getwch()
            if ch and ord(ch) == 3:
                print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
                sys.exit()
            if ch in ("\x00", "\xe0"):
                ch2 = msvcrt.getwch()
                win_map = {
                    "H": "\x1b[A",  # up
                    "P": "\x1b[B",  # down
                    "M": "\x1b[C",  # right
                    "K": "\x1b[D",  # left
                }
                return win_map.get(ch2, ch + ch2)
            if ch == "\r":
                return "\r"
            return ch

        elif os.name == "posix":
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                key = sys.stdin.read(1)

                if ord(key) == 3:  # CTRL-C
                    print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")                    #
                    sys.exit()
                elif ord(key) == 4:  # CTRL-D
                    print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
                    sys.exit()

                if ord(key) == 27:  # ESC
                    # read the next two chars (typical ANSI arrow seq)
                    key += sys.stdin.read(2)
                return key
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
        sys.exit()
#----Arrow Key Track----#

#----Arrow Key Menu System----#
def arrow_menu(title, text, options):
    """generic arrow key menu system"""
    try:
        selected = 0
        while True:
            clear_screen()
            LINE()
            if title == "gameCR":
                print(f"{Colours.BOLD}{Colours.BLUE}🎰 DUCK ROULETTE - CARD ROULETTE 🎰{Colours.RESET}")
            elif title == "gameCRRedBlack":
                print(f"{Colours.BOLD}{Colours.BLUE}🎰 DUCK ROULETTE - CARD ROULETTE - CARD COLOUR PICK🎰{Colours.RESET}")
            elif title == "confirm-cancel":
                print(f"{Colours.BOLD}{Colours.BLUE}🎰 DUCK ROULETTE - CARD ROULETTE - CONFIRM 🎰{Colours.RESET}")
            elif title == "menu":
                print(f"{Colours.BOLD}{Colours.BLUE}🎰 DUCK ROULETTE - MENU 🎰{Colours.RESET}")
            elif title == "name":
                print(f"{Colours.BOLD}{Colours.BLUE}🏷️  DUCK ROULETTE - NAME 🏷️{Colours.RESET}")

            LINE()
            if text is not None:
                print(text)
            
                
            # Display menu options
            for i, option in enumerate(options):
                if i == selected:
                    print(f"{Colours.BOLD}{Colours.YELLOW}► {option}{Colours.RESET}")
                else:
                    print(f"{Colours.WHITE}  {option}{Colours.RESET}")
            LINE()
            key = arrow_key()
            
            # Handle arrow keys and other inputs for Unix/macOS
            if len(key) > 1:
                if key == '\x1b[A':  # Up arrow
                    selected = (selected - 1) % len(options)
                elif key == '\x1b[B':  # Down arrow
                    selected = (selected + 1) % len(options)
                elif ord(key[0]) == 13:  # Enter
                    return selected
                elif len(key) == 1 and ord(key) == 27:  # ESC alone
                    return -1
            elif len(key) == 1:
                if key.lower() == 'w':  # W key - up
                    selected = (selected - 1) % len(options)
                elif key.lower() == 's':  # S key - down
                    selected = (selected + 1) % len(options)
                elif key == '\r' or key == '\n':  # Enter
                    return selected
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
        sys.exit()

#----Arrow Key Menu System----#

#----Start Game----#
def start_game():
    '''start of game info'''
    try:
        clear_screen()
        LINE()
        print(f"{Colours.BOLD}{Colours.BLUE}🎰 Duck Roulette 🎰{Colours.RESET}\n")
        if FILE_STATUS == 1:
            print(f"{Colours.BOLD}{Colours.GREEN}💾 Loaded Save File{Colours.RESET}")
        elif FILE_STATUS == 2:
            print(f"{Colours.BOLD}{Colours.YELLOW}💾 New Save File{Colours.RESET}")
        elif FILE_STATUS == 3:
            print(f"{Colours.BOLD}{Colours.RED}💾 Corrupted or Tampered Save File{Colours.RESET}")
        if os.name == "nt":
            print(f"{Colours.BOLD}{Colours.CYAN}🖥️  Windows Operating System{Colours.RESET}")
        elif os.name == "posix":
            print(f"{Colours.BOLD}{Colours.CYAN}🖥️  MacOS/Linux Operating System{Colours.RESET}")
        else:
            print(f"{Colours.BOLD}{Colours.CYAN}🖥️  Unknown Operating System{Colours.RESET}")
        print(f"{Colours.GREEN}💰 Your Money: ${USER_WALLET}{Colours.RESET}\n"
        f"{Colours.CYAN}🎉 Welcome to Duck Roulette, a gambling game combining roulette with a card deck 🎉{Colours.RESET}")
        if USER_NAME is None:
            print(f"{Colours.YELLOW}🏷️  Your  Name:{Colours.RESET}{Colours.RED} -UNKNOWN-{Colours.RESET}")
        else:
            print(f"{Colours.YELLOW}🏷️  Your  Name:{Colours.RESET} {USER_NAME}")
        LINE()
        key_press(1)
        clear_screen()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
        sys.exit()
#----Start Game----#

#----financial aid----#
def financial_aid():
    """Function to output the last message after losing all your money"""
    global USER_WALLET
    global MONEY_BORROWED
    MONEY_BORROWED += 100
    clear_screen()
    try:
        clear_screen()
        LINE()
        print(f"{Colours.BOLD}{Colours.BLUE}🏷️  DUCK ROULETTE - FINANCIAL AID 🏷️{Colours.RESET}")
        LINE()
        print(f"{Colours.YELLOW}Due to you being {Colours.RED}BROKE{Colours.RESET}{Colours.YELLOW}, you are given {Colours.RESET}{Colours.GREEN}$10{Colours.RESET} {Colours.YELLOW}to hopefully sustain your gambling addiction\n")
        USER_WALLET += 10
        print(f"{Colours.GREEN}You now have ${USER_WALLET}{Colours.RESET}")
        print(f"{Colours.RED}You have borrowed a total of ${MONEY_BORROWED}")
        LINE()
        save_game()
        key_press(1)
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
        sys.exit()
#----financial aid----#

#----Betting Check Function----#
def bet_check():
    '''betting check'''
    clear_screen()
    try:
        global user_bet
        global USER_WALLET
        global bet_confirm
        global bet_amount
        if USER_WALLET <= 0:
            financial_aid()
            return
        else:
            bet_error = 0
            user_bet = None
            bet_confirm = False
            user_bet_check = None
            while True:
                clear_screen()
                LINE()
                print(f"{Colours.BOLD}{Colours.BLUE}🎰 DUCK ROULETTE - MAIN GAME - BET 🎰{Colours.RESET}")
                LINE()

                if bet_error == 1:
                    print(f"{Colours.RED}⚠️ Invalid bet: {user_bet_check} - Please use a number ⚠️{Colours.RESET}")
                elif bet_error == 2:
                    print(f"{Colours.RED}⚠️ Invalid bet: {user_bet_check} - Please enter a number equal or bigger than 0.01 ⚠️{Colours.RESET}")
                elif bet_error == 3:
                    print(f"{Colours.RED}⚠️ Invalid bet: {user_bet_check} - You are betting more money than you have in your wallet ⚠️{Colours.RESET}")

                print(f"{Colours.GREEN}💰 Your Money: ${USER_WALLET}{Colours.RESET}\n"
                    f"{Colours.CYAN}💵  How much do you want to bet? (Min $0.01) 💵{Colours.RESET}")
                bet_error = 0
                try:
                    user_bet_check = input(f"{Colours.BOLD}❯ {Colours.RESET}").strip()
                except (KeyboardInterrupt, EOFError):
                    print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
                    sys.exit()
                
                if is_float(user_bet_check):
                    if money_valid(user_bet_check) and float(user_bet_check) >= 0.01:
                        if float(user_bet_check) <= USER_WALLET:
                            user_bet = float(user_bet_check)
                            clear_screen()
                            choices = arrow_menu("menu",
                                f"{Colours.GREEN}💵 You are betting: {Colours.WHITE}${user_bet}{Colours.RESET}\n{Colours.CYAN}✅ Please confirm bet amount ✅{Colours.RESET}\n",
                                Confirm_Redo_Cancel)
                            if choices == 0:
                                clear_screen()
                                bet_confirm = True
                                USER_WALLET -= user_bet
                                bet_amount = user_bet
                                break
                            elif choices == 1:
                                clear_screen()
                            elif choices == 2:
                                clear_screen()
                                break
                        else:
                            bet_error = 3
                            clear_screen()
                    else:
                        bet_error = 2
                        clear_screen()
                else:
                    bet_error = 1
                    clear_screen()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
        sys.exit()

#----Betting check Function----#

#----Name Function----#
def name_pick():
    '''Lets user pick a name'''
    global USER_NAME
    global USER_NAME_KNOWLEDGE
    
    while True:
        try:
            clear_screen()
            LINE()
            print(f"{Colours.BOLD}{Colours.BLUE}🏷️  DUCK ROULETTE - NAME 🏷️{Colours.RESET}")
            LINE()
            print(f"{Colours.YELLOW}✏️  What would you like your name to be? ✏️{Colours.RESET}")
            if USER_NAME_KNOWLEDGE is False:
                print(f"{Colours.RED}(You can change this later){Colours.RESET}")
            elif USER_NAME_KNOWLEDGE is True:
                pass
            try:
                USER_NAME = input(f"{Colours.BOLD}❯ {Colours.RESET}")
            except (KeyboardInterrupt, EOFError):
                print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
                sys.exit()
            
            clear_screen()
            choice = arrow_menu("name", (f"{Colours.BOLD}{Colours.YELLOW}YOU HAVE SELECTED: {Colours.RESET}{USER_NAME}\n"), Confirm_Redo)
            if choice == 0:
                USER_NAME_KNOWLEDGE = True
                clear_screen()
                break  # Exit the loop successfully
            elif choice == 1:
                continue  # Retry name input
                
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
            sys.exit()
#----Name Function----#

#----Help----#
def help_game():
    """help information function"""
    try:
        clear_screen()
        LINE()
        print(f"{Colours.BOLD}{Colours.BLUE}❓  DUCK ROULETTE - HELP ❓{Colours.RESET}")
        LINE()

        print(f"{Colours.CYAN}\"Duck Roulette\" is a gambling game inspired by the casino game, roulette, but using a deck of cards.\n\n{Colours.RESET}"
            f"{Colours.RED}IMPORTANT:{Colours.RESET} The {Colours.YELLOW}Jack{Colours.RESET} cards are replaced by {Colours.YELLOW}Ducks{Colours.RESET}"
            "In the first game, Card Roulette, when picking what type of card to bet on, you many need to choose multiple catagories"
        )
        LINE()
        key_press(1)
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
        sys.exit()
#----Help----#

#----Stats----#
def show_stats():
    """Display player statistics"""
    global WINS_TOTAL
    clear_screen()
    try:
        clear_screen()
        LINE()
        print(f"{Colours.BOLD}{Colours.CYAN}📊 PLAYER STATISTICS 📊{Colours.RESET}")
        LINE()
        print(f"{Colours.GREEN}💰 Money: ${USER_WALLET}{Colours.RESET}\n"
            f"{Colours.YELLOW}🏷️  Name: {USER_NAME}{Colours.RESET}\n"
            f"{Colours.CYAN}🎮 Games Played: {GAMES_PLAYED}{Colours.RESET}\n"
            f"{Colours.GREEN}💵 ⬆️  Money Earnt: {MONEY_EARNT}{Colours.RESET}\n"
            f"{Colours.RED}💵 ⬇️  Money Lost: {MONEY_LOST}{Colours.RESET}\n"
            f"{Colours.RED}💵 📉 Money Borrowed: {MONEY_BORROWED}{Colours.RESET}\n"
            f"{Colours.GOLD}🎰 🏆 Card Roulette Wins: {CARD_ROULETTE_WINS}{Colours.RESET}\n"
            f"{Colours.RED}🎰 🪦  Card Roulette Loses: {CARD_ROULETTE_LOSES}{Colours.RESET}"
        )
        LINE()
        key_press(1)
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
        sys.exit()
#----Stats----#

#----Game 1 - card roulette----#
def card_roulette():
    """First game"""
    global USER_WALLET, user_bet
    BetPick = None
    try:
        bet_check()
        while True:
            choices = arrow_menu("gameCR", (f"{Colours.CYAN}Pick what you would like to bet your {Colours.RESET}{Colours.GREEN}${user_bet}{Colours.RESET}{Colours.CYAN} on{Colours.RESET}\n"), CRPick)
            if choices == 0: # Card colour
                choices = arrow_menu("gameCRRedBlack", (f"{Colours.CYAN}Pick which {Colours.RESET}{Colours.YELLOW}colour{Colours.RESET}{Colours.CYAN} you want to bet on{Colours.RESET}\n\n{Colours.GREEN}x_{Colours.RESET} is the multiplier\n{Colours.YELLOW}[__%]{Colours.RESET} is the change of the bet being picked\n"), CRRedBlackPick)
                BetGroup = "COLOUR"
                if choices == 0:
                    BetPick = "RED"
                elif choices == 1:
                    BetPick = "BLACK"
                elif choices == 2 or choices == -1:
                    continue
                else:
                    continue
            elif choices == 1: # Card Suits
                choices = arrow_menu("gameCRSuits", (f"{Colours.CYAN}Pick which {Colours.RESET}{Colours.YELLOW}suit{Colours.RESET}{Colours.CYAN} you want to bet on{Colours.RESET}\n\n{Colours.GREEN}x_{Colours.RESET} is the multiplier\n{Colours.YELLOW}[__%]{Colours.RESET} is the change of the bet being picked\n"), CRSuitsPick)
                BetGroup = "SUIT"
                if choices == 0:
                    BetPick = "SPADE"
                elif choices == 1:
                    BetPick = "DIAMOND"
                elif choices == 2:
                    BetPick = "HEART"
                elif choices == 3:
                    BetPick = "CLUB"
                elif choices == 4 or choices == -1:
                    continue
                else:
                    continue
            elif choices == 2: # Card Groups
                choices = arrow_menu("gameCRGroups", (f"{Colours.CYAN}Pick which {Colours.RESET}{Colours.YELLOW}group{Colours.RESET}{Colours.CYAN} you want to bet on{Colours.RESET}\n\n{Colours.GREEN}x_{Colours.RESET} is the multiplier\n{Colours.YELLOW}[__%]{Colours.RESET} is the change of the bet being picked\n"), CRGroupPick)
                BetGroup = "GROUP"
                if choices == 0:
                    BetPick = "FACE"
                elif choices == 1:
                    BetPick = "NUMBER"
                elif choices == 2:
                    BetPick = "ROYAL"
                elif choices == 3:
                    BetPick = "BICYCLE"
                elif choices == 4 or choices == -1:
                    continue
                else:
                    continue
            elif choices == 3: # Certain card
                choices = arrow_menu("gameCRCertain", (f"{Colours.CYAN}Pick which {Colours.RESET}{Colours.YELLOW}value{Colours.RESET}{Colours.CYAN} you want to bet on{Colours.RESET}\n\n{Colours.GREEN}x_{Colours.RESET} is the multiplier\n{Colours.YELLOW}[__%]{Colours.RESET} is the change of the bet being picked\n"), CRCertainPick)
                BetGroup = "CERTAIN"
                if choices == 0:
                    BetPick = "2"
                elif choices == 1:
                    BetPick = "3"
                elif choices == 2:
                    BetPick = "4"
                elif choices == 3:
                    BetPick = "5"
                elif choices == 4:
                    BetPick = "6"
                elif choices == 5:
                    BetPick = "7"
                elif choices == 6:
                    BetPick = "8"
                elif choices == 7:
                    BetPick = "9"
                elif choices == 8:
                    BetPick = "10"
                elif choices == 9:
                    BetPick = "D"
                elif choices == 10:
                    BetPick = "Q"
                elif choices == 11:
                    BetPick = "K"
                elif choices == 12:
                    BetPick = "A"
                elif choices == 13 or choices == -1:
                    continue
                else:
                    continue
            elif choices == 4: # Specific card
                while True:
                    choices = arrow_menu("gameCRSpecific", (f"{Colours.CYAN}Pick which {Colours.RESET}{Colours.YELLOW}suit{Colours.RESET}{Colours.CYAN} the card you want to bet has{Colours.RESET}\n\n{Colours.GREEN}x_{Colours.RESET} is the multiplier\n{Colours.YELLOW}[__%]{Colours.RESET} is the change of the bet being picked\n"), CRSpecificPick)
                    if choices == 0: # Spades
                        choices = arrow_menu("gameCRSpecificSpades", (f"{Colours.CYAN}Pick which {Colours.RESET}{Colours.YELLOW}card{Colours.RESET}{Colours.CYAN} you want to bet on{Colours.RESET}\n\n{Colours.GREEN}x_{Colours.RESET} is the multiplier\n{Colours.YELLOW}[__%]{Colours.RESET} is the change of the bet being picked\n"), CRSuitsSpades)
                        BetGroup = "SSPECIFIC"
                        if choices == 0:
                            BetPick = "2SPADE"
                        elif choices == 1:
                            BetPick = "3SPADE"
                        elif choices == 2:
                            BetPick = "4SPADE"
                        elif choices == 3:
                            BetPick = "5SPADE"
                        elif choices == 4:
                            BetPick = "6SPADE"
                        elif choices == 5:
                            BetPick = "7SPADE"
                        elif choices == 6:
                            BetPick = "8SPADE"
                        elif choices == 7:
                            BetPick = "9SPADE"
                        elif choices == 8:
                            BetPick = "10SPADE"
                        elif choices == 9:
                            BetPick = "DSPADE"
                        elif choices == 10:
                            BetPick = "QSPADE"
                        elif choices == 11:
                            BetPick = "KSPADE"
                        elif choices == 12:
                            BetPick = "ASPADE"
                        elif choices == 13 or choices == -1:
                            continue
                        else:
                            continue
                    elif choices == 1:# Diamonds
                        choices = arrow_menu("gameCRSpecificDiamonds", (f"{Colours.CYAN}Pick which {Colours.RESET}{Colours.YELLOW}card{Colours.RESET}{Colours.CYAN} you want to bet on{Colours.RESET}\n\n{Colours.GREEN}x_{Colours.RESET} is the multiplier\n{Colours.YELLOW}[__%]{Colours.RESET} is the change of the bet being picked\n"), CRSuitsDiamonds)
                        BetGroup = "DSPECIFIC"
                        if choices == 0:
                            BetPick = "2DIAMOND"
                        elif choices == 1:
                            BetPick = "3DIAMOND"
                        elif choices == 2:
                            BetPick = "4DIAMOND"
                        elif choices == 3:
                            BetPick = "5DIAMOND"
                        elif choices == 4:
                            BetPick = "6DIAMOND"
                        elif choices == 5:
                            BetPick = "7DIAMOND"
                        elif choices == 6:
                            BetPick = "8DIAMOND"
                        elif choices == 7:
                            BetPick = "9DIAMOND"
                        elif choices == 8:
                            BetPick = "10DIAMOND"
                        elif choices == 9:
                            BetPick = "DDIAMOND"
                        elif choices == 10:
                            BetPick = "QDIAMOND"
                        elif choices == 11:
                            BetPick = "KDIAMOND"
                        elif choices == 12:
                            BetPick = "ADIAMOND"
                        elif choices == 13 or choices == -1:
                            continue
                        else:
                            continue
                    elif choices == 2:# heart
                        choices = arrow_menu("gameCRSpecificHearts", (f"{Colours.CYAN}Pick which {Colours.RESET}{Colours.YELLOW}card{Colours.RESET}{Colours.CYAN} you want to bet on{Colours.RESET}\n\n{Colours.GREEN}x_{Colours.RESET} is the multiplier\n{Colours.YELLOW}[__%]{Colours.RESET} is the change of the bet being picked\n"), CRSuitsHearts)
                        BetGroup = "HSPECIFIC"
                        if choices == 0:
                            BetPick = "2HEART"
                        elif choices == 1:
                            BetPick = "3HEART"
                        elif choices == 2:
                            BetPick = "4HEART"
                        elif choices == 3:
                            BetPick = "5HEART"
                        elif choices == 4:
                            BetPick = "6HEART"
                        elif choices == 5:
                            BetPick = "7HEART"
                        elif choices == 6:
                            BetPick = "8HEART"
                        elif choices == 7:
                            BetPick = "9HEART"
                        elif choices == 8:
                            BetPick = "10HEART"
                        elif choices == 9:
                            BetPick = "DHEART"
                        elif choices == 10:
                            BetPick = "QHEART"
                        elif choices == 11:
                            BetPick = "KHEART"
                        elif choices == 12:
                            BetPick = "AHEART"
                        elif choices == 13 or choices == -1:
                            continue
                        else:
                            continue
                    elif choices == 3: #clubs
                        choices = arrow_menu("gameCRSpecificClubs", (f"{Colours.CYAN}Pick which {Colours.RESET}{Colours.YELLOW}card{Colours.RESET}{Colours.CYAN} you want to bet on{Colours.RESET}\n\n{Colours.GREEN}x_{Colours.RESET} is the multiplier\n{Colours.YELLOW}[__%]{Colours.RESET} is the change of the bet being picked\n"), CRSuitsClubs)
                        BetGroup = "CSPECIFIC"
                        if choices == 0:
                            BetPick = "2CLUB"
                        elif choices == 1:
                            BetPick = "3CLUB"
                        elif choices == 2:
                            BetPick = "4CLUB"
                        elif choices == 3:
                            BetPick = "5CLUB"
                        elif choices == 4:
                            BetPick = "6CLUB"
                        elif choices == 5:
                            BetPick = "7CLUB"
                        elif choices == 6:
                            BetPick = "8CLUB"
                        elif choices == 7:
                            BetPick = "9CLUB"
                        elif choices == 8:
                            BetPick = "10CLUB"
                        elif choices == 9:
                            BetPick = "DCLUB"
                        elif choices == 10:
                            BetPick = "QCLUB"
                        elif choices == 11:
                            BetPick = "KCLUB"
                        elif choices == 12:
                            BetPick = "ACLUB"
                    elif choices == 4 or choices == -1:
                        continue
                    else:
                        continue
            elif choices == 5: # Exit Game
                key_press(2)
                USER_WALLET += user_bet
                user_bet = None
                return
            else: # Exit game
                key_press(2)
                USER_WALLET += user_bet
                user_bet = None
                return
            clear_screen()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
        sys.exit()
#----Game 1 - card roulette----#

#----Main Menu----#
def main_menu():
    """Main game menu with arrow navigation"""
    try:
        options = [
            "🎮 Play Card Roulette",                                                #CHANE GAME NAMES
            "📊 View Statistics",
            "❓ Help", 
            "✏️  Change Name",
            "💾 Save Game",
            "🚪 Quit Game"
        ]
        global CURRENT_GAME
        while True:
            if USER_WALLET <= 0:
                financial_aid()
                continue
            else:
                clear_screen()
                
                choice = arrow_menu("menu", None, options)
                
                if choice == 0:  # Play Card roulette game
                    clear_screen()                                                  # GAME 1
                    choice = arrow_menu("confirm-cancel", (f"{Colours.CYAN}Please confirm to play Card Roulette{Colours.RESET}\n"), Confirm_Cancel)
                    card_roulette()
                elif choice == 1:  # View Stats
                    clear_screen()
                    show_stats()
                elif choice == 2:  # tips
                    clear_screen()
                    help_game()
                elif choice == 3:  # Change name
                    clear_screen()
                    name_pick()
                elif choice == 4:
                    save_game()
                    clear_screen()
                    LINE()
                    print(f"{Colours.BOLD}{Colours.BLUE}🏷️  DUCK ROULETTE - SAVE 🏷️{Colours.RESET}")
                    LINE()
                    print(f"{Colours.GREEN}Game saved successfully{Colours.RESET}")
                    LINE()
                    key_press(1)
                elif choice == 5 or choice == -1:  # Quit
                    clear_screen()
                    print(f"{Colours.RED}Thanks for playing! Goodbye!{Colours.RESET}")
                    sys.exit()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Duck Roulette{Colours.RESET}")
        sys.exit()
#----Main Menu----#

#----GAME ----#
def main():
    """Main entry point for the game."""
    clear_screen()
    start_game()
    if USER_NAME is None:
        name_pick()
    save_game()
    main_menu()

if __name__ == "__main__":
    main()