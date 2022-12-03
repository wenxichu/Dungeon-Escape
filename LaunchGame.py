import time
from GenerateMap import Generator, DisplayMap
from Dungeon import Command, map_size, SetFlags
from PlayerToken import Adventurer, Difficulty, DungeonMap
from NextFloor import NextLevel, MagicShop, GameOver
from MathQuiz import quiz_easy, quiz_normal, quiz_hard, take_quiz

print("========================")
print("A Simple Dungeon Crawler")
print("========================")

# Intro Text
print("\n== How to Play ==")
print('''
In this game, a horde of undead has locked your adventurer inside a dungeon with many floors.
Your goal is to grab the key, dig for gold, avoid the slimes, and reach the end of each room.
Make your way to the door and try your best to survive. Test your skills on three difficulty levels.
Can you escape the dungeon before running out of moves? Or will you be trapped underground forever?

Type in a letter to control the player token and move it to another place on the map. Good luck!''')
Difficulty()
print("\n==================")


def cont_game(answer):
    if "Y" in answer:
        SetFlags.game_ended = "No"
        print("\nYou enter the dungeon depths once more.")
        print("\nLoading the Game Pieces...")

        NextLevel(map_size).reset_stats()
        NextLevel(map_size).clear_map()
        Adventurer.effect["Damage"] = 0
        Adventurer.effect["Coins"] = 0
        DungeonMap.steps = 0
        DisplayMap.defeated = 0
        Adventurer.score = 100

        Difficulty()
        launch_game(Difficulty.levels, map_size)
    elif "N" in answer:
        if SetFlags.game_ended == "Yes":
            GameOver(map_size).__str__()
        print('''
    You decide it's not worth the trouble to go back down again. Sure you might've missed a few treasures and 
    didn't get to clear all the rooms, but why bother when you would get caught by the skeleton guards anyway? 

    Besides, you haven't eaten in days and you could use a good shower to clean off that slime residue. 
    Oh well, there's no point worrying about it now. You head towards the nearest tavern as the sunset draws close.''')


def helper_fcn():
    options = "Yes_No"
    play_again = input("\nPlay another game? (Y = Yes/N = No) ").upper()

    while options.find(play_again) == -1:
        print("\nError: Invalid Input.")
        play_again = input("\nPlay another game? (Y = Yes/N = No) ").upper()

    return play_again


def launch_game(diff, get_size):

    # Run the Game
    for _ in range(1, diff):
        Command(get_size)
        if SetFlags.game_ended == "Yes":
            cont_game(helper_fcn())
        get_size += 1

    # Quiz Time
    print("\nYour path is blocked by a stone guardian. It will only let you leave if you answer these questions.")

    game_mode = Difficulty.levels

    if game_mode == 4:
        take_quiz(quiz_easy)
    elif game_mode == 5:
        take_quiz(quiz_normal)
    elif game_mode == 6:
        take_quiz(quiz_hard)

    time.sleep(2.0)
    print("Well done, you have finally escaped the dungeon. A bright light shines from above, free at last!")

    # Player Coordinates
    print("\nCoordinates Traveled:")
    path = set(zip(Generator.player_x, Generator.player_y))
    print(path)
    Generator.player_x.clear()
    Generator.player_y.clear()

    # Reset Shop
    MagicShop.prices[0] = 2
    MagicShop.prices[1] = 1
    MagicShop.prices[2] = 2

    # Continue?
    GameOver(map_size).final_score(diff)
    cont_game(helper_fcn())
    print("\n==================")
    quit()


launch_game(Difficulty.levels, map_size)
