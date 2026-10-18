"""
Validation gate: ensures all numbers are sourced before Excel generation.
This is called by build_excel.py before writing.
"""

from schema import Market, validate_market, ValidationError
from typing import Tuple, List
import sys


def validate_and_report(market: Market) -> Tuple[bool, str]:
    """
    Validate a Market object and return a human-readable report.

    Returns:
        (is_valid: bool, report: str with errors or success message)
    """
    is_valid, errors = validate_market(market)

    if is_valid:
        # Additional sanity checks
        sanity_checks = _sanity_checks(market)
        if sanity_checks:
            return False, "\n".join(sanity_checks)

        report = f"""
✓ VALIDATION PASSED

Market: {market.sector} ({market.geography})
Datapoints: {len(market.datapoints)} sourced
Assumptions: {len(market.assumptions)} with ranges
Top-Down TAM: €{market.topdown.tam:,.0f}
Bottom-Up TAM: €{market.bottomup.tam:,.0f}
Triangulation gap: {market.triangulation.gap_pct:.0%}

All numbers are traceable to source or explicitly marked ASSUMPTION.
Ready for Excel export.
""".strip()
        return True, report
    else:
        report = f"""
✗ VALIDATION FAILED

Market: {market.sector} ({market.geography})

Errors:
""" + "\n".join(f"  • {e}" for e in errors)
        return False, report


def _sanity_checks(market: Market) -> List[str]:
    """Additional checks beyond schema validation"""
    checks = []

    # TAM should be > 0
    if market.topdown.tam <= 0:
        checks.append("Top-down TAM is zero or negative")
    if market.bottomup.tam <= 0:
        checks.append("Bottom-up TAM is zero or negative")

    # SOM should be < SAM < TAM
    if not (market.topdown.som <= market.topdown.sam <= market.topdown.tam):
        checks.append("Top-down: SOM > SAM > TAM hierarchy violated")
    if not (market.bottomup.som <= market.bottomup.sam <= market.bottomup.tam):
        checks.append("Bottom-up: SOM > SAM > TAM hierarchy violated")

    # If high confidence sources, gap should be < 100%
    high_conf_count = sum(1 for dp in market.datapoints.values() if dp.confidence.value == "HIGH")
    if high_conf_count > len(market.datapoints) * 0.7:  # Most sources are high-confidence
        if market.triangulation.gap_pct > 1.0:  # 100% gap
            checks.append(f"High confidence sources but gap is {market.triangulation.gap_pct:.0%} — review assumptions")

    # Attractiveness score should be 1-10
    if not (1 <= market.attractiveness_score <= 10):
        checks.append(f"Attractiveness score {market.attractiveness_score} is out of range [1, 10]")

    # Should have identified some risks
    if not market.key_risks:
        checks.append("No key risks identified — add at least 3")

    return checks


def validate_file(json_path: str) -> bool:
    """
    Load a Market JSON and validate it.
    Returns True if valid, False if errors.
    Prints report to stdout.
    """
    import json
    from datetime import date

    try:
        with open(json_path) as f:
            data = json.load(f)

        # Reconstruct Market object (simplified; a full implementation would deserialize deeply)
        market = Market(
            sector=data["sector"],
            geography=data["geography"],
            market_definition=data["market_definition"],
            datapoints={},
            assumptions={},
            topdown=None,
            bottomup=None,
            triangulation=None,
            competitors=[],
            attractiveness_score=data.get("attractiveness_score", 5),
            key_risks=data.get("key_risks", []),
            management_questions=data.get("management_questions", []),
        )

        is_valid, report = validate_and_report(market)
        print(report)
        return is_valid

    except Exception as e:
        print(f"✗ Failed to load {json_path}: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate.py <market_json_file>")
        sys.exit(1)

    success = validate_file(sys.argv[1])
    sys.exit(0 if success else 1)
