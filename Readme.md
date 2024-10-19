# Wordle Solver

This project implements an automated solver for the Wordle game using a simple API. The solver uses a strategy of generating and refining possible words based on the feedback from each guess.

## Features

- Automated solving of Wordle puzzles
- Configurable word length and maximum number of attempts
- Logging of solving process and results
- Error handling for API requests and unexpected issues
- Random word generation for initial guesses and error recovery

## Requirements

- Python 3.7+
- `requests` library

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/LeTriet17/wordle-solver.git
   cd wordle-solver
   ```

2. Install the required dependencies:
   ```
   pip install requests
   ```

## Usage

To run the Wordle solver:

```
python wordle_solver.py
```

By default, the solver will attempt to guess a 5-letter word within 100 attempts.

## Configuration

You can modify the following parameters in the `main()` function of `wordle_solver.py`:

- `word_length`: The length of the word to guess (default: 5)
- `max_attempts`: The maximum number of guessing attempts (default: 100)
- `seed`: A seed value for random number generation (default: 42)

## How It Works

1. The solver starts by considering all lowercase letters as possible for each position in the word.
2. For each guess:
   - It chooses a word based on the current possible letters for each position.
   - It sends this guess to the Wordle API.
   - Based on the API's response, it updates the possible letters for each position.
   - If the guess is correct, the solver terminates successfully.
   - If the maximum number of attempts is reached, the solver terminates unsuccessfully.