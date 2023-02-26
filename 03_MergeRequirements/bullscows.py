from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from random import choice
import urllib.request


def parse_args():
    parser = ArgumentParser("Play a game of bullcows")
    parser.add_argument('dictionary', help="Path/URL of dictionary to be used during the game")
    parser.add_argument('length', nargs='?', type=int, help="Word length")

    return parser.parse_args()


def ask(prompt: str, valid: list[str] = None) -> str:
    while True:
        guess = input(prompt)
        if valid is not None and guess not in valid:
            print('Такого слова нет в словаре')
            continue
        else:
            break

    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def bullscows(guess: str, secret: str) -> (int, int):
    if len(guess) != len(secret):
        raise ValueError("Guess and secret strings must have the same lengths")

    bulls = sum([guess_char == secret_char for guess_char, secret_char in zip(guess, secret)])
    cows = (Counter(guess) & Counter(secret)).total()
    
    return bulls, cows
            

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    if len(words) == 0:
        raise ValueError("Dictionary is empty")

    secret = choice(words)
    tries = 0

    while True:
        tries += 1
        guess = ask("Введите слово: ", words)
        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)

        if bulls == len(secret):
            break

    return tries


if __name__ == '__main__':
    args = parse_args()

    if Path(args.dictionary).exists():
        with Path(args.dictionary).open() as f:
            dictionary = list(map(lambda x: x.strip(), f.readlines()))
    else:
        with urllib.request.urlopen(args.dictionary) as f:
            dictionary = list(map(lambda x: x.decode('utf-8').strip(), f.readlines()))


    if args.length is not None:
        dictionary = [word for word in dictionary if len(word) == args.length]

    gameplay(ask, inform, dictionary)
