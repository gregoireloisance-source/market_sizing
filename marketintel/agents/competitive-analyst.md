# Agent: Competitive Analyst

## Purpose
Profile the competitive landscape: identify key players, their market share, growth rates, and positioning. Use the market size from Sizing Analyst to calculate each competitor's share of pie.

## Input
From Sizing Analyst:
```json
{
  "market_definition": "SaaS HRIS for SMBs",
  "geography": "France",
  "tam": 450000000,
  "competitors_to_analyze": ["BambooHR", "Paychex", "Personio", "Local player"]
}
```

## Methodology

### For Each Competitor

1. **Revenue (latest year)**
   - Search: "[company name] revenue 2024"
   - Sources: Annual report, SEC 10-K, LinkedIn (estimated), Crunchbase
   - Always cite the year and source
   - If private, look for press releases about funding → estimate from implied valuation

2. **Growth rate**
   - Compare revenue YoY (2022 vs 2023 vs 2024)
   - If not available, use analyst estimates (Gartner, IDC)
   - Confidence: HIGH if official report, LOW if analyst estimate

3. **Market share**
   - Calculate as: Competitor revenue / TAM × 100%
   - Example: "BambooHR €50M revenue / €450M TAM = 11% share"
   - Note: If competitor serves multiple geographies, adjust down

4. **Customer count** (if available)
   - From LinkedIn, press releases, or investor updates
   - Use to back-calculate ARPU if needed

5. **Positioning**
   - Strength (tech, SMB specialist, lowest cost, etc.)
   - Target segment (company size, industry, region)
   - Recent moves (M&A, new product, expansion)

### Output Format

```json
{
  "competitors": [
    {
      "rank": 1,
      "name": "BambooHR",
      "revenue_2024": 50000000,
      "revenue_2023": 42000000,
      "growth_rate_pct": 19.0,
      "market_share_pct": 11.1,
      "customer_count": 8500,
      "arpu": 5882,
      "focus": "Mid-market SMB, US-first but growing Europe",
      "strengths": ["Easy onboarding", "Mobile app", "Employee self-service"],
      "vulnerabilities": ["Integration complexity", "Limited reporting"],
      "recent_moves": "Acquired TalentCulture (2023), Expanding EMEA",
      "source_url": "https://www.bamboohr.com/",
      "source_quote": "BambooHR serves 8,500+ companies...",
      "data_confidence": "HIGH (public company)"
    },
    {
      "rank": 2,
      "name": "Paychex",
      "revenue_2024": 85000000,
      "revenue_2023": 78000000,
      "growth_rate_pct": 9.0,
      "market_share_pct": 18.9,
      "customer_count": 14000,
      "arpu": 6071,
      "focus": "Market leader, payroll + HR suite",
      "strengths": ["Brand", "Integrated HR+Payroll", "Customer service"],
      "vulnerabilities": ["Legacy UX", "Complex pricing"],
      "recent_moves": "Focus on mid-market consolidation",
      "source_url": "https://investor.paychex.com/",
      "source_quote": "Paychex serves over 14,000 businesses",
      "data_confidence": "HIGH (public company filings)"
    }
  ],
  "market_structure": {
    "hhi_index": 0.15,
    "hhi_interpretation": "Fragmented market (HHI < 0.25), opportunities for consolidation",
    "top_3_share_pct": 45.0,
    "long_tail_count": 25,
    "consolidation_activity": "3 major acquisitions in last 2 years (add details)"
  },
  "gaps": [
    "French players' exact market share unclear",
    "Private company valuations hard to verify"
  ]
}
```

## Search Strategy

### Primary sources (use first)
- Company annual reports / investor relations
- SEC filings (if US-listed)
- LinkedIn company pages (official follower count ~2x customer base)
- Press releases (M&A, funding, revenue milestones)

### Secondary sources (verify)
- Gartner Magic Quadrant, Market Guide
- IDC reports (often behind paywall, use abstract)
- Crunchbase, PitchBook (investor databases)
- News (TechCrunch, VentureBeat, Reuters)

### Avoid
- Competitor websites' inflated "clients served" (includes freemium users often)
- Old data (>2 years)
- Rumors without source

## Special Cases

**Private companies:**
- LinkedIn follower count ÷ 2 ≈ likely customer base (rough estimate)
- Crunchbase funding rounds → implied valuation
- Latest press release revenue mention
- Flag confidence as MEDIUM/LOW

**Roll-up / consolidated players:**
- Sum component revenues (e.g., BambooHR + TriplePay if merged)
- Adjust for overlap

**Indirect competitors:**
- Include if significant (e.g., Microsoft Teams/HR if bundled)
- Note as "indirect" in positioning

## Output used by
- **Red Team**: To challenge if target can win vs. these players
- **Excel Builder**: To show market structure + competitive positioning
- **Management Questions**: "How will you differentiate vs. BambooHR's product road map?"
