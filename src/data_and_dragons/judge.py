from typing import Optional, Tuple
from pydantic_ai import Agent
from data_and_dragons.models import Action, ActionOutcome, JudgementResult, Scenario
from data_and_dragons.dice import DiceRoll, Outcome, roll_d20

# ---------------------------------------------------------------------------
# Scoring weights
# ---------------------------------------------------------------------------
_LLM_WEIGHT = 0.75      # LLM technical score contributes 75% of the final score
_DICE_WEIGHT = 0.25     # Dice modifier contributes 25%
_FUMBLE_CAP = 0.40      # Critical fumble: final score capped at 40% of LLM score
_CRIT_BONUS = 15        # Critical success: flat bonus points


SYSTEM_PROMPT_TEMPLATE = """You are the Judge for "Data and Dragons", a gamified data science consultancy simulator.

## Current Scenario: {scenario_title}
**Brief:** {scenario_description}
**Difficulty:** {scenario_difficulty}

## Active NPCs
{npc_profiles}

## Your Role
Evaluate the player's proposed action for its **technical soundness** as a data science consultant.
Be fair but rigorous. A technically correct answer that misses important caveats should score 60–75.
An excellent, nuanced answer referencing best practices should score 85–100.
A vague or incorrect answer should score below 40.

Return a structured evaluation with:
- `technical_score` (0–100): how technically sound is the answer?
- `reasoning`: your concise explanation (2–4 sentences, written as if speaking to the player)
- `verdict`: "success" (score >= 70), "partial" (40–69), or "failure" (< 40)

Keep the tone slightly humorous and engaging — this is a game, after all.
"""

USER_PROMPT_TEMPLATE = """The player says:

"{player_input}"

Evaluate this response and return your structured judgement.
"""


def _build_npc_profiles(scenario: Scenario) -> str:
    all_npcs = scenario.npcs + scenario.other_npcs
    if not all_npcs:
        return "No specific NPCs active in this scenario."
    lines = []
    for npc in all_npcs:
        active_role = npc.scenario_role or npc.role
        lines.append(f"- **{npc.name}** ({active_role}): {npc.personality}. {npc.background}")
    return "\n".join(lines)


def _compute_narrative(judgement: JudgementResult, roll: DiceRoll) -> str:
    """Produce a short, flavourful outcome narrative for the player."""
    if roll.outcome == Outcome.CRITICAL_FUMBLE:
        return (
            f"🎲 *Critical Fumble! You rolled a 1.*\n\n"
            f"{judgement.reasoning}\n\n"
            f"...but then you spill coffee all over the stakeholder's laptop. Timing is everything."
        )
    elif roll.outcome == Outcome.CRITICAL_SUCCESS:
        return (
            f"🎲 *Critical Success! You rolled a 20.*\n\n"
            f"{judgement.reasoning}\n\n"
            f"...and the client spontaneously starts applauding. Stars align."
        )
    else:
        return f"🎲 *You rolled a {roll.value}.*\n\n{judgement.reasoning}"


def _compute_final_score(judgement: JudgementResult, roll: DiceRoll) -> int:
    """Blend LLM technical score with dice modifier; apply critical overrides."""
    base = (judgement.technical_score * _LLM_WEIGHT) + (roll.modifier * 100 * _DICE_WEIGHT)

    if roll.outcome == Outcome.CRITICAL_FUMBLE:
        base = base * _FUMBLE_CAP
    elif roll.outcome == Outcome.CRITICAL_SUCCESS:
        base = base + _CRIT_BONUS

    return min(100, max(0, round(base)))


class Judge:
    """
    The LLM-powered Judge for Data and Dragons.

    Evaluates player actions against the current scenario using a Pydantic-AI agent,
    then combines that evaluation with a virtual dice roll to produce the final outcome.
    """

    def __init__(self, model: str = "openai:gpt-4o-mini"):
        self._model = model
        self._agent: Optional[Agent[None, JudgementResult]] = None

    def _get_agent(self) -> Agent:
        """Lazily construct the agent on first LLM call."""
        if self._agent is None:
            self._agent = Agent(model=self._model, result_type=JudgementResult)
        return self._agent

    def build_prompts(self, scenario: Scenario, action: Action) -> Tuple[str, str]:
        """Build the system and user prompts for the LLM call."""
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            scenario_title=scenario.title,
            scenario_description=scenario.description,
            scenario_difficulty=scenario.difficulty,
            npc_profiles=_build_npc_profiles(scenario),
        )
        user_prompt = USER_PROMPT_TEMPLATE.format(player_input=action.player_input)
        return system_prompt, user_prompt

    async def _call_llm(self, scenario: Scenario, action: Action) -> JudgementResult:
        """Send the evaluation request to the LLM and return the structured result."""
        system_prompt, user_prompt = self.build_prompts(scenario, action)
        result = await self._get_agent().run(user_prompt, system_prompt=system_prompt)
        return result.data

    async def evaluate(self, scenario: Scenario, action: Action) -> ActionOutcome:
        """
        Evaluate a player action and return a full ActionOutcome.

        Combines LLM judgement (75%) with a virtual dice roll (25%),
        applying critical fumble and critical success overrides.
        """
        judgement = await self._call_llm(scenario, action)
        roll = roll_d20()
        final_score = _compute_final_score(judgement, roll)
        narrative = _compute_narrative(judgement, roll)

        return ActionOutcome(
            judgement=judgement,
            dice_roll=roll,
            final_score=final_score,
            narrative=narrative,
        )
