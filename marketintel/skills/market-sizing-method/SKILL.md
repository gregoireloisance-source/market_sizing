# Skill: Market Sizing Methodology

Framework for PE-grade market sizing: MECE-driven, source-first, dual-approach (top-down + bottom-up).

## Principles

1. **MECE (Mutually Exclusive, Collectively Exhaustive)**
   - Break market into non-overlapping segments
   - Ensure no company is counted twice
   - Cover the entire addressable market

   Example: SaaS HRIS market
   ```
   By company size: 10-50, 50-250, 250+
   By geography: France, Rest of Europe, Rest of world
   By adoption: Early adopters (already SaaS), mainstream (considering), laggards (on-premise)
   ```

2. **Source-First**
   - Every number must be traceable to a URL
   - Hierarchy: Statistics office > Regulator > Industry body > Research > Press
   - If source is paywalled, flag confidence as MEDIUM/LOW
   - If no source exists, use ASSUMPTION with range (low/high)

3. **Dual Approach (Redundancy)**
   - Top-down: Macro market × realistic filters
   - Bottom-up: Unit count × ARPU × penetration
   - Both should converge; if not, explain why
   - Goal: Not a single point estimate, but a range (football field)

4. **Confidence as Signal**
   - Every datapoint has confidence: HIGH / MEDIUM / LOW
   - HIGH = statistical office, regulator, public company filing
   - MEDIUM = published industry research, press with specifics
   - LOW = news, analyst abstract, private company estimate
   - Average confidence of model = overall credibility

## Tactical: MECE Driver Tree

Start with a driver tree to organize research:

```
SaaS HRIS Market Size
├─ Demand drivers
│  ├─ Total addressable companies (by size, region, industry)
│  ├─ % already using SaaS vs on-premise
│  ├─ % willing to switch
│  └─ Purchasing power (revenue per company, IT budget)
├─ Supply drivers
│  ├─ Incumbent players (Paychex, BambooHR, local)
│  ├─ New entrants (VC-funded, tech giants bundling)
│  └─ Consolidation activity (M&A prices, trends)
├─ Pricing drivers
│  ├─ ARPU (€ per employee per month)
│  ├─ Discounting by volume / segment
│  └─ Price elasticity (price wars?)
└─ Adoption drivers
   ├─ Regulatory (e.g., EU digital mandate)
   ├─ Economic (cost savings, efficiency)
   ├─ Technology (cloud maturity, APIs)
   └─ Competition (pressure from peers)
```

For each driver, search for data. This ensures you don't miss a major variable.

## Tactical: TAM Calculation

### Top-Down: Macro × Filters

Start with a macro pool (total companies, total revenue, total employees) and apply realistic filters.

**Formula:**
```
TAM = Macro pool × Filter 1 × Filter 2 × Filter 3 × ... × Spend ratio
```

**Example: SaaS HRIS, France**
```
TAM = (France companies with 10+ employees)
    × (% in industries that buy HRIS)
    × (% with revenue >€500k)
    × (IT spend as % of revenue)
    × (% of IT budget to HR/Paie)
    = 127,000 × 0.85 × 0.70 × 0.04 × 0.10
    = €30.3M TAM

Wait, that's too small. Try different cut:

TAM = (France companies)
    × (% with 10+ employees)
    × (Average revenue)
    × (IT spend %)
    × (HR/Paie %)
    = Different inputs, same logic
```

**Key rules:**
- Filters should be independent (don't double-count)
- Use published statistics for the base (INSEE, Eurostat, not guesses)
- Apply realistic filters (company size, revenue, adoption stage)
- Document every multiplication with source

### Bottom-Up: Units × ARPU × Penetration

Define the unit (company, employee, transaction) and build from there.

**Formula:**
```
TAM = Addressable units × ARPU (annual) × Realistic penetration rate
```

**Example: SaaS HRIS, France**
```
Units = Companies with 10-250 employees = 127,000
ARPU = €300/employee/year (industry benchmark)
Avg employees per company = 75
Penetration = 5% realistic market capture

TAM = 127,000 × 75 × €300 × 0.05 = €142.9M

Hmm, higher than top-down. Why?
- Top-down filtered more aggressively (revenue >€500k)
- Bottom-up assumes all companies in range are addressable
- Reconcile by understanding which assumption is weaker
```

**Key rules:**
- Unit count should be verifiable (not a guess)
- ARPU should benchmark against known competitors
- Penetration should be realistic (2-10% for a challenger is typical)
- Show the calculation step-by-step

## Tactical: SAM and SOM

**TAM** = Total addressable market (all possible buyers, if we had infinite resources)

**SAM** = Serviceable addressable market (realistic segment we target, given GTM constraint)
- Example: Maybe we focus on 50-250 employee companies (ignore 10-50, ignore 250+)
- SAM = TAM × (% of companies in our segment) = 40-60% of TAM typically

**SOM** = Serviceable obtainable market (realistic market capture in Year 1)
- Example: If market is mature with incumbents, 2-5% is ambitious
- If market is fragmented, 5-15% is possible
- SOM = SAM × (realistic penetration rate, 2-10% typically) = 1-5% of TAM

**Sanity check:**
```
TAM = €200M (all France companies)
SAM = €80M (our target segment: 50-250 employees)
SOM = €4M (2% of SAM is our realistic Year 1 capture)
```

This is realistic for a VC-backed challenger.

## Tactical: Triangulation

When top-down ≠ bottom-up, **explain the gap, don't hide it.**

**Gap calculation:**
```
Gap % = |TopDown_TAM - BottomUp_TAM| / TopDown_TAM

Example:
TopDown = €150M
BottomUp = €200M
Gap = |150-200|/150 = 33% (material!)
```

**When gap is <20%**: Approaches agree, use average or weighted average. Confidence is HIGH.

**When gap is 20-100%**: Diagnose
```
Possible reasons:
✓ Different addressable pool (one filters more aggressively)
✓ Different ARPU assumption (one overestimates pricing)
✓ Different penetration (one is optimistic, one conservative)
✓ Timing (one uses old data, market moved)
```

Example diagnosis:
```
TopDown = €150M (assumes 50% of companies have revenue >€500k)
BottomUp = €200M (assumes all 10-250 employee companies are addressable)

Gap explanation: TopDown is more conservative on addressability.
BottomUp likely overestimates; many small companies may not have budget for SaaS HRIS.

Recommendation: Use TopDown as base, with upside if adoption accelerates.
Football field: €150M (base) to €200M (upside if market shifts).
```

**When gap is >100%**: Something is wrong. Recheck inputs.

## Tactical: Competitive Analysis

Assess whether the market is fragmented or consolidated.

**HHI (Herfindahl-Hirschman Index):**
```
HHI = Sum of (market_share %)²

Interpretation:
< 1500 = Fragmented (many players)
1500-2500 = Moderate concentration
> 2500 = Highly consolidated (1-2 players dominate)

Example:
Paychex 18%, BambooHR 11%, Personio 8%, Others (40+) = 63%
HHI = 18² + 11² + 8² + 63² = 324 + 121 + 64 + 3969 = 4478 → Consolidated
```

**Consolidation activity:**
- Track M&A in last 2 years
- Are incumbents acquiring competitors (defensive)?
- Are roll-ups happening (consolidator buying 3-5 small players)?
- Implication: Hard for challengers to win if top player is aggressive on M&A

**Competitive positioning:**
- Who has the best tech? (Personio = modern UX, Paychex = legacy but integrated)
- Who is winning? (Look at growth rates)
- Who is vulnerable? (Legacy player, slow, high churn?)
- Where is the white space? (Niche market, segment, geography?)

## Tactical: Risk & Sensitivity

For assumptions, test low/high scenarios.

**Example: Assumption = "Avg company size 75 employees (range 50-100)"**
```
Base case: TAM = €150M
Low case (50 emp): TAM = €100M (-33%)
High case (100 emp): TAM = €200M (+33%)
```

**Tornado chart**: Rank assumptions by impact
```
Which assumption has the biggest effect on TAM?
1. % of companies already SaaS (biggest range, biggest TAM swing)
2. ARPU (middle range, middle swing)
3. Penetration rate (smallest range, smallest swing)
→ Focus due diligence on #1: Is SaaS adoption really 45% or is it 30%?
```

## Validation Checklist

Before Excel generation:

- [ ] Every number is sourced or flagged ASSUMPTION
- [ ] TAM < SAM < SOM (strictly decreasing)
- [ ] Gap between top-down and bottom-up is <100% AND explained
- [ ] Competitive landscape makes sense (HHI aligns with market maturity)
- [ ] ARPU checks against known competitors
- [ ] Penetration rate is realistic (<10% for mature market, <5% for us as challenger)
- [ ] 5-year growth projections are CAGR 10-25% (anything outside is red flag)
- [ ] At least 3 management questions are sharp (not obvious)

---

## Further reading (if you want to go deeper)

- **Benchmark public comps**: Use Paychex 10-K filing as a source of truth for SaaS HRIS benchmarks
- **Regulatory drivers**: Check if upcoming law (e.g., EU carbon tracking) would force SMBs to adopt software
- **Technology adoption curves**: S-curve model predicts market growth (early adopters → mainstream → laggards)
- **Valuation sanity check**: Market size × gross margin × growth rate = should justify valuation multiples
