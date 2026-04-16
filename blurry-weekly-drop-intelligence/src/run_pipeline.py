import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"


PIPELINE_STEPS = [
    "load_data.py",
    "data_quality_check.py",
    "stock_health.py",
    "market_opportunity.py",
    "pricing.py",
    "activation.py",
    "scenarios.py",
    "dashboard_export.py",
]


def run_step(script_name: str) -> None:
    script_path = SRC_DIR / script_name

    print("\n" + "=" * 80)
    print(f"RUNNING: {script_name}")
    print("=" * 80)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Pipeline failed on step: {script_name}")


def main() -> None:
    print("\nBLURRY WEEKLY DROP INTELLIGENCE — FULL PIPELINE")
    print("=" * 80)

    for step in PIPELINE_STEPS:
        run_step(step)

    print("\n" + "=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    main()