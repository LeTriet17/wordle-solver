import requests
import random
import string
import logging
from typing import List, Set, Dict
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class GuessResult:
    slot: int
    guess: str
    result: str

class WordleAPIError(Exception):
    """Custom exception for Wordle API errors"""
    pass

class WordleSolver:
    def __init__(self, word_length: int = 5, max_attempts: int = 100, seed: int = None, api_url: str = None):
        self.word_length = word_length
        self.max_attempts = max_attempts
        self.seed = seed
        self.possible_letters = [set(string.ascii_lowercase) for _ in range(word_length)]
        self.api_url = api_url

    def make_guess(self, guess: str) -> List[GuessResult]:
        params = {"guess": guess, "size": self.word_length, "seed": self.seed}
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            return [GuessResult(**r) for r in response.json()]
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise WordleAPIError(f"Failed to make a guess: {e}")

    @staticmethod
    def generate_random_word(length: int) -> str:
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    def filter_words(self, guess: str, result: List[GuessResult]) -> None:
        for r in result:
            if r.result == 'correct':
                self.possible_letters[r.slot] = {r.guess}
            elif r.result == 'present':
                if r.guess in self.possible_letters[r.slot]:
                    self.possible_letters[r.slot].remove(r.guess)
                for j in range(self.word_length):
                    if j != r.slot:
                        self.possible_letters[j].add(r.guess)
            elif r.result == 'absent':
                for letters in self.possible_letters:
                    if r.guess in letters and len(letters) > 1:
                        letters.remove(r.guess)

    def choose_word(self) -> str:
        return ''.join(random.choice(list(letters) or string.ascii_lowercase) for letters in self.possible_letters)

    def calculate_possible_words(self) -> int:
        return max(1, *(len(letters) for letters in self.possible_letters))

    def solve(self) -> None:
        for attempt in range(1, self.max_attempts + 1):
            try:
                guess = self.choose_word()
                logger.info(f"Attempt {attempt}: Guessing '{guess}'")
                
                result = self.make_guess(guess)
                logger.info(f"Result: {result}")
                
                self.filter_words(guess, result)
                
                if all(r.result == 'correct' for r in result):
                    logger.info(f"Word guessed correctly in {attempt} attempts!")
                    logger.info(f"Word: {guess}")
                    return
                
                possible_words = self.calculate_possible_words()
                logger.info(f"Possible words remaining: approximately {possible_words}")
            
            except WordleAPIError as e:
                logger.error(f"Wordle API error: {e}")
                logger.info("Generating a new random word and continuing...")
                continue
            except Exception as e:
                logger.exception(f"An unexpected error occurred: {e}")
                logger.info("Generating a new random word and continuing...")
                continue

        logger.warning(f"Failed to guess the word within {self.max_attempts} attempts.")

def main():
    solver = WordleSolver(word_length=5, max_attempts=100, seed=42, api_url="https://wordle.votee.dev:8000/random")
    solver.solve()

if __name__ == "__main__":
    main()