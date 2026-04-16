import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from data_and_dragons.models import Action, ResolvedNPC, Scenario, JudgementResult, ActionOutcome
from data_and_dragons.dice import DiceRoll, Outcome
from data_and_dragons.judge import Judge


def _make_scenario() -> Scenario:
    return Scenario(
        title="The Excel Catastrophe",
        description="A messy spreadsheet needs cleaning.",
        difficulty="Easy",
        npcs=[
            ResolvedNPC(
                id="sarah_jenkins",
                name="Sarah Jenkins",
                role="Senior Consultant",
                personality="Demanding",
                background="Veteran consultant.",
            )
        ],
    )


# ---------------------------------------------------------------------------
# JudgementResult model tests
# ---------------------------------------------------------------------------

def test_judgement_result_model():
    j = JudgementResult(
        technical_score=80,
        reasoning="Good use of Pandas.",
        verdict="success",
    )
    assert j.technical_score == 80
    assert j.verdict == "success"


def test_judgement_result_score_clamped():
    with pytest.raises(Exception):
        JudgementResult(technical_score=150, reasoning=".", verdict="success")


# ---------------------------------------------------------------------------
# ActionOutcome model tests
# ---------------------------------------------------------------------------

def test_action_outcome_model():
    judgement = JudgementResult(technical_score=70, reasoning="Decent.", verdict="partial")
    roll = DiceRoll(value=12, outcome=Outcome.NORMAL, modifier=12 / 20)
    outcome = ActionOutcome(
        judgement=judgement,
        dice_roll=roll,
        final_score=75,
        narrative="You partially succeed, but Sarah raises an eyebrow.",
    )
    assert outcome.final_score == 75
    assert outcome.dice_roll.value == 12


# ---------------------------------------------------------------------------
# Judge class tests (LLM calls mocked)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_judge_returns_action_outcome(monkeypatch):
    """Judge.evaluate should return an ActionOutcome with a valid final_score."""
    mock_judgement = JudgementResult(
        technical_score=85,
        reasoning="Solid Pandas pipeline proposal.",
        verdict="success",
    )

    judge = Judge()

    # Mock the internal LLM call
    monkeypatch.setattr(judge, "_call_llm", AsyncMock(return_value=mock_judgement))

    with patch("data_and_dragons.judge.roll_d20") as mock_roll:
        mock_roll.return_value = DiceRoll(value=14, outcome=Outcome.NORMAL, modifier=14 / 20)
        scenario = _make_scenario()
        action = Action(player_input="I'll use Pandas to normalise dates and strip currency symbols.")
        outcome = await judge.evaluate(scenario=scenario, action=action)

    assert isinstance(outcome, ActionOutcome)
    assert 0 <= outcome.final_score <= 100
    assert outcome.narrative  # Should have some narrative text
    assert outcome.dice_roll.value == 14


@pytest.mark.asyncio
async def test_judge_critical_fumble_overrides_score(monkeypatch):
    """A critical fumble (roll=1) should significantly penalise the final score."""
    mock_judgement = JudgementResult(
        technical_score=90,
        reasoning="Excellent answer.",
        verdict="success",
    )
    judge = Judge()
    monkeypatch.setattr(judge, "_call_llm", AsyncMock(return_value=mock_judgement))

    with patch("data_and_dragons.judge.roll_d20") as mock_roll:
        mock_roll.return_value = DiceRoll(value=1, outcome=Outcome.CRITICAL_FUMBLE, modifier=1 / 20)
        outcome = await judge.evaluate(scenario=_make_scenario(), action=Action(player_input="Perfect answer."))

    # Even a perfect LLM score should be dragged down by a critical fumble
    assert outcome.final_score < mock_judgement.technical_score


@pytest.mark.asyncio
async def test_judge_critical_success_boosts_score(monkeypatch):
    """A critical success (roll=20) should boost the final score."""
    mock_judgement = JudgementResult(
        technical_score=60,
        reasoning="Average answer.",
        verdict="partial",
    )
    judge = Judge()
    monkeypatch.setattr(judge, "_call_llm", AsyncMock(return_value=mock_judgement))

    with patch("data_and_dragons.judge.roll_d20") as mock_roll:
        mock_roll.return_value = DiceRoll(value=20, outcome=Outcome.CRITICAL_SUCCESS, modifier=1.0)
        outcome = await judge.evaluate(scenario=_make_scenario(), action=Action(player_input="Average answer."))

    assert outcome.final_score > mock_judgement.technical_score


def test_judge_build_prompt_contains_scenario_context():
    """The system and user prompts should include key scenario details."""
    judge = Judge()
    scenario = _make_scenario()
    action = Action(player_input="Use Pandas.")
    system_prompt, user_prompt = judge.build_prompts(scenario=scenario, action=action)

    assert "Excel Catastrophe" in system_prompt
    assert "Sarah Jenkins" in system_prompt
    assert "Use Pandas." in user_prompt
