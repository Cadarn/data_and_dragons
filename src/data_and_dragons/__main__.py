"""
Data and Dragons — CLI entry point.

Run with: uv run python -m data_and_dragons
"""

import asyncio
import glob
import os
import sys

from dotenv import load_dotenv

# Load .env from the project root (two levels up from this file in src/data_and_dragons/)
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(os.path.join(_project_root, ".env"))

from data_and_dragons.models import Player
from data_and_dragons.scenario_loader import NPCRoster, ScenarioLoader
from data_and_dragons.game_loop import GameLoop

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
NPC_ROSTER_PATH = os.path.join(DATA_DIR, "npcs.yaml")
SCENARIOS_GLOB = os.path.join(DATA_DIR, "scenarios", "*.yaml")

_SEPARATOR = "─" * 60


def _print_banner():
    print()
    print("  🐉  DATA AND DRAGONS  📊")
    print("  Roll for Data Quality.")
    print(_SEPARATOR)
    print()


def _print_scenario(scenario):
    print(f"\n📋  Scenario: {scenario.title}  [{scenario.difficulty}]")
    print(_SEPARATOR)
    print(scenario.description.strip())

    all_npcs = scenario.npcs + scenario.other_npcs
    if all_npcs:
        print("\n👥  People you can talk to:")
        for npc in all_npcs:
            active_role = npc.scenario_role or npc.role
            print(f"   • {npc.name} — {active_role}")
    print()


def _print_outcome(outcome):
    print()
    print(_SEPARATOR)
    print(outcome.narrative)
    print()
    print(f"  📊  Technical Score : {outcome.judgement.technical_score}/100")
    print(f"  🎲  Dice Roll       : {outcome.dice_roll.value}/20  ({outcome.dice_roll.outcome.value})")
    print(f"  ✅  Final Score     : {outcome.final_score}/100")
    print(_SEPARATOR)
    print()


async def run():
    _print_banner()

    # Check API key early
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY is not set. The Judge will not be able to evaluate answers.")
        print("   Set it with: export OPENAI_API_KEY='sk-...'")
        print()

    # Load player name
    name = input("Enter your consultant name: ").strip() or "Anonymous"
    player = Player(name=name)
    print(f"\nWelcome, {name}. Your first client is waiting.\n")

    # Load NPC roster and scenarios
    roster = NPCRoster(NPC_ROSTER_PATH).load()
    scenario_paths = sorted(glob.glob(SCENARIOS_GLOB))
    if not scenario_paths:
        print("❌  No scenario files found in data/scenarios/. Exiting.")
        sys.exit(1)

    scenarios = [ScenarioLoader(path, roster).load() for path in scenario_paths]
    loop = GameLoop(player=player, scenarios=scenarios)

    # Main game loop
    while loop.is_running:
        scenario = loop.current_scenario
        _print_scenario(scenario)

        print("What is your plan of attack? (Type your response below.)")
        print("  [Press Enter twice to submit, or type 'skip' to move on]\n")

        lines = []
        try:
            while True:
                line = input()
                if line.lower() == "skip":
                    lines = ["[Player skipped this scenario.]"]
                    break
                if line == "" and lines:
                    break
                if line:
                    lines.append(line)
        except (EOFError, KeyboardInterrupt):
            print("\n\nGame interrupted. Thanks for playing!")
            break

        player_input = " ".join(lines)
        if not player_input:
            continue

        print("\n⚖️  The Judge is deliberating...\n")
        try:
            outcome = await loop.process_turn(player_input)
            _print_outcome(outcome)
        except Exception as e:
            print(f"❌  The Judge encountered an error: {e}")
            print("   (Check your OPENAI_API_KEY and network connection.)\n")

        input("Press Enter to continue to the next scenario...")
        loop.advance_scenario()

    # Game over
    print()
    print(_SEPARATOR)
    print(f"  🏁  GAME OVER  —  Final Consultancy Score: {loop.player.score}")
    print(_SEPARATOR)
    print()


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
