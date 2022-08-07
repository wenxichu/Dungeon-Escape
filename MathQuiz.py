import math
from PlayerToken import Adventurer
from fractions import Fraction

# Quiz Questions
quiz_easy = {0: ["\nQ1 There are 28 cookies in the jar. Thomas took a dozen cookies. Kevin had 4 more than him. "
                 "How many cookies are left?", 0], 1: ["Q2 Find the SQRT of 64 divided by 2.", int(math.sqrt(64)/2)],
             2: ["Q3 What is the value of (25-4^2)/3?", int((25-math.pow(4, 2))/3)]}

quiz_normal = {0: ["\nQ1 Solve the equation for x. x^2-4=0 where x<0", -abs(2)], 1: [
    "Q2 What is the value of 1/5+1/3?", Fraction(8, 15)],
               2: ["Q3 Solve the proportion for y. Round to the nearest whole number. y/7=8/9", math.floor(6.22)]}

quiz_hard = {0: ["\nQ1 How many ways can you arrange the letters ABCD with no repeats?", math.factorial(4)], 1: [
    "Q2 You flip a quarter 4 times. What is the probability of getting 3 heads in a row?", 0.25], 2: [
    "Q3 Find the sine of pi/2.", int(math.sin(math.pi/2))]}


# Check Answer
class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.number = 0

    def next_question(self):
        current_question = self.questions[self.number]
        self.number += 1
        player_answer = input(f"{current_question[0]} ")
        self.check_answer(player_answer, current_question[1])

    def __lt__(self, other):
        return self.number < other

    @staticmethod
    def check_answer(player_answer, solution):
        if player_answer == str(solution):
            Adventurer.score += 100
            print("\nThat is correct! The skeleton guardian nods its head.")
            print("You have earned 100 points.\n")
        else:
            print("\nThat is incorrect. The skeleton guardian shakes its head.")
            print(f"The right answer is \033[1m{solution}\033[0m\n")


def take_quiz(question_bank):
    quiz = Quiz(question_bank)

    while quiz.__lt__(3):
        quiz.next_question()
