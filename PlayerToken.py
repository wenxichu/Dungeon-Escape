import random
import time
from os import linesep
from GenerateMap import DisplayMap


class DungeonMap(DisplayMap):
    steps = 0

    # View Symbols
    @staticmethod
    def read_key():
        symbols = ("A = Adventurer", "D = Door", "G = Gold", "K = Key", "S = Slime", "_ = Free Space")

        for number, letter in enumerate(symbols, 1):
            print(str(number) + ".", letter)

    # Movement
    @classmethod
    def movement(cls):
        action = input("\nSelect an action: (W = Walk, R = Run, S = Stats) ").upper()

        if "W" in action:
            Adventurer.stats["Speed"] = 1
        elif "R" in action:
            Adventurer.stats["Speed"] = 2
        elif "S" in action:
            print(linesep)
            time.sleep(1.0)
            for key, value in Adventurer.stats.items():
                print(key + " = " + str(value))
            print("\n==================")
        elif "K" in action:
            print("\n==================")
            DungeonMap.read_key()
        else:
            print("No such request exists.")
            return False


class Adventurer(DungeonMap):
    score = int(100)
    max_hp = float(0)
    effect = {"Damage": 0, "Coins": 0}
    stats = {"Health": max_hp, "Gold": 0, "Sword": False, "Shield": False, "PowerUp": "None", "Speed": 1}

    def __init__(self, size):
        super().__init__(size)
        self.has_key = 0
        self.roll = 0
        self.total_damage = Adventurer.effect["Damage"]
        self.total_gold = Adventurer.effect["Coins"]

    # Equip Boots
    def get_boots(self):
        self.roll = random.randint(1, 6)
        if self.roll < 3 and Adventurer.stats["PowerUp"] == "None":
            print("\nYou found a pair of boots. You can run now!")
            Adventurer.stats.update({"PowerUp": "Boots"})
        else:
            return False

    # Grab Key
    def grab_key(self, player):
        if player == "K":
            self.has_key = 1
            print("\nYou found a key to the door!")
            return True

    # Take Damage
    @staticmethod
    def take_dmg(player):
        if player == "S" and Adventurer.stats["Health"] > 0:
            print("\nA slime suddenly attacks you!")
            Adventurer.stats["Health"] -= 2
            if Adventurer.stats["Shield"]:
                print("You block the attack with your shield.")
                Adventurer.stats["Health"] += 1.00
            if Adventurer.stats["Sword"]:
                print("You defeat the slime with your sword.")
                Adventurer.stats["Health"] += 0.75
                DisplayMap.defeated += 1
            Adventurer.effect["Damage"] += 2

    # Mine Gold
    @staticmethod
    def mine_gold(player):
        if player == "G":
            print("\nYou picked up some gold. It might be useful later!")
            Adventurer.stats["Gold"] += 1
            Adventurer.effect["Coins"] += 1


class Difficulty:
    levels = 0
    remaining = 0

    # Select Mode
    def __init__(self):
        print('''
E = Easy 
N = Normal 
H = Hard 
        ''')

        game_modes = "Easy__Normal__Hard"
        self.diff_lvl = str(input("Select Your Difficulty: ").title())
        while game_modes.find(self.diff_lvl) == -1:
            print("\nThis level does not exist. Try again!")
            self.diff_lvl = str(input("\nSelect Your Difficulty: ").title())
        self.__contains__(self.diff_lvl)

    def __contains__(self, modes):
        # Easy
        if "E" in modes:
            Difficulty.levels = 4
            Difficulty.remaining = 3
            Adventurer.stats["Gold"] = 2
            Adventurer.max_hp = float(10)
            Adventurer.stats["Health"] = Adventurer.max_hp
            Adventurer.score += 25

        # Normal
        elif "N" in modes:
            Difficulty.levels = 5
            Difficulty.remaining = 4
            Adventurer.stats["Gold"] = 1
            Adventurer.max_hp = float(9)
            Adventurer.stats["Health"] = Adventurer.max_hp
            Adventurer.score += 50

        # Hard
        elif "H" in modes:
            Difficulty.levels = 6
            Difficulty.remaining = 5
            Adventurer.stats["Gold"] = 0
            Adventurer.max_hp = float(8)
            Adventurer.stats["Health"] = Adventurer.max_hp
            Adventurer.score += 100
