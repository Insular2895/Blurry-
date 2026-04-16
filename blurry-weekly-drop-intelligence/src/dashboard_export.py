from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
CURATED_DIR = BASE_DIR / "data" / "curated"
EXPORT_DIR = BASE_DIR / "data" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_curated(file_name: str) -> pd.DataFrame:
    return pd.read_csv(CURATED_DIR / file_name)


def build_approved_activations(df: pd.DataFrame) -> pd.DataFrame:
    approved = df[df["activation_decision"] == "approve"].copy()

    cols = [
        "activation_date",
        "weekly_drop_id",
        "sku_id",
        "source_location_id",
        "target_country_code",
        "candidate_units",
        "stock_risk_score_v2",
        "market_opportunity_score_v2",
        "landed_cost_v2",
        "recommended_price_v2",
        "avg_market_price",
        "expected_margin_pct",
        "expected_margin_value",
        "activation_score_v2",
        "activation_priority",
        "decision_reason",
    ]

    approved = approved[cols].sort_values("activation_score_v2", ascending=False)
    return approved


def build_scenario_summary(df: pd.DataFrame) -> pd.DataFrame:
    approved = df[df["activation_decision"] == "approve"].copy()

    summary = approved.groupby("scenario_name").agg(
        approved_activations=("sku_id", "count"),
        profitable_activations=("scenario_status", lambda x: (x == "profitable").sum()),
        total_profit=("profit_scn", "sum"),
        avg_unit_margin=("unit_margin_scn", "mean"),
        avg_landed_cost=("landed_cost_scn", "mean"),
        avg_expected_units=("expected_units_to_sell_scn", "mean"),
    ).reset_index()

    return summary.sort_values("total_profit", ascending=False)


def build_rejected_activations(df: pd.DataFrame) -> pd.DataFrame:
    rejected = df[df["activation_decision"] == "reject"].copy()

    cols = [
        "sku_id",
        "source_location_id",
        "target_country_code",
        "pricing_status",
        "market_tier",
        "stock_status",
        "activation_score_v2",
        "decision_reason",
    ]

    rejected = rejected[cols].sort_values("activation_score_v2", ascending=False)
    return rejected


def main() -> None:
    activation_df = load_curated("activation_recommendation.csv")
    scenario_df = load_curated("scenario_analysis.csv")

    approved_df = build_approved_activations(activation_df)
    rejected_df = build_rejected_activations(activation_df)
    scenario_summary_df = build_scenario_summary(scenario_df)

    approved_path = EXPORT_DIR / "approved_activations.csv"
    rejected_path = EXPORT_DIR / "rejected_activations.csv"
    scenario_summary_path = EXPORT_DIR / "scenario_summary.csv"

    approved_df.to_csv(approved_path, index=False)
    rejected_df.to_csv(rejected_path, index=False)
    scenario_summary_df.to_csv(scenario_summary_path, index=False)

    print("\nDASHBOARD EXPORT")
    print("=" * 70)
    print(f"Approved activations: {len(approved_df)} rows")
    print(f"Rejected activations: {len(rejected_df)} rows")
    print(f"Scenario summary: {len(scenario_summary_df)} rows")

    print(f"\nSaved: {approved_path}")
    print(f"Saved: {rejected_path}")
    print(f"Saved: {scenario_summary_path}")


if __name__ == "__main__":
    main()