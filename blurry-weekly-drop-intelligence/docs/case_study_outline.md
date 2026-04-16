# Case Study Outline — Blurry Weekly Drop Intelligence

## 1. Context

Blurry works with multiple boutiques and partner stock points to prevent inventory from remaining unsold in low-demand catchment areas.

The company does not move inventory continuously.  
To limit operational risk, stock only moves when a weekly cross-border activation is validated.

This creates a controlled model where logistics are triggered only when demand, pricing and margin conditions justify the move.

---

## 2. Business Problem

A product can underperform locally while still being attractive in another market.

The challenge is not only to detect demand, but to determine:

- which markets are truly attractive,
- which dormant stocks should be activated,
- whether the target market can support the required selling price,
- and whether the move remains profitable after shipping, customs and FX risk.

---

## 3. Project Objective

Build a decision-support engine able to recommend:

- which SKU-location combinations should be activated,
- which target countries should be prioritized,
- what recommended selling price should be used,
- and which approved activations remain resilient under stress.

---

## 4. Scope

### Included
- 5 SKUs
- 5 stock locations / boutiques
- 5 target markets
- synthetic demand and pricing data
- stock risk scoring
- market opportunity scoring
- landed cost and pricing logic
- weekly activation decision engine
- scenario analysis
- dashboard-ready exports

### Excluded
- live marketplace API integration
- real-time warehouse execution
- complex optimization engine
- full marketplace operations layer

---

## 5. Data Model

### Dimensions
- DimSKU
- DimLocation
- DimMarket

### Facts
- FactStockHealth
- FactMarketOpportunity
- FactWeeklyActivation
- FactScenario

---

## 6. Analytical Logic

### Stock Health
Objective: identify dormant local stock worth activating.

Main signals:
- days in stock
- sell-through rate
- stock volume

Output:
- stock risk score
- slow-moving flag
- weekly drop eligibility flag

### Market Opportunity
Objective: identify the most attractive target markets.

Main signals:
- average market price
- demand score
- trend score
- volatility score

Output:
- market opportunity score
- market tier

### Pricing
Objective: determine whether a target market can support the required margin.

Main components:
- buy price
- shipping
- customs
- packaging
- quality control
- FX buffer

Output:
- landed cost
- recommended price
- price gap vs market
- pricing status

### Activation Engine
Objective: approve only robust weekly drops.

Validation logic:
- stock must be eligible
- market must be attractive enough
- market must support the price

Output:
- activation score
- approval / rejection
- reason for decision

### Scenario Analysis
Objective: stress-test approved activations.

Scenarios:
- base
- FX stress
- shipping stress
- demand stress
- combined worst

Output:
- profit by scenario
- unit margin by scenario
- resilience of approved flows

---

## 7. Key Results

### Portfolio Output
- 25 stock rows analysed
- 25 product-market rows analysed
- 10 weekly flows tested
- 3 approved activations
- 7 rejected activations

### Main Findings
- only a limited share of dormant stock should be activated
- Canada shows strong demand but not all flows remain viable after full cost
- BX appears as a cleaner market on several tested flows
- approved activations remain profitable even under combined stress

---

## 8. Business Interpretation

The model supports Blurry’s operating logic:

- avoid unnecessary stock movement,
- activate only during controlled weekly drops,
- protect margin before volume,
- use data to justify cross-border stock rotation.

This is aligned with a risk-controlled operating model rather than a continuous redistribution system.

---

## 9. Deliverables

- clean synthetic dataset
- Python analytical scripts
- curated data marts
- dashboard-ready exports
- case study
- executive narrative

---

## 10. Recruiter Takeaway

This project demonstrates the ability to:

- structure a business decision engine,
- connect pricing, margin and international logistics,
- model cross-border stock allocation logic,
- build decision outputs instead of only descriptive dashboards,
- present the result with a senior business analytics framing.