# Solitaire solver
# Copyright (c) 2026 Joshua Taylor

from rich.console import Console
from rich.progress import track
import solver
import cards

# How many random decks we try
NUM_TESTS = 1_000_000


def main():
    console = Console()
    console.print("[bold cyan]Solitaire Solver[/bold cyan]")
    console.print("[dim]Evaluating all possible shuffles...[/dim]")

    # Loop through each possible shuffle of the deck and
    # keep track of how many successful games we get
    success = 0
    fail = 0

    step_counts = []

    for deck in track(
        cards.shuffled(cards.standard_deck(), NUM_TESTS),
        description="Solving games",
        total=NUM_TESTS,
    ):
        # Try to solve the game
        num_steps = solver.solve(deck)
        if num_steps is not None:
            success += 1
            step_counts.append(num_steps)
        else:
            fail += 1

    # Print the results
    console.print(f"[green]Successes:[/green] {success}")
    console.print(f"[red]Failures:[/red] {fail}")
    console.print(
        f"[blue]Percentage solved:[/blue] {success / (success + fail) * 100:.2f}%"
    )
    console.print()
    if step_counts:
        average_steps = sum(step_counts) / len(step_counts)
        console.print(f"[blue]Average steps to solve:[/blue] {average_steps:.2f}")
        median_steps = sorted(step_counts)[len(step_counts) // 2]
        console.print(f"[blue]Median steps to solve:[/blue] {median_steps}")
    else:
        console.print("[yellow]No successful games to calculate statistics.[/yellow]")
    console.print()


if __name__ == "__main__":
    main()
