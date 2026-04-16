# Blurry Weekly Drop Intelligence

Blurry Weekly Drop Intelligence is a portfolio project that simulates a business decision system for an international sneaker and streetwear resale network.

Blurry works with multiple partner boutiques and local stock points. The business problem is not to move products every day across the network, but to identify when unsold stock should be activated through a controlled **weekly drop / raffle sale mechanism**.

Products only move when Blurry decides to activate them through this weekly system. Outside of these weekly drops, stock stays local in order to reduce operational risk, unnecessary logistics costs, and margin erosion.

The objective of the project is to determine:

- which products should be activated
- from which boutique/location
- for which target market
- at what recommended price
- under what margin and scenario constraints

---

## 1. Business context

Some products underperform in their local catchment area and remain unsold for too long.  
At the same time, demand, pricing power, logistics costs, customs exposure, and FX risk differ across international markets.

Blurry's operating model is intentionally simple:

- stock is held locally by partner boutiques
- stock does **not** circulate continuously across the network
- stock is only moved when selected for a **weekly drop**
- weekly drops are the single controlled mechanism used to reallocate and monetize slow-moving inventory internationally

This makes the project different from a traditional marketplace or warehouse optimization project.  
The goal is not real-time fulfillment orchestration.  
The goal is to support **high-quality weekly activation decisions**.

---

## 2. Project objective

Build a lightweight but credible decision-support pipeline that helps answer:

- Which products are slow-moving enough to be activation candidates?
- Which international markets offer the best opportunity for those products?
- Does the market support the price required after shipping, customs, packaging, QC and FX buffer?
- Which activations should Blurry approve for the next weekly drop?
- How resilient are those recommendations under stress scenarios?

---

## 3. What the project covers

This project includes:

- a limited portfolio of 5 products
- 5 partner locations / boutiques
- 5 target markets
- synthetic but realistic stock and demand signals
- pricing logic with landed cost
- shipping, customs and FX enrichment
- stock activation logic
- weekly drop recommendation logic
- scenario analysis
- reproducible pipeline execution
- exported CSV outputs ready for dashboarding

This project does **not** include:

- real-time marketplace API integration
- live operational dispatching
- full warehouse execution
- advanced optimization solver
- production-grade orchestration
- actual payment or order management flows

---

## 4. Project logic

The pipeline follows a simple business logic:

### Step 1 — Identify stock under pressure
Find products that are sitting too long locally and show weak local sell-through.

### Step 2 — Measure market opportunity
Estimate which target countries have stronger demand, pricing support and acceptable volatility.

### Step 3 — Calculate landed cost
For each source-location / target-market pair, compute total cost including:

- buy price
- shipping cost
- customs cost
- packaging cost
- quality control cost
- FX risk buffer

### Step 4 — Check price feasibility
Compare the recommended selling price to observed market price.

### Step 5 — Approve or reject activation
Only approve weekly drops where:

- stock is eligible
- market opportunity is strong enough
- price is supported by market reality
- expected margin remains acceptable

### Step 6 — Stress test decisions
Evaluate how approved activations perform under:

- FX stress
- shipping stress
- demand stress
- combined worst-case scenario

---

## 5. Repository structure

```text
blurry-weekly-drop-intelligence/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   ├── dim_sku.csv
│   │   ├── dim_location.csv
│   │   ├── dim_market.csv
│   │   ├── fact_stock_health.csv
│   │   ├── fact_market_opportunity.csv
│   │   ├── fact_weekly_activation.csv
│   │   ├── fact_scenario.csv
│   │   ├── fx_rates.csv
│   │   ├── shipping_rates.csv
│   │   └── customs_rules.csv
│   ├── curated/
│   │   ├── stock_health_enriched.csv
│   │   ├── market_opportunity_enriched.csv
│   │   ├── pricing_enriched.csv
│   │   ├── activation_recommendation.csv
│   │   ├── scenario_analysis.csv
│   │   └── *_clean.csv
│   └── exports/
│       ├── approved_activations.csv
│       ├── rejected_activations.csv
│       └── scenario_summary.csv
└── src/
    ├── load_data.py
    ├── data_quality_check.py
    ├── stock_health.py
    ├── market_opportunity.py
    ├── pricing.py
    ├── activation.py
    ├── scenarios.py
    ├── dashboard_export.py
    └── run_pipeline.py
