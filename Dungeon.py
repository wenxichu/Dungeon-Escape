import numpy
import time
from GenerateMap import Generator
from PlayerToken import Adventurer, DungeonMap
from NextFloor import NextLevel, GameOver

map_size = 3


class SetFlags(Adventurer):
    game_ended = "No"

    def power_up(self):
        if Adventurer.stats["PowerUp"] == "Boots":
            self.movement()

    def replace(self, loc_x, loc_y, slime):
        if Adventurer.stats["Sword"]:
            self.dungeon[loc_y][loc_x] = "A"
        else:
            self.dungeon[slime] = "S"

    def hit_wall(self):
        print("\nYou've hit a wall. Ouch!")
        self.moves_left -= 1
        print(f"Moves Left: {self.moves_left}\n")
        Adventurer.stats["Health"] -= 1
        print(self.dungeon)

    def end_game(self):
        if self.moves_left <= 0:
            GameOver(map_size).out_of_moves()
            return True
        elif Adventurer.stats["Health"] <= 0:
            GameOver(map_size).out_of_health()
            return True
        else:
            self.moves_left -= 1
            DungeonMap.steps += 1

    @classmethod
    def level_complete(cls):
        print("\nWell done, you've made it to the end!\n")
        print("Steps Taken: " + str(DungeonMap.steps))
        NextLevel(map_size).load()


# Movement
class Command(SetFlags):

    def __init__(self, size):
        super().__init__(size)
        x, y = (0, 0)
        a, b = numpy.where(self.dungeon == "D")
        slime_token = numpy.where(self.dungeon == "S")
        del Generator.player_x[0]
        del Generator.player_y[0]
        self.__str__()
        # Player Actions
        while True:
            print("\nMove your adventurer token. (K = Map Key)")
            # PowerUp
            self.power_up()
            # Controls
            self.move = input("\nL = Left, R = Right, U = Up, or D = Down? ").upper()
            # Map Key
            if self.move == "K":
                time.sleep(1.0)
                print("\n==================")
                DungeonMap.read_key()
                continue
            print("\n==================")
            # Move Token
            direction = {"L", "R", "U", "D"}

            if self.move in direction:
                self.dungeon[y][x] = "_"
                speed = Adventurer.stats["Speed"]
                # Direction
                if self.move == "L" and x - speed >= 0:
                    x -= speed
                elif self.move == "R" and x + speed <= self.size - 1:
                    x += speed
                elif self.move == "D" and y + speed <= self.size - 1:
                    y += speed
                elif self.move == "U" and y - speed >= 0:
                    y -= speed
                else:
                    self.dungeon[y][x] = "A"
                    self.hit_wall()
                    continue
                # Game Over?
                if self.end_game():
                    SetFlags.game_ended = "Yes"
                    break
                # Block Types
                self.mine_gold(self.dungeon[y][x])
                self.take_dmg(self.dungeon[y][x])
                self.grab_key(self.dungeon[y][x])
                # Save Coordinates
                self.dungeon[y][x] = "A"
                Generator.player_x.append(x)
                Generator.player_y.append(y)
            else:
                # Invalid Moves
                print("\nError: Please try again.\n")
                self.dungeon[y][x] = "A"
                print(self.dungeon)
                continue
            # Replace Location
            self.dungeon[a[0]][b[0]] = "D"
            self.replace(x, y, slime_token)
            # Door Conditions
            if self.dungeon[y][x] == self.dungeon[a[0]][b[0]] and self.has_key:
                self.dungeon[a[0]][b[0]] = "A"
                self.level_complete()
                break
            elif self.dungeon[y][x] == self.dungeon[a[0]][b[0]] and not self.has_key:
                print("\nThe door is locked. Where is the key?")
            # Dungeon Output
            print(f"\nMoves Left: \033[1m{self.moves_left}\033[0m")
            print("You are here:\n")
            print(self.dungeon)
            self.get_boots()

