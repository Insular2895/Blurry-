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


def compute_market_opportunity(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result["market_price_score"] = min_max_scale(result["avg_market_price"])
    result["demand_score_scaled"] = min_max_scale(result["demand_score"])
    result["trend_score_scaled"] = min_max_scale(result["trend_score"])
    result["volatility_penalty_score"] = inverse_min_max_scale(result["volatility_score"])

    result["market_opportunity_score_v2"] = (
        0.40 * result["demand_score_scaled"]
        + 0.30 * result["market_price_score"]
        + 0.20 * result["trend_score_scaled"]
        + 0.10 * result["volatility_penalty_score"]
    ).round(2)

    result["market_tier"] = pd.cut(
        result["market_opportunity_score_v2"],
        bins=[-1, 45, 65, 100],
        labels=["low_priority", "medium_priority", "high_priority"]
    )

    return result


def print_summary(df: pd.DataFrame) -> None:
    print("\nMARKET OPPORTUNITY SUMMARY")
    print("=" * 70)
    print(f"Rows: {len(df)}")

    print("\nTop product-market opportunities")
    print("-" * 70)
    cols = [
        "sku_id",
        "target_country_code",
        "avg_market_price",
        "demand_score",
        "trend_score",
        "volatility_score",
        "market_opportunity_score_v2",
        "market_tier",
    ]
    top_df = df.sort_values("market_opportunity_score_v2", ascending=False)[cols].head(10)
    print(top_df.to_string(index=False))


def main() -> None:
    datasets = load_all_data()
    market_df = datasets["fact_market_opportunity"]

    enriched_df = compute_market_opportunity(market_df)
    output_path = CURATED_DIR / "market_opportunity_enriched.csv"
    enriched_df.to_csv(output_path, index=False)

    print_summary(enriched_df)
    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    main()