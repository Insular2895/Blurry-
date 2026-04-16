# KPI Definition — Blurry Weekly Drop Intelligence

## Purpose

This dashboard supports weekly decision-making for Blurry’s cross-border stock activation model.

Blurry does not move stock continuously across boutiques.  
Stock is only moved when a weekly drop activation is validated by the decision engine.

The dashboard is designed to answer four business questions:

1. Which stocks are truly at risk locally?
2. Which international markets are attractive enough to justify activation?
3. Which product-flow combinations remain profitable after full landed cost?
4. Which approved activations stay resilient under stress scenarios?

---

## KPI Groups

## 1. Stock KPIs

### Slow-Moving Products
Number of SKU-location combinations flagged as slow-moving.

**Formula**  
Count of rows where `slow_moving_flag_v2 = 1`

### Eligible for Weekly Drop
Number of SKU-location combinations eligible for international activation.

**Formula**  
Count of rows where `eligible_for_drop_flag_v2 = 1`

### Average Stock Risk Score
Average stock risk level across the portfolio.

**Formula**  
Average of `stock_risk_score_v2`

---

## 2. Market KPIs

### Average Market Opportunity Score
Average attractiveness of tested target markets.

**Formula**  
Average of `market_opportunity_score_v2`

### High-Priority Markets
Number of product-market combinations classified as high priority.

**Formula**  
Count of rows where `market_tier = high_priority`

### Top Market by Opportunity
Highest scoring target country based on market opportunity.

**Formula**  
Country with highest mean `market_opportunity_score_v2`

---

## 3. Pricing KPIs

### Average Landed Cost
Average full landed cost across tested flows.

**Formula**  
Average of `landed_cost_v2`

### Average Recommended Price
Average target selling price needed to preserve target margin.

**Formula**  
Average of `recommended_price_v2`

### Market-Supported Flows
Number of tested flows where market price supports the recommended price.

**Formula**  
Count of rows where `pricing_status = market_supports_price`

### Price Gap vs Market
Difference between observed market price and recommended price.

**Formula**  
`avg_market_price - recommended_price_v2`

---

## 4. Activation KPIs

### Approved Activations
Number of weekly drops approved by the engine.

**Formula**  
Count of rows where `activation_decision = approve`

### Rejected Activations
Number of weekly drops rejected by the engine.

**Formula**  
Count of rows where `activation_decision = reject`

### Average Activation Score
Average combined decision score across tested weekly drops.

**Formula**  
Average of `activation_score_v2`

### Top Approved Flow
Highest-ranked approved SKU / source / target combination.

**Formula**  
Approved row with highest `activation_score_v2`

---

## 5. Scenario KPIs

### Total Profit by Scenario
Total simulated profit of approved activations under each scenario.

**Formula**  
Sum of `profit_scn` by `scenario_name`

### Profitable Activations Under Stress
Number of approved activations that remain profitable in each scenario.

**Formula**  
Count where `scenario_status = profitable`

### Average Unit Margin Under Stress
Average unit margin under each scenario.

**Formula**  
Average of `unit_margin_scn` by `scenario_name`

### Worst-Case Profit
Total profit under the `combined_worst` scenario.

**Formula**  
Sum of `profit_scn` where `scenario_name = combined_worst`

---

## Suggested Dashboard Pages

## Page 1 — Executive Overview
- Approved activations
- Rejected activations
- Eligible stock count
- Market-supported flows
- Total base profit
- Worst-case profit

## Page 2 — Stock Risk
- Stock risk by location
- Slow-moving products
- Weekly drop eligibility
- Top dormant stocks

## Page 3 — Market Opportunity
- Opportunity score by country
- Top product-market combinations
- Demand vs volatility comparison

## Page 4 — Pricing
- Landed cost vs market price
- Recommended price vs observed market price
- Flows above market threshold

## Page 5 — Scenario Stress Test
- Profit by scenario
- Margin erosion by scenario
- Most resilient approved activations