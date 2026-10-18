# Command: /market-sizing

Comprehensive market sizing for PE due diligence. Dual approach (top-down + bottom-up), all sourced, Excel output.

## Usage

```
/market-sizing <sector> <geography> [options]

Options:
  --company=NAME        Specific company to compare (adds competitive analysis)
  --depth=quick|deep    Default: deep (full analysis)
  --competitors=LIST    Specific competitors to analyze (comma-separated)
```

## Examples

```
/market-sizing "Logistics SaaS" France
/market-sizing "Digital Health" Europe --depth=quick
/market-sizing "B2B Payments" France --company=Stripe --competitors=Payplug,Ingenico
```

## Workflow

1. **Market Scoping** (30 sec)
   - Confirm market definition (in/out boundaries)
   - Identify key drivers (MECE tree)
   - List known competitors

2. **Market Research** (Parallel, 5-10 min)
   - Web search for datapoints (INSEE, Gartner, press, etc.)
   - Find company financials and growth rates
   - Return: sourced datapoints, confidence scores, gaps

3. **Sizing Analysis** (3-5 min)
   - Build top-down model (macro × filters)
   - Build bottom-up model (units × ARPU × penetration)
   - Triangulate gap
   - Return: TAM/SAM/SOM with formulas, football field range

4. **Competitive Landscape** (2-3 min)
   - Profile top 5 competitors
   - Calculate market share
   - Assess consolidation, M&A activity
   - Return: competitor table, market structure (HHI)

5. **Red Team Challenge** (3-5 min)
   - Test assumptions (low/high sensitivity)
   - Challenge competitive positioning
   - Identify weak points
   - Generate management questions

6. **Excel Generation** (1 min)
   - Validate all data
   - Build 8-sheet professional workbook
   - Save locally

## Output

Single Excel file with:
- **Executive Summary** (for partners, 5 min read)
- **Top-Down Analysis** (drivers + TAM/SAM/SOM)
- **Bottom-Up Analysis** (unit econ + penetration)
- **Triangulation** (gap analysis + football field)
- **Scenarios** (bull/base/bear + sensitivity)
- **Competitive Landscape** (player profiles + market structure)
- **Inputs & Sources** (every datapoint with URL and quote)
- **Red Flags & Questions** (risks + management questions)

## What gets sourced

✅ **All datapoints** must have a URL and quote
- Statistical fact: INSEE/Eurostat/etc.
- Industry benchmark: Gartner, IDC, trade association
- Company data: LinkedIn, filings, press release

✅ **Assumptions** (when data unavailable) must be flagged and include range
- "ASSUMPTION: Avg company size 50 employees (range 30-80)"
- Colored yellow in Excel, with rationale

❌ **No orphan numbers** are allowed
- Every input to the model traces to a source or flagged assumption

## Confidence levels

- **HIGH** (green): Statistical office, regulator, company filing
- **MEDIUM** (yellow): Industry body, published research
- **LOW** (orange): News, analyst abstract, hearsay

## Example output

```
MARKET ASSESSMENT: Logistics SaaS - France

Market Size:      €450M - €750M TAM
Attractiveness:   7/10 ✓
Growth:           14% CAGR

Competitors:      Paychex (18%), BambooHR (11%), 3 French regional

Risks:            Amazon/Azure entry, regulatory uncertainty, consolidation

Management Qs:    "How will you differentiate vs. Paychex?"
                  "What's your TAM vs. their claimed addressable market?"
                  "How much market is locked into incumbent payroll?"

File:             Market_Sizing_Logistics_France_20241018.xlsx
```

## Typical timeline

- **Quick** (--depth=quick): 10-15 min (TAM only, fewer competitors, no red team)
- **Deep** (default): 20-30 min (full TAM/SAM/SOM, 5 competitors, red team challenge)

## Limitations

- **Paywalled sources** (Gartner, Statista, PitchBook): Abstracts only, flagged MEDIUM/LOW confidence
- **Private companies**: Revenue estimated from LinkedIn/Crunchbase (MEDIUM/LOW confidence)
- **Niche markets**: Fewer public sources, more assumptions
- **Rapid-change sectors** (AI, crypto): Data may be 6+ months old

## What you should do after

1. **Review Excel** (15 min)
   - Check if assumptions match your knowledge of market
   - Identify which data points seem off
   - List gaps for management questions

2. **Challenge findings** (30 min)
   - Share with diligence team; gather feedback
   - Test assumptions ("Is 50 avg employees realistic for this segment?")
   - Add your own market knowledge

3. **Management questions** (60+ min with mgmt)
   - Work through the red-team questions
   - Validate ARPU, CAC, churn assumptions
   - Understand their competitive positioning
   - Stress-test for risks (regulatory, consolidation, technology)

4. **Decision**
   - Market is attractive? → Deep diligence on execution
   - Market is questionable? → Better to know now than after close
   - Market is small? → Consider if it's a niche play or consolidation target

---

**Questions?** Review the Excel "Red Flags & Questions" sheet; these are the points that matter most.
