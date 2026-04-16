from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
CURATED_DIR = BASE_DIR / "data" / "curated"


def load_curated(file_name: str) -> pd.DataFrame:
    return pd.read_csv(CURATED_DIR / file_name)


def compute_activation_recommendation(
    stock_df: pd.DataFrame,
    market_df: pd.DataFrame,
    pricing_df: pd.DataFrame,
) -> pd.DataFrame:
    result = pricing_df.copy()

    stock_cols = [
        "sku_id",
        "location_id",
        "stock_risk_score_v2",
        "slow_moving_flag_v2",
        "eligible_for_drop_flag_v2",
        "stock_status",
    ]

    result = result.merge(
        stock_df[stock_cols],
        left_on=["sku_id", "source_location_id"],
        right_on=["sku_id", "location_id"],
        how="left"
    ).drop(columns=["location_id"])

    market_cols = [
        "sku_id",
        "target_country_code",
        "market_opportunity_score_v2",
        "market_tier",
    ]

    result = result.merge(
        market_df[market_cols],
        on=["sku_id", "target_country_code"],
        how="left"
    )

    result["activation_score_v2"] = (
        0.35 * result["stock_risk_score_v2"]
        + 0.35 * result["market_opportunity_score_v2"]
        + 0.20 * (result["expected_margin_pct"] * 100)
        + 0.10 * result["candidate_units"]
    ).round(2)

    result["activation_decision"] = "reject"

    approved_condition = (
        (result["eligible_for_drop_flag_v2"] == 1) &
        (result["pricing_status"] == "market_supports_price") &
        (result["market_opportunity_score_v2"] >= 50)
    )

    result.loc[approved_condition, "activation_decision"] = "approve"

    result["activation_priority"] = pd.cut(
        result["activation_score_v2"],
        bins=[-1, 50, 70, 100],
        labels=["low", "medium", "high"]
    )

    result["decision_reason"] = "insufficient_combined_score"

    result.loc[result["eligible_for_drop_flag_v2"] != 1, "decision_reason"] = "stock_not_eligible"
    result.loc[
        (result["eligible_for_drop_flag_v2"] == 1) &
        (result["pricing_status"] != "market_supports_price"),
        "decision_reason"
    ] = "price_not_supported_by_market"
    result.loc[
        (result["eligible_for_drop_flag_v2"] == 1) &
        (result["pricing_status"] == "market_supports_price") &
        (result["market_opportunity_score_v2"] < 50),
        "decision_reason"
    ] = "market_opportunity_too_low"
    result.loc[approved_condition, "decision_reason"] = "approved_for_weekly_drop"

    return result


def print_summary(df: pd.DataFrame) -> None:
    print("\nACTIVATION SUMMARY")
    print("=" * 70)
    print(f"Rows: {len(df)}")
    print(f"Approved: {(df['activation_decision'] == 'approve').sum()}")
    print(f"Rejected: {(df['activation_decision'] == 'reject').sum()}")

    print("\nApproved activations")
    print("-" * 70)
    approved_cols = [
        "sku_id",
        "source_location_id",
        "target_country_code",
        "stock_risk_score_v2",
        "market_opportunity_score_v2",
        "expected_margin_pct",
        "candidate_units",
        "activation_score_v2",
        "activation_priority",
        "activation_decision",
        "decision_reason",
    ]

    approved_df = df[df["activation_decision"] == "approve"] \
        .sort_values("activation_score_v2", ascending=False)[approved_cols]

    if approved_df.empty:
        print("No approved activations.")
    else:
        print(approved_df.to_string(index=False))

    print("\nRejected activations")
    print("-" * 70)
    rejected_cols = [
        "sku_id",
        "source_location_id",
        "target_country_code",
        "pricing_status",
        "market_tier",
        "activation_score_v2",
        "activation_decision",
        "decision_reason",
    ]

    rejected_df = df[df["activation_decision"] == "reject"] \
        .sort_values("activation_score_v2", ascending=False)[rejected_cols]

    if rejected_df.empty:
        print("No rejected activations.")
    else:
        print(rejected_df.to_string(index=False))


def main() -> None:
    stock_df = load_curated("stock_health_enriched.csv")
    market_df = load_curated("market_opportunity_enriched.csv")
    pricing_df = load_curated("pricing_enriched.csv")

    result_df = compute_activation_recommendation(stock_df, market_df, pricing_df)

    output_path = CURATED_DIR / "activation_recommendation.csv"
    result_df.to_csv(output_path, index=False)

    print_summary(result_df)
    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    main()