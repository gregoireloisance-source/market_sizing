"""
Data structures for market sizing: datapoints, assumptions, models.
Validation ensures no orphan numbers and every value is traceable.
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict, Any, List
from datetime import date
from enum import Enum
import json


class Confidence(str, Enum):
    """Source confidence level"""
    HIGH = "HIGH"      # Statistical office, regulator, company filing
    MEDIUM = "MEDIUM"  # Industry body, published research
    LOW = "LOW"        # News, analyst call, abstract only


class SourceType(str, Enum):
    """Hierarchy for source preference"""
    STATISTICAL_OFFICE = 1  # INSEE, Eurostat, ONS, etc.
    REGULATOR = 2          # Company House, SEC, etc.
    COMPANY_FILING = 3     # 10-K, annual report
    INDUSTRY_BODY = 4      # Trade association
    RESEARCH = 5           # Gartner, IDC, etc.
    PRESS = 6              # News, blog


@dataclass
class DataPoint:
    """A single fact with source (not an assumption, not a calculation)"""
    name: str                      # "France PME count", "SaaS adoption rate"
    value: float                   # The number
    unit: str                      # "%", "count", "EUR", etc.
    year: int                      # 2024
    source_url: str                # Exact link
    source_quote: str              # Exact excerpt from source
    source_type: SourceType        # For ranking
    confidence: Confidence         # HIGH/MEDIUM/LOW based on source
    retrieval_date: date           # When we fetched it

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "year": self.year,
            "source_url": self.source_url,
            "source_quote": self.source_quote,
            "source_type": self.source_type.name,
            "confidence": self.confidence.value,
            "retrieval_date": self.retrieval_date.isoformat(),
        }

    @staticmethod
    def validate_required(dp: 'DataPoint') -> bool:
        """A datapoint must have all fields populated"""
        return all([
            dp.name, dp.value is not None, dp.unit, dp.year,
            dp.source_url.startswith(('http://', 'https://')),
            dp.source_quote, dp.confidence
        ])


@dataclass
class Assumption:
    """A value we assume because a source is not available (yet).
    Marked visually in Excel; must include low/high range for sensitivity.
    """
    name: str                      # "Avg employees per company"
    value: float                   # Best estimate
    unit: str                      # "count", "%", etc.
    low: float                     # Pessimistic
    high: float                    # Optimistic
    rationale: str                 # Why this assumption, what would prove it wrong
    year: int                      # Assumption year

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "low": self.low,
            "high": self.high,
            "rationale": self.rationale,
            "year": self.year,
        }

    @staticmethod
    def validate_required(a: 'Assumption') -> bool:
        """Assumption must be complete: no orphan values"""
        return all([
            a.name, a.value is not None, a.unit, a.low, a.high,
            a.rationale, a.year,
            a.low <= a.value <= a.high  # Value within range
        ])


@dataclass
class TopDownModel:
    """Top-down TAM: macro pool × filters"""
    market_definition: str         # "SaaS HRIS for SMB"
    geography: str                 # "France"

    # Inputs (each referencing a DataPoint or Assumption)
    total_target_companies: float  # Count or derived value
    avg_revenue_per_company: float
    it_spend_pct_revenue: float
    hr_software_pct_it: float
    addressable_pct: float         # Which % of companies are we targeting?

    # Outputs (calculated, stored for traceability)
    tam: float                     # Total Addressable Market
    sam: float                     # Serviceable Addressable Market
    som: float                     # Serviceable Obtainable Market

    # Metadata
    datapoints_used: List[str] = field(default_factory=list)  # Names of DataPoints
    assumptions_used: List[str] = field(default_factory=list)  # Names of Assumptions


@dataclass
class BottomUpModel:
    """Bottom-up market: units × price × penetration"""
    market_definition: str
    geography: str

    # Inputs
    target_segment_size: float     # Number of addressable units (companies, users, etc.)
    avg_arpu_annual: float         # Annual revenue per unit (€)
    market_penetration_pct: float  # % of segment we can realistically capture

    # Outputs
    tam: float
    sam: float
    som: float

    # Metadata
    datapoints_used: List[str] = field(default_factory=list)
    assumptions_used: List[str] = field(default_factory=list)


@dataclass
class TriangulationResult:
    """Comparison of top-down and bottom-up"""
    topdown_som: float
    bottomup_som: float
    gap_pct: float                 # |topdown - bottomup| / topdown
    explanation: str               # Why the gap (different addressable, different prices, etc.)
    recommendation: str            # Which one to trust more and why
    football_field_low: float      # Low estimate (bear case)
    football_field_high: float     # High estimate (bull case)


@dataclass
class CompetitorAnalysis:
    """Single competitor profile"""
    name: str
    revenue_latest_year: float
    revenue_year: int
    market_share_pct: Optional[float]  # If market size is known
    growth_rate_pct: float             # YoY %
    focus: str                         # Segment / positioning
    source_url: str
    datapoints_used: List[str] = field(default_factory=list)


@dataclass
class Market:
    """Complete market sizing result"""
    sector: str
    geography: str
    market_definition: str

    datapoints: Dict[str, DataPoint]       # name → DataPoint
    assumptions: Dict[str, Assumption]     # name → Assumption

    topdown: TopDownModel
    bottomup: BottomUpModel
    triangulation: TriangulationResult

    competitors: List[CompetitorAnalysis]

    attractiveness_score: float            # 1-10, with rubric
    key_risks: List[Tuple[str, str]]       # (risk, likelihood: HIGH/MED/LOW)
    management_questions: List[str]        # Questions to ask about weak assumptions

    created_date: date = field(default_factory=date.today)

    def to_json(self) -> str:
        """Serialize for passing between agents"""
        return json.dumps({
            "sector": self.sector,
            "geography": self.geography,
            "market_definition": self.market_definition,
            "datapoints": {k: v.to_dict() for k, v in self.datapoints.items()},
            "assumptions": {k: v.to_dict() for k, v in self.assumptions.items()},
            "topdown": {
                "tam": self.topdown.tam,
                "sam": self.topdown.sam,
                "som": self.topdown.som,
            },
            "bottomup": {
                "tam": self.bottomup.tam,
                "sam": self.bottomup.sam,
                "som": self.bottomup.som,
            },
            "triangulation": {
                "gap_pct": self.triangulation.gap_pct,
                "explanation": self.triangulation.explanation,
            },
            "attractiveness_score": self.attractiveness_score,
            "key_risks": self.key_risks,
        }, indent=2)


class ValidationError(Exception):
    """Raised when data validation fails"""
    pass


def validate_market(market: Market) -> Tuple[bool, List[str]]:
    """
    Gate-keeper: check that every number is sourced or flagged ASSUMPTION.
    Returns (is_valid, list_of_errors)
    """
    errors = []

    # Every datapoint must be complete
    for name, dp in market.datapoints.items():
        if not DataPoint.validate_required(dp):
            errors.append(f"DataPoint '{name}' incomplete: missing fields or invalid URL")

    # Every assumption must be complete
    for name, a in market.assumptions.items():
        if not Assumption.validate_required(a):
            errors.append(f"Assumption '{name}' incomplete: value not in [low, high] or missing rationale")

    # topdown and bottomup must list which datapoints/assumptions they use
    all_used = set(market.topdown.datapoints_used + market.topdown.assumptions_used +
                   market.bottomup.datapoints_used + market.bottomup.assumptions_used)
    all_defined = set(market.datapoints.keys()) | set(market.assumptions.keys())

    orphaned = all_used - all_defined
    if orphaned:
        errors.append(f"Models reference undefined datapoints/assumptions: {orphaned}")

    # If triangulation gap > 50%, must have explanation
    if market.triangulation.gap_pct > 0.5:
        if not market.triangulation.explanation or len(market.triangulation.explanation) < 20:
            errors.append(f"Gap is {market.triangulation.gap_pct:.0%} but explanation is missing or too brief")

    return len(errors) == 0, errors
