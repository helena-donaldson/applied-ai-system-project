import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from logic_utils import check_guess, get_range_for_difficulty
    
def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 50)

def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 100)
    
def test_guess_correct():
    outcome, message = check_guess(10, 10)

    assert outcome == "Win"
    assert "Correct" in message

def test_guess_too_high():
    outcome, message = check_guess(20, 10)

    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    outcome, message = check_guess(5, 10)

    assert outcome == "Too Low"
    assert "HIGHER" in message
