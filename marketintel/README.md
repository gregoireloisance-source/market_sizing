# MarketIntel: PE Market Sizing Plugin for Claude Code

Professional-grade market sizing for private equity due diligence. Dual approach (top-down + bottom-up), every figure sourced, Excel output.

## Features

✅ **Web-researched datapoints** – StatisticalOffice → Regulator → Research → Press hierarchy
✅ **Dual-method TAM** – Top-down (macro × filters) + bottom-up (units × ARPU × penetration)
✅ **Triangulation & reconciliation** – Gap analysis, football-field ranges
✅ **Competitive analysis** – Player profiles, market share, consolidation
✅ **Red-team challenge** – Assumption testing, risk identification, management questions
✅ **Professional Excel** – 8 sheets, live formulas, consulting-style formatting
✅ **Full source traceability** – Every number links to URL + quote

## Installation

Clone the repository and add as a Claude Code plugin:

```bash
# In Claude Code
/plugin marketplace add /path/to/marketintel
```

Or manually:
```bash
git clone <repo> /path/to/marketintel
pip install -r marketintel/requirements.txt
```

## Quick Start

```
/market-sizing "Logistics SaaS" France
```

The agent will:
1. Confirm market definition
2. Run parallel research (datapoints, competitors)
3. Build top-down and bottom-up models
4. Triangulate and reconcile
5. Challenge with red team
6. Generate Excel report

Output: `Market_Sizing_Logistics_SaaS_France_20241018.xlsx`

## Usage Examples

### Qualification (Junior)
```
/market-sizing "Digital Health" France --depth=quick
```
→ 10 min, basic TAM only, answers "is the market interesting?"

### Deep Dive (Partner)
```
/market-sizing "B2B Payments" France --company=Stripe --competitors=Payplug,Ingenico
```
→ 30 min, full analysis with competitor positioning and red team

### With specific parameters
```
/market-sizing "HR Tech" Europe --depth=deep --competitors=ADP,Paychex,Personio
```

## What's Inside

```
marketintel/
├── .claude-plugin/plugin.json      # Plugin registration
├── agents/
│   ├── market-researcher.md        # Web search for datapoints
│   ├── sizing-analyst.md           # Build TAM/SAM/SOM
│   ├── competitive-analyst.md      # Competitive landscape
│   └── red-team.md                 # Challenge assumptions
├── commands/
│   └── market-sizing.md            # Command definition & workflow
├── skills/
│   └── market-sizing-method/SKILL.md  # MECE framework, best practices
├── scripts/
│   ├── schema.py                   # Data structures (DataPoint, Assumption, Market)
│   ├── validate.py                 # Gate-keeper: no orphan numbers
│   └── build_excel.py              # Excel report generator (openpyxl)
├── requirements.txt
└── README.md (this file)
```

## Excel Output Structure

### Sheet 1: Executive Summary
- Market size (TAM range)
- Attractiveness score (1-10)
- Key drivers & risks
- Investment verdict

### Sheet 2: Top-Down Analysis
- Macro pool and filters with sources
- TAM/SAM/SOM calculation
- Documentation of every step

### Sheet 3: Bottom-Up Analysis
- Addressable units, ARPU, penetration
- Unit economics
- TAM/SAM/SOM with independent inputs

### Sheet 4: Triangulation
- Side-by-side comparison
- Gap analysis & explanation
- Football-field (low/high) range

### Sheet 5: Scenarios & Sensitivity
- Bull/base/bear cases
- 5-year projections (CAGR)
- Tornado chart (which assumptions matter most)

### Sheet 6: Competitive Landscape
- Top 5 competitors (revenue, growth, market share)
- Market structure (HHI index)
- Consolidation activity

### Sheet 7: Inputs & Sources
- **Every datapoint**: value, unit, year, URL, exact quote, confidence, retrieval date
- **Every assumption**: value, low/high range, rationale
- Color-coded: GREEN = sourced, YELLOW = assumption

### Sheet 8: Red Flags & Questions
- Key risks (likelihood: HIGH/MED/LOW)
- Management questions to ask
- Gaps in research

## Source Confidence Levels

| Level | Color | Examples |
|-------|-------|----------|
| HIGH | Green | INSEE, Eurostat, SEC 10-K, company investor relations |
| MEDIUM | Yellow | Gartner reports, industry bodies, published research |
| LOW | Orange | News, analyst abstracts, LinkedIn estimates, rumors |

**Rule**: If most datapoints are MEDIUM/LOW, overall model confidence is lower. Excel will flag this.

## Validation Rules

Before Excel generation, the validator checks:

✅ No orphan numbers (every input is sourced or flagged ASSUMPTION)
✅ TAM > SAM > SOM (strictly decreasing)
✅ Gap between top-down and bottom-up is explained
✅ Assumptions have low/high ranges
✅ Attractiveness score is 1-10 with rubric
✅ At least 3 key risks identified
✅ At least 5 management questions

If validation fails, you get a clear error message with what to fix.

## Assumptions vs. Datapoints

**Datapoint**: A sourced fact
```
"France PME count (10-249 employees) = 127,000"
Source: INSEE (HIGH confidence)
```

**Assumption**: An estimate when source not available, with range
```
"Avg employees per company = 50 (range: 30-80)"
Rationale: Industry benchmark; will validate with target's customer mix
```

Assumptions are colored YELLOW in Excel; nothing is hidden.

## Management Questions (Red Team)

The agent auto-generates questions like:
- "How does your TAM vs. the market leader's stated addressable market align?"
- "What is your realistic Year 1 market penetration vs. comparable SaaS companies?"
- "How will you defend against bundling by Microsoft/Paychex/Amazon?"
- "What is your target ARPU vs. the industry average?"

These are the conversations to have during management interviews.

## Limitations

- **Paywalled sources** (Gartner full reports, Statista, PitchBook): Only abstracts available → MEDIUM/LOW confidence
- **Private companies**: Revenue estimated from LinkedIn/Crunchbase → MEDIUM/LOW confidence
- **Niche markets**: Fewer public sources → more ASSUMPTIONS
- **Fast-moving sectors**: Data may be 6+ months old

## Next Steps After Analysis

1. **Review Excel** (15 min)
   - Does TAM range feel right?
   - Are assumptions reasonable?
   - Any data that surprises you?

2. **Validate with diligence team** (30 min)
   - Share with lawyers, financials team
   - Stress-test key assumptions

3. **Management interview** (1-2 hours)
   - Work through red-team management questions
   - Validate ARPU, CAC, churn, competitive positioning
   - Understand their moat

4. **Investment decision**
   - Market is attractive + team is strong → Proceed to detailed DD
   - Market is questionable → Better to know now
   - Market is small or consolidating → Consider if it's even worth your time

## Development

### Adding a new agent
1. Create a new `.md` file in `agents/`
2. Define Input, Methodology, Output format
3. Update the orchestration in commands/market-sizing.md

### Adding validation rules
1. Edit `scripts/validate.py`
2. Add a check function and call it from `validate_market()`

### Customizing Excel style
1. Edit `scripts/build_excel.py` — modify `header_fill`, `assumption_fill`, etc.
2. Regenerate a test file

## Performance Notes

- **Quick analysis** (~10 min): TAM only, 2 competitors, no red team
- **Deep analysis** (~30 min): Full TAM/SAM/SOM, 5 competitors, red team challenge, management questions

Time scales with market research complexity (narrow vs. broad sector).

## Support

- **Questions about the framework?** → Read `skills/market-sizing-method/SKILL.md`
- **How does a specific agent work?** → Read `agents/<agent>.md`
- **Excel won't generate?** → Check `scripts/validate.py` errors
- **Datapoints seem wrong?** → Edit `agents/market-researcher.md` search strategy

## License & Attribution

MarketIntel is designed for private equity due diligence. Use freely; adapt as needed.

---

**Version**: 1.0.0
**Last Updated**: October 2024
