from enum import Enum
from typing import List, NamedTuple, Iterator


class LetterState(Enum):
    not_guessed_yet = "not_guessed_yet"
    not_present = "not_present"
    incorrect_position = "incorrect_position"
    correct_position = "correct_position"


class LetterAndState(NamedTuple):
    letter: str
    state: LetterState


def check_guess(guess: str, solution: str) -> list[list[str, LetterState]] | str:
    if guess == solution:
        return "WIN"
    pool = {}
    for g, s in zip(guess, solution):
        if g == s:
            continue
        if s in pool:
            pool[s] += 1
        else:
            pool[s] = 1

    states = []
    for guess_letter, solution_letter in zip(guess, solution):
        if guess_letter == solution_letter:
            states.append([guess_letter, LetterState.correct_position])
        elif guess_letter in solution and guess_letter in pool and pool[guess_letter] > 0:
            states.append([guess_letter, LetterState.incorrect_position])
            pool[guess_letter] -= 1
        else:
            states.append([guess_letter, LetterState.not_present])
    return states


def check_guesses(solution: str, *guesses: str) -> Iterator[list[LetterAndState]]:
    for guess in guesses:
        yield check_guess(guess, solution)
