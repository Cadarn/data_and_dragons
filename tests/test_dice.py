import pytest
from unittest.mock import patch
from data_and_dragons.dice import roll_d20, DiceRoll, Outcome

# ---------------------------------------------------------------------------
# Dice roll tests
# ---------------------------------------------------------------------------

def test_roll_d20_returns_value_in_range():
    for _ in range(100):
        r = roll_d20()
        assert 1 <= r.value <= 20

def test_roll_d20_critical_success():
    with patch("data_and_dragons.dice.random.randint", return_value=20):
        r = roll_d20()
    assert r.value == 20
    assert r.outcome == Outcome.CRITICAL_SUCCESS

def test_roll_d20_critical_fumble():
    with patch("data_and_dragons.dice.random.randint", return_value=1):
        r = roll_d20()
    assert r.value == 1
    assert r.outcome == Outcome.CRITICAL_FUMBLE

def test_roll_d20_normal_high():
    with patch("data_and_dragons.dice.random.randint", return_value=15):
        r = roll_d20()
    assert r.outcome == Outcome.NORMAL

def test_dice_roll_score_modifier():
    """DiceRoll should expose a normalised 0.0–1.0 modifier for score blending."""
    with patch("data_and_dragons.dice.random.randint", return_value=10):
        r = roll_d20()
    assert 0.0 <= r.modifier <= 1.0
