from pathlib import Path
import pandas as pd

from load_data import load_all_data


BASE_DIR = Path(__file__).resolve().parents[1]
CURATED_DIR = BASE_DIR / "data" / "curated"
CURATED_DIR.mkdir(parents=True, exist_ok=True)


def pick_first_existing_column(df: pd.DataFrame, candidates: list[str], label: str) -> str:
    for col in candidates:
        if col in df.columns:
            return col
    raise KeyError(f"No column found for {label}. Tried: {candidates}")


def compute_pricing(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    activation = datasets["fact_weekly_activation"].copy()
    dim_sku = datasets["dim_sku"].copy()
    dim_location = datasets["dim_location"].copy()
    dim_market = datasets["dim_market"].copy()
    market = datasets["fact_market_opportunity"].copy()
    fx_rates = datasets["fx_rates"].copy()
    shipping_rates = datasets["shipping_rates"].copy()
    customs_rules = datasets["customs_rules"].copy()

    location_country_col = pick_first_existing_column(
        dim_location,
        ["country_code", "source_country_code", "location_country_code", "region_code"],
        "dim_location country column"
    )
    location_name_col = pick_first_existing_column(
        dim_location,
        ["location_name", "boutique_name", "warehouse_name", "name"],
        "dim_location name column"
    )

    market_name_col = pick_first_existing_column(
        dim_market,
        ["country_name", "market_name", "target_country_name", "name"],
        "dim_market name column"
    )
    market_currency_col = pick_first_existing_column(
        dim_market,
        ["currency_code", "currency", "target_currency_code"],
        "dim_market currency column"
    )

    activation = activation.merge(
        dim_sku[["sku_id", "brand", "model_name", "buy_price_eur", "target_margin_pct"]],
        on="sku_id",
        how="left"
    )

    activation = activation.merge(
        dim_location[["location_id", location_country_col, location_name_col]],
        left_on="source_location_id",
        right_on="location_id",
        how="left"
    ).rename(
        columns={
            location_country_col: "source_country_code",
            location_name_col: "source_location_name",
        }
    ).drop(columns=["location_id"])

    activation = activation.merge(
        dim_market[["target_country_code", market_name_col, market_currency_col]],
        on="target_country_code",
        how="left"
    ).rename(
        columns={
            market_name_col: "target_country_name",
            market_currency_col: "currency_code",
        }
    )

    activation = activation.merge(
        market[["sku_id", "target_country_code", "avg_market_price"]],
        on=["sku_id", "target_country_code"],
        how="left"
    )

    activation = activation.merge(
        shipping_rates,
        on=["source_country_code", "target_country_code"],
        how="left"
    )

    activation = activation.merge(
        customs_rules,
        on=["source_country_code", "target_country_code"],
        how="left"
    )

    activation = activation.merge(
        fx_rates,
        on="currency_code",
        how="left"
    )

    missing_shipping = activation["shipping_cost_eur"].isna().sum()
    missing_customs = activation["customs_pct"].isna().sum()
    missing_fx = activation["fx_rate_to_eur"].isna().sum()

    if missing_shipping > 0:
        raise ValueError(f"Missing shipping rate for {missing_shipping} rows")

    if missing_customs > 0:
        raise ValueError(f"Missing customs rule for {missing_customs} rows")

    if missing_fx > 0:
        raise ValueError(f"Missing FX rate for {missing_fx} rows")

    activation["shipping_cost_v2"] = activation["shipping_cost_eur"].round(2)
    activation["customs_cost_v2"] = (
        activation["buy_price_eur"] * activation["customs_pct"]
    ).round(2)

    activation["packaging_cost_v2"] = 3.00
    activation["qc_cost_v2"] = 2.50

    activation["fx_buffer_v2"] = (
        activation["buy_price_eur"] * activation["fx_buffer_pct"]
    ).round(2)

    activation["landed_cost_v2"] = (
        activation["buy_price_eur"]
        + activation["shipping_cost_v2"]
        + activation["customs_cost_v2"]
        + activation["packaging_cost_v2"]
        + activation["qc_cost_v2"]
        + activation["fx_buffer_v2"]
    ).round(2)

    activation["recommended_price_v2"] = (
        activation["landed_cost_v2"] / (1 - activation["target_margin_pct"])
    ).round(2)

    activation["price_vs_market_gap"] = (
        activation["avg_market_price"] - activation["recommended_price_v2"]
    ).round(2)

    activation["expected_margin_value"] = (
        activation["recommended_price_v2"] - activation["landed_cost_v2"]
    ).round(2)

    activation["pricing_status"] = activation["price_vs_market_gap"].apply(
        lambda x: "market_supports_price" if x >= 0 else "price_above_market"
    )

    ordered_columns = [
        "activation_date",
        "weekly_drop_id",
        "sku_id",
        "brand",
        "model_name",
        "source_location_id",
        "source_location_name",
        "source_country_code",
        "target_country_code",
        "target_country_name",
        "currency_code",
        "fx_rate_to_eur",
        "fx_buffer_pct",
        "buy_price_eur",
        "shipping_cost_v2",
        "avg_ship_delay_days",
        "customs_pct",
        "customs_cost_v2",
        "packaging_cost_v2",
        "qc_cost_v2",
        "fx_buffer_v2",
        "landed_cost_v2",
        "target_margin_pct",
        "recommended_price_v2",
        "avg_market_price",
        "price_vs_market_gap",
        "expected_margin_pct",
        "expected_margin_value",
        "candidate_units",
        "expected_units_to_sell",
        "pricing_status",
    ]

    return activation[ordered_columns]


def print_summary(df: pd.DataFrame) -> None:
    print("\nPRICING SUMMARY")
    print("=" * 70)
    print(f"Rows: {len(df)}")

    cols = [
        "sku_id",
        "source_location_id",
        "target_country_code",
        "buy_price_eur",
        "shipping_cost_v2",
        "customs_cost_v2",
        "fx_buffer_v2",
        "landed_cost_v2",
        "recommended_price_v2",
        "avg_market_price",
        "price_vs_market_gap",
        "pricing_status",
    ]

    print("\nPricing review")
    print("-" * 70)
    print(df[cols].sort_values("price_vs_market_gap", ascending=False).to_string(index=False))


def main() -> None:
    datasets = load_all_data()
    pricing_df = compute_pricing(datasets)

    output_path = CURATED_DIR / "pricing_enriched.csv"
    pricing_df.to_csv(output_path, index=False)

    print_summary(pricing_df)
    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    main()