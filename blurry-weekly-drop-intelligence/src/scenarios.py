from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
CURATED_DIR = BASE_DIR / "data" / "curated"


def load_curated(file_name: str) -> pd.DataFrame:
    return pd.read_csv(CURATED_DIR / file_name)


def apply_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    scenarios = [
        {"scenario_name": "base", "fx_multiplier": 1.00, "shipping_multiplier": 1.00, "demand_multiplier": 1.00},
        {"scenario_name": "stress_fx", "fx_multiplier": 1.50, "shipping_multiplier": 1.00, "demand_multiplier": 1.00},
        {"scenario_name": "stress_shipping", "fx_multiplier": 1.00, "shipping_multiplier": 1.30, "demand_multiplier": 1.00},
        {"scenario_name": "stress_demand", "fx_multiplier": 1.00, "shipping_multiplier": 1.00, "demand_multiplier": 0.80},
        {"scenario_name": "combined_worst", "fx_multiplier": 1.50, "shipping_multiplier": 1.30, "demand_multiplier": 0.75},
    ]

    all_rows = []

    for scenario in scenarios:
        tmp = df.copy()

        tmp["scenario_name"] = scenario["scenario_name"]

        tmp["shipping_cost_scn"] = (
            tmp["shipping_cost_v2"] * scenario["shipping_multiplier"]
        ).round(2)

        tmp["fx_buffer_scn"] = (
            tmp["fx_buffer_v2"] * scenario["fx_multiplier"]
        ).round(2)

        tmp["landed_cost_scn"] = (
            tmp["buy_price_eur"]
            + tmp["shipping_cost_scn"]
            + tmp["customs_cost_v2"]
            + tmp["packaging_cost_v2"]
            + tmp["qc_cost_v2"]
            + tmp["fx_buffer_scn"]
        ).round(2)

        tmp["expected_units_to_sell_scn"] = (
            tmp["expected_units_to_sell"] * scenario["demand_multiplier"]
        ).round(2)

        tmp["unit_margin_scn"] = (
            tmp["recommended_price_v2"] - tmp["landed_cost_scn"]
        ).round(2)

        tmp["profit_scn"] = (
            tmp["unit_margin_scn"] * tmp["expected_units_to_sell_scn"]
        ).round(2)

        tmp["scenario_status"] = tmp["profit_scn"].apply(
            lambda x: "profitable" if x > 0 else "not_profitable"
        )

        all_rows.append(tmp)

    return pd.concat(all_rows, ignore_index=True)


def print_summary(df: pd.DataFrame) -> None:
    approved_df = df[df["activation_decision"] == "approve"].copy()

    print("\nSCENARIO SUMMARY")
    print("=" * 70)

    summary = approved_df.groupby("scenario_name").agg(
        approved_activations=("sku_id", "count"),
        profitable_activations=("scenario_status", lambda x: (x == "profitable").sum()),
        total_profit=("profit_scn", "sum"),
        avg_unit_margin=("unit_margin_scn", "mean"),
    ).reset_index()

    print(summary.to_string(index=False))

    print("\nApproved activations by scenario")
    print("-" * 70)
    cols = [
        "scenario_name",
        "sku_id",
        "source_location_id",
        "target_country_code",
        "landed_cost_scn",
        "recommended_price_v2",
        "expected_units_to_sell_scn",
        "unit_margin_scn",
        "profit_scn",
        "scenario_status",
    ]
    print(
        approved_df[cols]
        .sort_values(["scenario_name", "profit_scn"], ascending=[True, False])
        .to_string(index=False)
    )


def main() -> None:
    activation_df = load_curated("activation_recommendation.csv")
    scenario_df = apply_scenarios(activation_df)

    output_path = CURATED_DIR / "scenario_analysis.csv"
    scenario_df.to_csv(output_path, index=False)

    print_summary(scenario_df)
    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    main()