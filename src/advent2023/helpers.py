from pathlib import Path


def read_input_as_lines(day_name: str, sample: bool = False) -> list[str]:
    day_number = Path(day_name).name[3:5]
    with open(f"input/day{day_number}{'.sample' if sample else ''}.txt") as f:
        return f.read().splitlines()
