from letter_state import LetterState
from typing import List
from wordle import Wordle
from colorama import Fore
import random


# interface class
def main():
    word_set = load_word_set("wordle_words.txt")
    secret = random.choice(list(word_set))
    wordle = Wordle(secret)

    while wordle.can_attempt:
        x = input("\nType your guess: ")

        if len(x) != wordle.WORD_LENGTH:
            print(Fore.RED + f"Word must be {wordle.WORD_LENGTH} characters long!" + Fore.RESET)
            # Print error statement in red, and reset in the end
            continue

        '''
        if x not in word_set:
            print(Fore.RED + f"{x} is not a valid word!" + Fore.RESET)
            continue 
        '''

        wordle.attempt(x)

        if not wordle.is_solved:
            display_attempts(wordle)

        display_board(wordle)

    if wordle.is_solved:
        print("\nYou've solved the puzzle!")
    else:
        print("\nYou failed to solve the puzzle!")
        print(f"The secret word was: { Fore.BLUE + wordle.secret + Fore.RESET}")


def display_board(wordle: Wordle):
    lines = []

    for word in wordle.attempts:
        result = wordle.guess(word)
        colored_result_str = convert_result_to_color(result)
        lines.append(colored_result_str)

    # use underscore in Python, if you want a placeholder variable
    for _ in range(wordle.remaining_attempts):
        lines.append(" ".join(["_"] * wordle.WORD_LENGTH))

    draw_border_around(lines)


def display_attempts(wordle: Wordle):
    print(f"\nYou have {wordle.remaining_attempts} attempts left.")


# asks for a string input
def load_word_set(path: str):
    word_set = set()  # set() creates a dictionary, that is able to hold each value that's assigned
    with open(path, "r") as f:  # while loop opens the text file, reads each line (.readlines not .readline),
        # erases the spaces and makes it uppercase
        for line in f.readlines():
            word = line.strip().upper()
            word_set.add(word)
    return word_set


def convert_result_to_color(result: List[LetterState]):
    result_with_color = []
    for letter in result:
        if letter.is_in_position:
            color = Fore.GREEN
        elif letter.is_in_word:
            color = Fore.YELLOW
        else:
            color = Fore.WHITE
        colored_letter = color + letter.character + Fore.RESET
        result_with_color.append(colored_letter)
    return " ".join(result_with_color)


def draw_border_around(lines: List[str], size: int = 4, pad: int = 1):
    content_length = size + pad * 2
    top_border = "┌" + ("─" * content_length) + "┐"
    bottom_border = "└" + ("─" * content_length) + "┘"
    space = " " * pad
    print(f"\n{top_border}")

    for line in lines:
        print("│" + space + line + space + "│")

    print(bottom_border)


if __name__ == "__main__":
    main()
