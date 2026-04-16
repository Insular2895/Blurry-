
---

# 3. `assumptions.md`

```md id="qwgc6y"
# Assumptions

## Business model assumptions

- Blurry works with partner boutiques holding local inventory.
- Inventory stays in the original boutique by default.
- Blurry does **not** perform permanent inter-boutique stock transfers.
- A product only moves when it is selected in a **weekly drop / raffle** activation.
- The objective is to reduce slow-moving inventory while preserving a credible net margin.

## Project assumptions

- This project is a **realistic simulation**, not a live operating system.
- Market demand, target market opportunity and weekly activations are partly synthetic.
- Costs such as shipping, customs, packaging, QC and FX buffer are estimated.
- Data is intentionally simplified to keep the portfolio project readable and decision-oriented.

## Stock assumptions

- Slow-moving inventory is identified using simplified metrics such as:
  - days in stock
  - sell-through rate
  - local demand score
- Eligibility for weekly activation is based on a simplified stock risk score.

## Market assumptions

- Market opportunity is estimated using simplified indicators such as:
  - average market price
  - demand score
  - trend score
  - volatility score
- Target markets are grouped at country or regional level for clarity.

## Pricing assumptions

- Landed cost is estimated using:

```text
landed_cost = buy_price + shipping_cost + customs_cost + packaging_cost + qc_cost + fx_buffer