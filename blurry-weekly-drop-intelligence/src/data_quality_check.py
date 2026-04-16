from pathlib import Path
import pandas as pd

from load_data import load_all_data


BASE_DIR = Path(__file__).resolve().parents[1]
CURATED_DIR = BASE_DIR / "data" / "curated"
CURATED_DIR.mkdir(parents=True, exist_ok=True)


REQUIRED_COLUMNS = {
    "dim_sku": [
        "sku_id",
        "brand",
        "model_name",
        "buy_price_eur",
        "target_margin_pct",
    ],
    "dim_location": [
        "location_id",
        "location_name",
        "country_code",
    ],
    "dim_market": [
        "target_country_code",
        "currency_code",
    ],
    "fact_stock_health": [
        "sku_id",
        "location_id",
        "on_hand_qty",
        "days_in_stock_avg",
        "sell_through_rate_30d",
    ],
    "fact_market_opportunity": [
        "sku_id",
        "target_country_code",
        "avg_market_price",
        "demand_score",
        "trend_score",
        "volatility_score",
    ],
    "fact_weekly_activation": [
        "weekly_drop_id",
        "sku_id",
        "source_location_id",
        "target_country_code",
        "candidate_units",
        "expected_units_to_sell",
        "expected_margin_pct",
    ],
     "fact_scenario": [
        "sku_id",
        "target_country_code",
        "fx_shock_pct",
        "shipping_shock_pct",
        "demand_shock_pct",
    ],
    "fx_rates": [
        "currency_code",
        "fx_rate_to_eur",
        "fx_buffer_pct",
    ],
    "shipping_rates": [
        "source_country_code",
        "target_country_code",
        "shipping_cost_eur",
        "avg_ship_delay_days",
    ],
    "customs_rules": [
        "source_country_code",
        "target_country_code",
        "customs_pct",
    ],
}


DUPLICATE_KEY_CANDIDATES = {
    "dim_sku": [["sku_id"]],
    "dim_location": [["location_id"]],
    "dim_market": [["target_country_code"], ["market_id"]],
    "fact_stock_health": [
        ["stock_date", "sku_id", "location_id"],
        ["snapshot_date", "sku_id", "location_id"],
        ["sku_id", "location_id"],
    ],
    "fact_market_opportunity": [
        ["snapshot_date", "sku_id", "target_country_code"],
        ["market_date", "sku_id", "target_country_code"],
        ["sku_id", "target_country_code"],
    ],
    "fact_weekly_activation": [
        ["weekly_drop_id", "sku_id", "source_location_id", "target_country_code"],
    ],
    "fact_scenario": [
        ["scenario_id", "sku_id", "source_location_id", "target_country_code"],
        ["scenario_id", "sku_id", "target_country_code"],
        ["sku_id", "target_country_code"],
    ],
    "fx_rates": [["currency_code"]],
    "shipping_rates": [["source_country_code", "target_country_code"]],
    "customs_rules": [["source_country_code", "target_country_code"]],
}


def get_existing_duplicate_keys(df_name: str, df: pd.DataFrame) -> list[str] | None:
    candidates = DUPLICATE_KEY_CANDIDATES.get(df_name, [])

    for keys in candidates:
        if all(col in df.columns for col in keys):
            return keys

    return None


def check_columns(df_name: str, df: pd.DataFrame) -> list[str]:
    required = REQUIRED_COLUMNS[df_name]
    actual = list(df.columns)

    errors = []
    missing = [col for col in required if col not in actual]

    if missing:
        errors.append(f"{df_name}: missing required columns -> {missing}")

    return errors


def check_nulls(df_name: str, df: pd.DataFrame) -> list[str]:
    errors = []

    null_counts = df.isnull().sum()
    null_cols = null_counts[null_counts > 0]

    if not null_cols.empty:
        errors.append(f"{df_name}: null values found -> {null_cols.to_dict()}")

    return errors


def check_duplicates(df_name: str, df: pd.DataFrame) -> list[str]:
    errors = []

    keys = get_existing_duplicate_keys(df_name, df)
    if keys is None:
        errors.append(f"{df_name}: no valid duplicate key available for current schema")
        return errors

    duplicate_count = df.duplicated(subset=keys).sum()
    if duplicate_count > 0:
        errors.append(f"{df_name}: duplicate rows found on keys {keys} -> {duplicate_count}")

    return errors


def save_clean_copy(df_name: str, df: pd.DataFrame) -> None:
    output_path = CURATED_DIR / f"{df_name}_clean.csv"
    df.to_csv(output_path, index=False)


def print_check_result(label: str, errors: list[str]) -> None:
    if errors:
        print(f"[ERROR] {label}")
        for err in errors:
            print(f"  - {err}")
    else:
        print(f"[OK] {label}")


def check_foreign_keys(datasets: dict[str, pd.DataFrame]) -> list[str]:
    errors = []

    sku_ids = set(datasets["dim_sku"]["sku_id"])
    location_ids = set(datasets["dim_location"]["location_id"])
    market_ids = set(datasets["dim_market"]["target_country_code"])

    if "fact_stock_health" in datasets:
        if not set(datasets["fact_stock_health"]["sku_id"]).issubset(sku_ids):
            errors.append("fact_stock_health: invalid sku_id detected")
        if not set(datasets["fact_stock_health"]["location_id"]).issubset(location_ids):
            errors.append("fact_stock_health: invalid location_id detected")

    if "fact_market_opportunity" in datasets:
        if not set(datasets["fact_market_opportunity"]["sku_id"]).issubset(sku_ids):
            errors.append("fact_market_opportunity: invalid sku_id detected")
        if not set(datasets["fact_market_opportunity"]["target_country_code"]).issubset(market_ids):
            errors.append("fact_market_opportunity: invalid target_country_code detected")

    if "fact_weekly_activation" in datasets:
        if not set(datasets["fact_weekly_activation"]["sku_id"]).issubset(sku_ids):
            errors.append("fact_weekly_activation: invalid sku_id detected")
        if not set(datasets["fact_weekly_activation"]["source_location_id"]).issubset(location_ids):
            errors.append("fact_weekly_activation: invalid source_location_id detected")
        if not set(datasets["fact_weekly_activation"]["target_country_code"]).issubset(market_ids):
            errors.append("fact_weekly_activation: invalid target_country_code detected")

    if "fact_scenario" in datasets:
        scenario_df = datasets["fact_scenario"]

        if "sku_id" in scenario_df.columns:
            if not set(scenario_df["sku_id"]).issubset(sku_ids):
                errors.append("fact_scenario: invalid sku_id detected")

        if "source_location_id" in scenario_df.columns:
            if not set(scenario_df["source_location_id"]).issubset(location_ids):
                errors.append("fact_scenario: invalid source_location_id detected")

        if "target_country_code" in scenario_df.columns:
            if not set(scenario_df["target_country_code"]).issubset(market_ids):
                errors.append("fact_scenario: invalid target_country_code detected")

    return errors


def main() -> None:
    datasets = load_all_data()

    print("\nDATA QUALITY CHECK")
    print("=" * 70)

    all_errors = []

    for name, df in datasets.items():
        print(f"\n{name}")
        print("-" * 70)

        column_errors = check_columns(name, df)
        null_errors = check_nulls(name, df)
        duplicate_errors = check_duplicates(name, df)

        print_check_result("columns", column_errors)
        print_check_result("nulls", null_errors)
        print_check_result("duplicates", duplicate_errors)

        all_errors.extend(column_errors)
        all_errors.extend(null_errors)
        all_errors.extend(duplicate_errors)

        if not column_errors and not null_errors and not duplicate_errors:
            save_clean_copy(name, df)

    print("\nFOREIGN KEY CHECK")
    print("-" * 70)

    fk_errors = check_foreign_keys(datasets)
    print_check_result("foreign keys", fk_errors)
    all_errors.extend(fk_errors)

    if all_errors:
        print("\nQUALITY CHECK FAILED")
        print("=" * 70)
        for err in all_errors:
            print(f"- {err}")
        raise ValueError("Data quality check failed")

    print("\nQUALITY CHECK PASSED")
    print("=" * 70)
    print("Clean copies saved in data/curated/")


if __name__ == "__main__":
    main()