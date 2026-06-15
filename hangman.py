import random

# ─────────────────────────────────────────
#  Horizon TechX — Task 1: Hangman Game
#  Key concepts: random, while loop,
#                if-else, strings, lists
# ─────────────────────────────────────────

WORDS = ["python", "keyboard", "galaxy", "jungle", "wizard"]

HANGMAN_STAGES = [
    # 0 wrong guesses
    """
       -----
       |   |
           |
           |
           |
           |
    ==========""",
    # 1
    """
       -----
       |   |
       O   |
           |
           |
           |
    ==========""",
    # 2
    """
       -----
       |   |
       O   |
       |   |
           |
           |
    ==========""",
    # 3
    """
       -----
       |   |
       O   |
      /|   |
           |
           |
    ==========""",
    # 4
    """
       -----
       |   |
       O   |
      /|\\  |
           |
           |
    ==========""",
    # 5
    """
       -----
       |   |
       O   |
      /|\\  |
      /    |
           |
    ==========""",
    # 6 wrong — dead
    """
       -----
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    ==========""",
]

HINTS = {
    "python":   "A popular programming language",
    "keyboard": "You type on this device",
    "galaxy":   "A system of billions of stars",
    "jungle":   "Dense tropical forest",
    "wizard":   "A magical person with special powers",
}

MAX_WRONG = 6


def display_state(secret, guessed, wrong_letters):
    """Print the current game state to the console."""
    print(HANGMAN_STAGES[len(wrong_letters)])
    print(f"\n  Hint: {HINTS[secret]}")
    print("\n  Word: ", end="")
    for ch in secret:
        print(ch.upper() if ch in guessed else "_", end=" ")
    print()
    if wrong_letters:
        print(f"\n  Wrong letters ({len(wrong_letters)}/{MAX_WRONG}): "
              f"{' '.join(l.upper() for l in sorted(wrong_letters))}")
    print()


def get_valid_input(guessed):
    """Prompt the player until they enter a valid, unused letter."""
    while True:
        guess = input("  Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("  ⚠  Please enter a single letter (a-z).")
        elif guess in guessed:
            print(f"  ⚠  You already guessed '{guess.upper()}'. Try another.")
        else:
            return guess


def play():
    secret = random.choice(WORDS)
    guessed = set()
    wrong_letters = set()

    print("\n" + "=" * 40)
    print("     W E L C O M E  T O  H A N G M A N")
    print("=" * 40)
    print(f"  A {len(secret)}-letter word has been chosen.")
    print(f"  You have {MAX_WRONG} incorrect guesses.\n")

    while True:
        display_state(secret, guessed, wrong_letters)

        # ── Win check ──────────────────────────
        if all(ch in guessed for ch in secret):
            print("  🎉  You won! The word was:", secret.upper())
            break

        # ── Lose check ─────────────────────────
        if len(wrong_letters) >= MAX_WRONG:
            print(HANGMAN_STAGES[MAX_WRONG])
            print("  💀  Game over! The word was:", secret.upper())
            break

        # ── Player's turn ──────────────────────
        letter = get_valid_input(guessed)
        guessed.add(letter)

        if letter in secret:
            print(f"\n  ✅  '{letter.upper()}' is in the word!\n")
        else:
            wrong_letters.add(letter)
            remaining = MAX_WRONG - len(wrong_letters)
            print(f"\n  ❌  '{letter.upper()}' is NOT in the word. "
                  f"{remaining} guess(es) left.\n")


def main():
    while True:
        play()
        again = input("\n  Play again? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Thanks for playing! Goodbye.\n")
            break


if __name__ == "__main__":
    main()