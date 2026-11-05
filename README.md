# Natural Numbers Interpretation

Command-line app for the Omilia programming assignment. It takes the numbers recognized from a spoken phone number (for example `2 10 69 30 6 6 4`), prints the number, says whether it is a valid Greek phone number, and lists every way the number could have been said.

## Requirements

- Python 3.9 or newer (tested with Python 3.9.0 on Windows)
- No external libraries for the app. pytest is only needed for the tests.

## Run

```
python main.py
```

Type the numbers separated by spaces and press Enter. An empty line exits.

```
Enter a number: 2 10 69 30 6 6 4
Number: 2106930664  Phone number: VALID

Possible interpretations (4):
   1. 2106930664   VALID
   2. 21060930664  INVALID
   3. 2106093664   VALID
   4. 210693664    INVALID
```

## Tests

```
pip install pytest
python -m pytest
```

The tests cover all the examples from the assignment, plus some edge cases.

## How it works

1. Each token is split into the number words it could come from: `724` is seven hundred, twenty, four. `69` is sixty, nine. `16` stays as sixteen, because it is one word.
2. A recursive function tries every way of grouping those words back into numbers that can be said as one: hundreds + tens + units, tens + units, hundreds + teens, and so on. Results are memoized by position.
3. Each grouping gives one interpretation. The first one is always the number exactly as recognized. Duplicates are removed.

This covers the three cases in the assignment with one rule: `20 5` can be 25 or 205, `75` can be 75 or 705, and `700 24` can be 724 or 70024.

## Assumptions

- Numbers are spoken in English, as in the examples. 10 to 19 are single words, so `10 6` is never 16.
- Each token has 1 to 3 digits. Anything else is rejected with a message. Extra spaces are ignored.
- Tokens with a leading zero, like `05`, are taken as they are.
- Only the first interpretation has a fixed position. The rest may come in a different order than in the assignment.

## Limitations

- Acoustic confusions like "sixteen" vs "sixty" are out of scope. The input is taken as the speech recognizer's output.
- Cases like `2 100` read as "two hundred" are not handled.
- The number of interpretations grows exponentially with the number of ambiguities. That is fine for phone numbers.

## In a voice dialog

If exactly one interpretation is a valid phone number, the bot can confirm it. If several are valid, it should read the number back digit by digit or ask which one is right. If none is valid, it should ask again and say the expected format.

