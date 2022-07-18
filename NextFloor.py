import sys
import time
import os
from PlayerToken import Adventurer, Difficulty, DungeonMap
from GenerateMap import Treasure, Slime, DoorKey, DisplayMap


class MagicShop:
    prices = [2, 1, 2]

    def __init__(self):
        self._sword = MagicShop.prices[0]
        self._shield = MagicShop.prices[1]
        self._restore = MagicShop.prices[2]
        # Magic Shop
        print("\nA magic shop appears before you!")
        print(f"\n1 = Sword (Cost: {self._sword} Gold)"
              f"\n2 = Shield (Cost: {self._shield} Gold)"
              f"\n3 = Potion (Cost: {self._restore} Gold)"
              f"\n4 = Nothing (Cost: Free)")
        self.shop = input("\nWhat would you like to buy? ")
        self.buy_item(self.shop)
        if self.shop != "4":
            self.second = input("\nAnything else you want? ")
            self.buy_item(self.second)
        print("\n==================")
        time.sleep(2.5)
        self.item_cost()

    @property
    def sword(self):
        return self._sword

    @property
    def shield(self):
        return self._shield

    @property
    def restore(self):
        return self._restore

    @classmethod
    def buy_item(cls, item):
        # Items for Sale
        if item == "1" and Adventurer.stats["Gold"] >= MagicShop.prices[0]:
            print("You get a medieval sword.")
            Adventurer.stats["Gold"] -= MagicShop.prices[0]
            Adventurer.stats["Sword"] = True
        elif item == "2" and Adventurer.stats["Gold"] >= MagicShop.prices[1]:
            print("You get a wooden shield.")
            Adventurer.stats["Gold"] -= MagicShop.prices[1]
            Adventurer.stats["Shield"] = True
        elif item == "3" and Adventurer.stats["Gold"] >= MagicShop.prices[2]:
            print("You drank a health potion.")
            Adventurer.stats["Gold"] -= MagicShop.prices[2]
            Adventurer.stats["Health"] = float(Adventurer.max_hp)
        elif item == "4":
            print("Nothing ventured is nothing gained.")
            return None
        else:
            print("You don't have enough gold...")
            return None

    @staticmethod
    def item_cost():
        # Raise Cost
        MagicShop.prices[0] += 1
        MagicShop.prices[1] += 1
        MagicShop.prices[2] += 1


# Level Complete
class NextLevel(Adventurer):

    def __init__(self, size):
        super().__init__(size)

    def load(self):
        print(os.linesep + "You manage to reach the exit...but you haven't escaped yet.")
        print("\nYour status ailments have worn off.")
        time.sleep(2.0)
        self.reset_stats()
        Difficulty.remaining -= 1
        if Difficulty.remaining > 0:
            MagicShop()
        self.clear_map()

    @classmethod
    def clear_map(cls):
        Treasure.index = 0
        Slime.index = 0
        DoorKey.index = 0
        # Reset Grid
        Treasure.gold_x.clear()
        Treasure.gold_y.clear()
        Slime.spawn_x.clear()
        Slime.spawn_y.clear()

    @staticmethod
    def reset_stats():
        Adventurer.stats["Shield"] = False
        Adventurer.stats["Sword"] = False
        Adventurer.stats["PowerUp"] = "None"
        Adventurer.stats["Speed"] = 1


class GameOver(Adventurer):

    # Game Over
    def out_of_moves(self):
        # Out of Moves
        print("\nGAME OVER: You have no more moves left.")
        print("You are too exhausted to keep going.")
        self.final_score(Difficulty.levels - Difficulty.remaining)
        self.__str__()

    def out_of_health(self):
        # Health is 0
        print("\nGAME OVER: You ran out of health.")
        print("Your consciousness gradually slips away.")
        self.final_score(Difficulty.levels - Difficulty.remaining)
        self.__str__()

    def __str__(self):
        print("\nThis is your new home now. You sit next to the green slimes.")
        print("The spooky skeletons feed you a few scraps out of pity...")
        print("\n==================")
        sys.exit()

    # Get Score
    def final_score(self, levels):
        Adventurer.score -= DungeonMap.steps - 1
        print(f"\nTotal Steps: {DungeonMap.steps}")
        Adventurer.score -= self.total_damage * 5
        print(f"Damage Taken: {self.total_damage}")
        Adventurer.score += int(self.total_gold) * 10
        print(f"Coins Collected: {self.total_gold}")
        Adventurer.score += DisplayMap.defeated * 20
        print(f"Slimes Defeated: {DisplayMap.defeated}")
        Adventurer.score += int(levels-1) * 50
        print(f"Levels Completed: {levels-1}")
        print("\nYour final score is: " + str(Adventurer.score))
