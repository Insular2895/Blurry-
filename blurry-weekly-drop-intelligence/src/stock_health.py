from pathlib import Path
import pandas as pd

from load_data import load_all_data


BASE_DIR = Path(__file__).resolve().parents[1]
CURATED_DIR = BASE_DIR / "data" / "curated"
CURATED_DIR.mkdir(parents=True, exist_ok=True)


def min_max_scale(series: pd.Series) -> pd.Series:
    min_val = series.min()
    max_val = series.max()

    if min_val == max_val:
        return pd.Series([50.0] * len(series), index=series.index)

    return ((series - min_val) / (max_val - min_val)) * 100


def inverse_min_max_scale(series: pd.Series) -> pd.Series:
    min_val = series.min()
    max_val = series.max()

    if min_val == max_val:
        return pd.Series([50.0] * len(series), index=series.index)

    return ((max_val - series) / (max_val - min_val)) * 100


def compute_stock_health(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result["days_in_stock_score"] = min_max_scale(result["days_in_stock_avg"])
    result["low_sell_through_score"] = inverse_min_max_scale(result["sell_through_rate_30d"])
    result["excess_stock_score"] = min_max_scale(result["on_hand_qty"])

    result["stock_risk_score_v2"] = (
        0.40 * result["days_in_stock_score"]
        + 0.35 * result["low_sell_through_score"]
        + 0.25 * result["excess_stock_score"]
    ).round(2)

    result["slow_moving_flag_v2"] = (
        (result["days_in_stock_avg"] > 45) |
        (result["sell_through_rate_30d"] < 0.18)
    ).astype(int)

    result["eligible_for_drop_flag_v2"] = (
        (result["slow_moving_flag_v2"] == 1) &
        (result["stock_risk_score_v2"] >= 60)
    ).astype(int)

    result["stock_status"] = result["eligible_for_drop_flag_v2"].map({
        1: "activate_candidate",
        0: "hold_local"
    })

    return result


def print_summary(df: pd.DataFrame) -> None:
    print("\nSTOCK HEALTH SUMMARY")
    print("=" * 70)
    print(f"Rows: {len(df)}")
    print(f"Slow-moving products: {df['slow_moving_flag_v2'].sum()}")
    print(f"Eligible for weekly drop: {df['eligible_for_drop_flag_v2'].sum()}")

    print("\nTop activation candidates")
    print("-" * 70)
    cols = [
        "sku_id",
        "location_id",
        "on_hand_qty",
        "days_in_stock_avg",
        "sell_through_rate_30d",
        "stock_risk_score_v2",
        "stock_status",
    ]
    top_df = df.sort_values("stock_risk_score_v2", ascending=False)[cols].head(10)
    print(top_df.to_string(index=False))


def main() -> None:
    datasets = load_all_data()
    stock_df = datasets["fact_stock_health"]

    enriched_df = compute_stock_health(stock_df)
    output_path = CURATED_DIR / "stock_health_enriched.csv"
    enriched_df.to_csv(output_path, index=False)

    print_summary(enriched_df)
    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    main()