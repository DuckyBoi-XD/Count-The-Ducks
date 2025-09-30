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
    return os.path.expanduser("~/.config/ride-the-duck")                        #CHANGE NAME

def load_game(): # access save file JSON
    '''loading save file - returns both money and name'''
    config_dir = get_config_dir()
    save_path = os.path.join(config_dir, "DuckCountSaveFile.bin")                 #CHANGE GAME NAME
    try:
        with open(save_path, "rb") as f:                                           #ADD ITEMS TO SAVE FILE
            encoded_bytes = f.read()
            json_str = decode_save(encoded_bytes)
            data = json.loads(json_str)
            return (data.get("money", 500),
                    data.get("name", None),
                    data.get("games played", 0),
                    data.get("money earnt", 0),
                    data.get("money lost", 0),
                    data.get("Broke count", 0))
    except FileNotFoundError:
        return 500, None, 0, 0, 0, 0                                                  #ADD ITEMS TO SAVE FILE
    except (ValueError, json.JSONDecodeError) as error:
        return 500, None, 0, 0, 0, 0                                                  #ADD ITEMS TO SAVE FILE

def save_game(money=None, name=None, game_played=None, money_earnt=None, money_lost=None, broke_count=None):               #ADD ITEMS TO SAVE FILE
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
    if broke_count is None:
        broke_count = BROKE_COUNT
    data = {
        "money": money,
        "name": name,
        "games played": game_played,
        "money earnt": money_earnt,
        "money lost": money_lost,
        "Broke count": broke_count
    }
    json_str = json.dumps(data)
    encoded_bytes = encode_save(json_str)
    config_dir = get_config_dir()
    os.makedirs(config_dir, exist_ok=True)
    save_path = os.path.join(config_dir, "DuckCountSaveFile.bin")                   #CHANGE NAME
    with open(save_path, "wb") as f:
        f.write(encoded_bytes)
#--Save File Money--#

#----Preloaded function----#

#---Variables---#
USER_WALLET, USER_NAME, GAMES_PLAYED, MONEY_EARNT, MONEY_LOST, BROKE_COUNT = load_game()  # Load both money and name from save file
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
    if OS == 'Unix':
        os.system('clear')
    elif OS == 'Windows':
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