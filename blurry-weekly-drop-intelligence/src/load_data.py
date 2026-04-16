from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"


REQUIRED_FILES = [
    "dim_sku.csv",
    "dim_location.csv",
    "dim_market.csv",
    "fact_stock_health.csv",
    "fact_market_opportunity.csv",
    "fact_weekly_activation.csv",
    "fact_scenario.csv",
    "fx_rates.csv",
    "shipping_rates.csv",
    "customs_rules.csv",
]


def load_csv(file_name: str) -> pd.DataFrame:
    file_path = RAW_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Missing required file: {file_path}")

    return pd.read_csv(file_path)


def validate_required_files() -> None:
    missing_files = [file_name for file_name in REQUIRED_FILES if not (RAW_DIR / file_name).exists()]

    if missing_files:
        missing_str = "\n".join(f"- {file_name}" for file_name in missing_files)
        raise FileNotFoundError(
            f"The following required files are missing in {RAW_DIR}:\n{missing_str}"
        )


def load_all_data() -> dict[str, pd.DataFrame]:
    validate_required_files()

    datasets = {
        "dim_sku": load_csv("dim_sku.csv"),
        "dim_location": load_csv("dim_location.csv"),
        "dim_market": load_csv("dim_market.csv"),
        "fact_stock_health": load_csv("fact_stock_health.csv"),
        "fact_market_opportunity": load_csv("fact_market_opportunity.csv"),
        "fact_weekly_activation": load_csv("fact_weekly_activation.csv"),
        "fact_scenario": load_csv("fact_scenario.csv"),
        "fx_rates": load_csv("fx_rates.csv"),
        "shipping_rates": load_csv("shipping_rates.csv"),
        "customs_rules": load_csv("customs_rules.csv"),
    }

    return datasets


def print_dataset_overview(datasets: dict[str, pd.DataFrame]) -> None:
    print("\nDataset overview")
    print("-" * 60)

    for name, df in datasets.items():
        print(f"{name}: {df.shape[0]} rows x {df.shape[1]} columns")


def main() -> None:
    datasets = load_all_data()
    print_dataset_overview(datasets)


if __name__ == "__main__":
    main()