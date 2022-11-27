import numpy
import time
import random


class Generator:
    player_x, player_y = [], []

    def __init__(self, size):
        # Generate Map
        self.size = size
        self.moves_left = 0
        self.dungeon = numpy.array([["_"] * self.size for _ in range(self.size)])
        self.starting_point()
        self.exit_door()

    def number_moves(self):
        # Moves Remaining
        self.moves_left = int(self.size ** 2 - numpy.floor(self.size / 2))
        return self.moves_left

    def starting_point(self):
        # Start Position
        self.dungeon[0][0] = "A"
        Generator.player_x.append(0)
        Generator.player_y.append(0)

    def exit_door(self):
        # Door Location
        row = self.size - 1
        column = random.randrange(2, self.size)
        self.dungeon[row][column] = "D"


class Treasure(Generator):
    gold_x, gold_y = [], []
    index = 0

    def __init__(self, size):
        Generator.__init__(self, size)
        self.number_moves()
        self.dimension = str(self.size) + " x " + str(self.size)

        while Treasure.index < self.gold_amount():
            row = random.randint(0, self.size - 1)
            column = random.randint(0, self.size - 1)
            # Deposit Gold
            if self.dungeon[row][column] == "_":
                self.dungeon[row][column] = "G"
                Treasure.gold_x.append(row)
                Treasure.gold_y.append(column)
                Treasure.index += 1
                continue

    def gold_amount(self):
        # Gold Count
        gold = {3: 2, 4: 5, 5: 9, 6: 14, 7: 19, 8: 26}
        return gold[self.size]


class Slime(Treasure):
    spawn_x, spawn_y = [], []
    index = 0

    def __init__(self, size):
        Treasure.__init__(self, size)
        number = [value for value in range(self.size)]
        quantity = Treasure(size).gold_amount()

        while Slime.index < self.__sub__(quantity):
            row = random.choice(number)
            column = random.choice(number)
            # Spawn Slimes
            if self.dungeon[row][column] == "_":
                self.dungeon[row][column] = "S"
                Slime.spawn_x.append(row)
                Slime.spawn_y.append(column)
                Slime.index += 1
                continue

    def __sub__(self, other):
        # Slime Count
        self.slime_count = other - 1
        return self.slime_count


class DoorKey(Slime):
    index = 0

    def __init__(self, size):
        Slime.__init__(self, size)
        self.__iter__()
        self.__next__()

    def __iter__(self):
        return DoorKey.index

    def __next__(self):
        while DoorKey.index < 1:
            row = random.randrange(1, self.size)
            column = random.randrange(self.size)
            # Drop Key
            if self.dungeon[row][column] == "_":
                self.dungeon[row][column] = "K"
                DoorKey.index += 1
                continue


class DisplayMap(DoorKey):
    defeated = 0

    def __init__(self, size):
        DoorKey.__init__(self, size)

    def __str__(self):
        time.sleep(1.5)
        if self.size == 3:
            print(f"\nGenerating the dungeon map...\n" + f"\nMap Size: \033[1m{self.dimension}\033[0m"
                  f"\nMoves Left: \033[1m{self.moves_left}\033[0m")
            print("\nCan you find a way out?\n")
            print(self.dungeon)
        elif self.size > 3:
            print("\nYou hear happy slime noises nearby." + "\nLoading the next level...")
            print(f"\nMap Size: \033[1m{self.dimension}\033[0m" + f"\nMoves Left: \033[1m{self.number_moves()}\033[0m")
            print("\nCan you find a way out?\n")
            print(self.dungeon)

