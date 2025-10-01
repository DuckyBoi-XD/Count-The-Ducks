#----Import Python Packages----#
#--Save File--#
import json
import base64
import codecs

#--Functions--#
import random
import time

#--Os Check--#
import os
import sys

import termios
import tty

'''import msvcrt'''
#----Import Python Packages----#

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
    return os.path.expanduser("~/.config/counting-ducks")                        #CHANGE NAME

def load_game(): # access save file JSON
    '''loading save file - returns both money and name'''
    global FILE_STATUS
    config_dir = get_config_dir()
    save_path = os.path.join(config_dir, "CountingDucksSaveFile.bin")                 #CHANGE GAME NAME
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
                    data.get("money borrowed", 0))
    except FileNotFoundError:
        FILE_STATUS = 2
        return 500, None, 0, 0, 0, 0                                               #ADD ITEMS TO SAVE FILE
    except (ValueError, json.JSONDecodeError) as error:
        FILE_STATUS = 3
        return 500, None, 0, 0, 0, 0                                                  #ADD ITEMS TO SAVE FILE

def save_game(money=None, name=None, game_played=None, money_earnt=None, money_lost=None, money_borrowed=None):               #ADD ITEMS TO SAVE FILE
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
    if MONEY_BORROWED is None:
        money_borrowed = MONEY_BORROWED
    data = {
        "money": money,
        "name": name,
        "games played": game_played,
        "money earnt": money_earnt,
        "money lost": money_lost,
        "money borrowed": MONEY_BORROWED
    }
    json_str = json.dumps(data)
    encoded_bytes = encode_save(json_str)
    config_dir = get_config_dir()
    os.makedirs(config_dir, exist_ok=True)
    save_path = os.path.join(config_dir, "CountingDucksSaveFile.bin")                   #CHANGE NAME
    with open(save_path, "wb") as f:
        f.write(encoded_bytes)
#--Save File Money--#

#----Preloaded function----#

#---Variables---#
USER_WALLET, USER_NAME, GAMES_PLAYED, MONEY_EARNT, MONEY_LOST, MONEY_BORROWED = load_game()  # Load both money and name from save file
CARD_SUITS = ("♠", "♦", "♥", "♣") # creates suits for card deck creation
USER_NAME_KNOWLEDGE = False

Confirm_Redo = ["✅ Confirm", "🔄 Redo"]
Confirm_Redo_Cancel = ["✅ Confirm", "🔄 Redo", "❌ Cancel"]

card_output = ""
bet_amount = None

RedBlackPick = [
    "🟥 Red",
    "⬛ Black"
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
    elif os.name == 'posix':
        os.system('cls')

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
        print(f"\n{Colours.RED}Thanks for playing Ride The Duck{Colours.RESET}")
        sys.exit()
#----Single Key Track----#

#----Arrow Key Track----#
def arrow_key():
    """Read one key or arrow key"""
    try:
        if os.name == "nt":
            ch = msvcrt.getwch()
            if ch and ord(ch) == 3:
                print(f"\n{Colours.RED}Thanks for playing Ride The Duck{Colours.RESET}")
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
                    print(f"\n{Colours.RED}Thanks for playing Counting Ducks{Colours.RESET}")                    #
                    sys.exit()
                elif ord(key) == 4:  # CTRL-D
                    print(f"\n{Colours.RED}Thanks for playing Counting Ducks{Colours.RESET}")
                    sys.exit()

                if ord(key) == 27:  # ESC
                    # read the next two chars (typical ANSI arrow seq)
                    key += sys.stdin.read(2)
                return key
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Ride The Duck{Colours.RESET}")
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
            #Game information
            LINE()
            #Text above options
                
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
        print(f"\n{Colours.RED}Thanks for playing Ride The Duck{Colours.RESET}")
        sys.exit()

#----Arrow Key Menu System----#

#----Start Game----#
def start_game():
    '''start of game info'''
    try:
        clear_screen()
        LINE()
        print(f"{Colours.BOLD}{Colours.BLUE}🎰 Counting Ducks 🎰{Colours.RESET}\n")
        if FILE_STATUS == 1:
            f"{Colours.BOLD}{Colours.GREEN}💾 Loaded Save File"
        elif FILE_STATUS == 2:
            f"{Colours.BOLD}{Colours.YELLOW}💾 New Save File"
        elif FILE_STATUS == 2:
            f"{Colours.BOLD}{Colours.RED}💾 Corrupted or Tamppered Savee File"
        print(f"{Colours.GREEN}💰 Your Money: ${USER_WALLET}{Colours.RESET}\n"
        f"{Colours.CYAN}🎉 Welcome to Counting Ducks, a gambling game 🎉{Colours.RESET}")
        if USER_NAME is None:
            print(f"{Colours.YELLOW}🏷️  Your  Name:{Colours.RESET}{Colours.RED} -UNKNOWN-{Colours.RESET}")
        else:
            print(f"{Colours.YELLOW}🏷️  Your  Name:{Colours.RESET} {USER_NAME}")
        LINE()
        key_press(1)
        clear_screen()
    except KeyboardInterrupt:
        print(f"{Colours.RED}Thanks for playing Ride The Duck{Colours.RESET}")
        sys.exit()
    except EOFError:
        print(f"{Colours.RED}Thanks for playing Ride The Duck{Colours.RESET}")
        sys.exit() 
#----Start Game----#

#----financial aid----#
def financial_aid():
    """Function to output the last message after losing all your money"""
    global USER_WALLET
    global MONEY_BORROWED
    MONEY_BORROWED + 100
    clear_screen()
    try:
        clear_screen()
        LINE()
        print(f"{Colours.BOLD}{Colours.BLUE}🏷️  RIDE THE DUCK - FINANCIAL AID 🏷️{Colours.RESET}")
        LINE()
        print(f"{Colours.YELLOW}Due to you being {Colours.RED}BROKE{Colours.RESET}{Colours.YELLOW}, you are given {Colours.RESET}{Colours.GREEN}$10{Colours.RESET} {Colours.YELLOW}to hopefully sustain your gambling addiction\n")
        USER_WALLET += 10
        print(f"{Colours.GREEN}You now have ${USER_WALLET}{Colours.RESET}")
        print(f"{Colours.RED}You have borrowed a total of ${MONEY_BORROWED}")
        LINE()
        save_game()
        key_press(1)
    except KeyboardInterrupt:
        print(f"{Colours.RED}Thanks for playing Ride The Duck{Colours.RESET}")
        sys.exit()
    except EOFError:
        print(f"{Colours.RED}Thanks for playing Ride The Duck{Colours.RESET}")
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
            while True:
                clear_screen()
                LINE()
                print(f"{Colours.BOLD}{Colours.BLUE}🎰 RIDE THE DUCK - MAIN GAME - BET 🎰{Colours.RESET}")
                LINE()

                if bet_error == 1:
                    print(f"{Colours.RED}⚠️ Invalid bet: {user_bet} - Please use a number ⚠️{Colours.RESET}")
                elif bet_error == 2:
                    print(f"{Colours.RED}⚠️ Invalid bet: {user_bet} - Please enter a number equal or bigger than 0.01 ⚠️{Colours.RESET}")
                elif bet_error == 3:
                    print(f"{Colours.RED}⚠️ Invalid bet: {user_bet} - You are betting more money than you have in your wallet ⚠️{Colours.RESET}")

                print(f"{Colours.GREEN}💰 Your Money: ${USER_WALLET}{Colours.RESET}\n"
                    f"{Colours.CYAN}💵  How much do you want to bet? (Min $0.01) 💵{Colours.RESET}")
                bet_error = 0
                try:
                    user_bet = input(f"{Colours.BOLD}❯ {Colours.RESET}").strip()
                except (KeyboardInterrupt, EOFError):
                    print(f"\n{Colours.RED}Thanks for playing Ride The Duck{Colours.RESET}")
                    sys.exit()
                
                if is_float(user_bet):
                    if money_valid(user_bet) and float(user_bet) >= 0.01:
                        if float(user_bet) <= USER_WALLET:
                            clear_screen()
                            choices = arrow_menu("menu",
                                f"{Colours.GREEN}💵 You are betting: {Colours.WHITE}${user_bet}{Colours.RESET}\n{Colours.CYAN}✅ Please confirm bet amount ✅{Colours.RESET}\n",
                                Confirm_Redo_Cancel)
                            if choices == 0:
                                clear_screen()
                                bet_confirm = True
                                USER_WALLET -= float(user_bet)
                                bet_amount = float(user_bet)
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
        print(f"\n{Colours.RED}Thanks for playing Ride The Duck{Colours.RESET}")
        sys.exit()

#----Betting check Function----#