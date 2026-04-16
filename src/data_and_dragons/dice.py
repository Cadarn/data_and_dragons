import random
from enum import Enum
from pydantic import BaseModel, computed_field


class Outcome(str, Enum):
    CRITICAL_FUMBLE = "critical_fumble"  # Roll of 1 — disaster strikes
    NORMAL = "normal"                    # Roll of 2–19
    CRITICAL_SUCCESS = "critical_success"  # Roll of 20 — fortune favours the bold


class DiceRoll(BaseModel):
    value: int
    outcome: Outcome
    modifier: float  # Normalised 0.0–1.0 for blending into scoring


def roll_d20() -> DiceRoll:
    """Roll a d20 and return the result with its outcome classification."""
    value = random.randint(1, 20)

    if value == 1:
        outcome = Outcome.CRITICAL_FUMBLE
    elif value == 20:
        outcome = Outcome.CRITICAL_SUCCESS
    else:
        outcome = Outcome.NORMAL

    return DiceRoll(value=value, outcome=outcome, modifier=value / 20)
