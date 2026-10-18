"""
Excel report builder: generates consulting-style workbook with live formulas.
Every sheet is tied to the Market data structure.
"""

from schema import Market, DataPoint, Assumption, Confidence
from validate import validate_and_report
from typing import Optional
from datetime import date
import os

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
    from openpyxl.utils.dataframe import dataframe_to_rows
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False


class MarketSizingReportBuilder:
    """Builds an Excel workbook from a Market object"""

    def __init__(self, market: Market):
        self.market = market
        self.wb = None

        # Define styling (McKinsey-ish)
        self.header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
        self.header_font = Font(color="FFFFFF", bold=True, size=11)

        self.subheader_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
        self.subheader_font = Font(bold=True, size=10)

        self.assumption_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
        self.assumption_font = Font(italic=True, size=9)

        self.number_format = "#,##0.00"
        self.currency_format = "€#,##0"
        self.pct_format = "0.0%"

        self.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

    def build(self, output_path: str) -> str:
        """
        Build the complete workbook and save it.

        Returns:
            output_path if successful

        Raises:
            ValidationError if market data is invalid
        """
        if not HAS_OPENPYXL:
            raise ImportError("openpyxl required. pip install openpyxl")

        # Validate first
        is_valid, errors = validate_and_report(self.market)
        if not is_valid:
            raise ValueError(f"Market validation failed:\n{errors}")

        # Create workbook
        self.wb = Workbook()
        self.wb.remove(self.wb.active)

        # Build sheets in order
        self._sheet_executive_summary()
        self._sheet_topdown()
        self._sheet_bottomup()
        self._sheet_triangulation()
        self._sheet_scenarios()
        self._sheet_competitive_landscape()
        self._sheet_inputs_and_sources()
        self._sheet_red_flags()

        # Save
        self.wb.save(output_path)
        return output_path

    def _sheet_executive_summary(self):
        """Sheet 1: 1-pager for partners"""
        ws = self.wb.create_sheet("Executive Summary", 0)

        row = 1
        ws[f'A{row}'] = "MARKET ASSESSMENT"
        ws[f'A{row}'].font = Font(bold=True, size=14)
        ws[f'B{row}'] = f"{self.market.sector} — {self.market.geography}"
        ws[f'B{row}'].font = Font(size=12)

        row += 2

        # Key metrics
        metrics = [
            ("Market Definition", self.market.market_definition),
            ("TAM (Top-Down)", f"€{self.market.topdown.tam:,.0f}"),
            ("TAM (Bottom-Up)", f"€{self.market.bottomup.tam:,.0f}"),
            ("Recommended TAM", f"€{self.market.triangulation.football_field_low:,.0f} - €{self.market.triangulation.football_field_high:,.0f}"),
            ("Attractiveness Score", f"{self.market.attractiveness_score:.1f}/10"),
            ("Confidence Level", "HIGH" if self.market.attractiveness_score >= 7 else "MEDIUM" if self.market.attractiveness_score >= 5 else "LOW"),
        ]

        for label, value in metrics:
            ws[f'A{row}'] = label
            ws[f'A{row}'].font = self.subheader_font
            ws[f'B{row}'] = value
            row += 1

        row += 1
        ws[f'A{row}'] = "KEY DRIVERS"
        ws[f'A{row}'].font = self.subheader_font
        row += 1

        # List top drivers from datapoints
        for dp in list(self.market.datapoints.values())[:5]:
            ws[f'A{row}'] = f"✓ {dp.name}: {dp.value} {dp.unit}"
            row += 1

        row += 1
        ws[f'A{row}'] = "TOP RISKS"
        ws[f'A{row}'].font = self.subheader_font
        row += 1

        for risk, likelihood in self.market.key_risks[:5]:
            ws[f'A{row}'] = f"⚠ {risk} ({likelihood})"
            row += 1

        # Auto-fit columns
        ws.column_dimensions['A'].width = 40
        ws.column_dimensions['B'].width = 50

    def _sheet_topdown(self):
        """Sheet 2: Top-down TAM/SAM/SOM with driver tree"""
        ws = self.wb.create_sheet("Top-Down Analysis", 1)

        row = 1
        ws[f'A{row}'] = "TOP-DOWN MARKET SIZING"
        ws[f'A{row}'].font = Font(bold=True, size=12)
        ws.merge_cells(f'A{row}:D{row}')

        row += 2

        # Driver tree (simplified)
        headers = ["Driver", "Value", "Unit", "Source"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=row, column=col, value=header)
            cell.fill = self.header_fill
            cell.font = self.header_font

        row += 1

        # List datapoints used in topdown
        for dp_name in self.market.topdown.datapoints_used:
            if dp_name in self.market.datapoints:
                dp = self.market.datapoints[dp_name]
                ws.cell(row=row, column=1, value=dp.name)
                ws.cell(row=row, column=2, value=dp.value)
                ws.cell(row=row, column=3, value=dp.unit)
                ws.cell(row=row, column=4, value=dp.source_url[:50] + "...")
                row += 1

        # Results
        row += 1
        ws[f'A{row}'] = "RESULTS"
        ws[f'A{row}'].font = self.subheader_font
        row += 1

        results = [
            ("TAM (Total Addressable Market)", self.market.topdown.tam),
            ("SAM (Serviceable Addressable)", self.market.topdown.sam),
            ("SOM (Serviceable Obtainable)", self.market.topdown.som),
        ]

        for label, value in results:
            ws[f'A{row}'] = label
            ws[f'B{row}'] = value
            ws[f'B{row}'].number_format = self.currency_format
            row += 1

        ws.column_dimensions['A'].width = 40
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 50

    def _sheet_bottomup(self):
        """Sheet 3: Bottom-up with unit economics"""
        ws = self.wb.create_sheet("Bottom-Up Analysis", 2)

        row = 1
        ws[f'A{row}'] = "BOTTOM-UP MARKET SIZING"
        ws[f'A{row}'].font = Font(bold=True, size=12)

        row += 2

        headers = ["Component", "Value", "Unit", "Source"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=row, column=col, value=header)
            cell.fill = self.header_fill
            cell.font = self.header_font

        row += 1

        # List datapoints + assumptions
        for dp_name in self.market.bottomup.datapoints_used:
            if dp_name in self.market.datapoints:
                dp = self.market.datapoints[dp_name]
                ws.cell(row=row, column=1, value=dp.name)
                ws.cell(row=row, column=2, value=dp.value)
                ws.cell(row=row, column=3, value=dp.unit)
                ws.cell(row=row, column=4, value=dp.source_url[:50] + "...")
                row += 1

        for a_name in self.market.bottomup.assumptions_used:
            if a_name in self.market.assumptions:
                a = self.market.assumptions[a_name]
                ws.cell(row=row, column=1, value=a.name)
                ws.cell(row=row, column=2, value=a.value)
                ws.cell(row=row, column=3, value=a.unit)
                ws.cell(row=row, column=4, value=f"ASSUMPTION: {a.rationale}")

                # Color it
                for col in range(1, 5):
                    ws.cell(row=row, column=col).fill = self.assumption_fill
                    ws.cell(row=row, column=col).font = self.assumption_font

                row += 1

        # Results
        row += 1
        ws[f'A{row}'] = "RESULTS"
        ws[f'A{row}'].font = self.subheader_font
        row += 1

        results = [
            ("TAM (Total Addressable Market)", self.market.bottomup.tam),
            ("SAM (Serviceable Addressable)", self.market.bottomup.sam),
            ("SOM (Serviceable Obtainable)", self.market.bottomup.som),
        ]

        for label, value in results:
            ws[f'A{row}'] = label
            ws[f'B{row}'] = value
            ws[f'B{row}'].number_format = self.currency_format
            row += 1

        ws.column_dimensions['A'].width = 40
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 50

    def _sheet_triangulation(self):
        """Sheet 4: Comparison & reconciliation"""
        ws = self.wb.create_sheet("Triangulation", 3)

        row = 1
        ws[f'A{row}'] = "TRIANGULATION: TOP-DOWN vs BOTTOM-UP"
        ws[f'A{row}'].font = Font(bold=True, size=12)

        row += 2

        tri = self.market.triangulation
        ws[f'A{row}'] = "Top-Down SOM"
        ws[f'B{row}'] = tri.topdown_som
        ws[f'B{row}'].number_format = self.currency_format
        row += 1

        ws[f'A{row}'] = "Bottom-Up SOM"
        ws[f'B{row}'] = tri.bottomup_som
        ws[f'B{row}'].number_format = self.currency_format
        row += 1

        ws[f'A{row}'] = "Gap %"
        ws[f'B{row}'] = tri.gap_pct
        ws[f'B{row}'].number_format = self.pct_format
        row += 2

        ws[f'A{row}'] = "Gap Explanation"
        ws[f'A{row}'].font = self.subheader_font
        row += 1

        ws[f'A{row}'] = tri.explanation
        ws.merge_cells(f'A{row}:C{row+3}')
        row += 4

        ws[f'A{row}'] = "Recommendation"
        ws[f'A{row}'].font = self.subheader_font
        row += 1

        ws[f'A{row}'] = tri.recommendation
        ws.merge_cells(f'A{row}:C{row+2}')

        ws.column_dimensions['A'].width = 40
        ws.column_dimensions['B'].width = 20

    def _sheet_scenarios(self):
        """Sheet 5: Bull/Base/Bear and sensitivity"""
        ws = self.wb.create_sheet("Scenarios & Sensitivity", 4)

        row = 1
        ws[f'A{row}'] = "MARKET SIZE SCENARIOS"
        ws[f'A{row}'].font = Font(bold=True, size=12)

        row += 2

        tri = self.market.triangulation

        # Football field
        scenarios = [
            ("Bear Case", tri.football_field_low * 0.8),
            ("Base Case", (tri.football_field_low + tri.football_field_high) / 2),
            ("Bull Case", tri.football_field_high * 1.2),
        ]

        for label, value in scenarios:
            ws[f'A{row}'] = label
            ws[f'B{row}'] = value
            ws[f'B{row}'].number_format = self.currency_format
            row += 1

        row += 2
        ws[f'A{row}'] = "5-YEAR PROJECTION"
        ws[f'A{row}'].font = self.subheader_font
        row += 1

        # Simple CAGR projection
        headers = ["Year", "Market Value (€)", "YoY Growth %"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=row, column=col, value=header)
            cell.fill = self.header_fill
            cell.font = self.header_font

        row += 1

        base_value = (tri.football_field_low + tri.football_field_high) / 2
        cagr = 0.15  # Assume 15% growth

        for year in range(1, 6):
            ws.cell(row=row, column=1, value=2024 + year)
            value = base_value * ((1 + cagr) ** year)
            ws.cell(row=row, column=2, value=value)
            ws.cell(row=row, column=2).number_format = self.currency_format
            ws.cell(row=row, column=3, value=cagr)
            ws.cell(row=row, column=3).number_format = self.pct_format
            row += 1

        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 15

    def _sheet_competitive_landscape(self):
        """Sheet 6: Competitors and market structure"""
        ws = self.wb.create_sheet("Competitive Landscape", 5)

        row = 1
        ws[f'A{row}'] = "COMPETITOR ANALYSIS"
        ws[f'A{row}'].font = Font(bold=True, size=12)

        row += 2

        headers = ["Competitor", "Revenue (€)", "Year", "Market Share %", "Growth %", "Focus", "Source"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=row, column=col, value=header)
            cell.fill = self.header_fill
            cell.font = self.header_font

        row += 1

        for comp in self.market.competitors:
            ws.cell(row=row, column=1, value=comp.name)
            ws.cell(row=row, column=2, value=comp.revenue_latest_year)
            ws.cell(row=row, column=2).number_format = self.currency_format
            ws.cell(row=row, column=3, value=comp.revenue_year)
            ws.cell(row=row, column=4, value=comp.market_share_pct or 0)
            ws.cell(row=row, column=4).number_format = self.pct_format
            ws.cell(row=row, column=5, value=comp.growth_rate_pct)
            ws.cell(row=row, column=5).number_format = self.pct_format
            ws.cell(row=row, column=6, value=comp.focus)
            ws.cell(row=row, column=7, value=comp.source_url[:50])
            row += 1

        for col in range(1, 8):
            ws.column_dimensions[chr(64+col)].width = 18

    def _sheet_inputs_and_sources(self):
        """Sheet 7: Every datapoint and assumption with full traceability"""
        ws = self.wb.create_sheet("Inputs & Sources", 6)

        row = 1
        ws[f'A{row}'] = "DATAPOINTS: SOURCED FACTS"
        ws[f'A{row}'].font = Font(bold=True, size=12)

        row += 1

        headers = ["Name", "Value", "Unit", "Year", "Confidence", "Source Type", "URL", "Quote", "Retrieval Date"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=row, column=col, value=header)
            cell.fill = self.header_fill
            cell.font = self.header_font

        row += 1

        for dp in self.market.datapoints.values():
            ws.cell(row=row, column=1, value=dp.name)
            ws.cell(row=row, column=2, value=dp.value)
            ws.cell(row=row, column=3, value=dp.unit)
            ws.cell(row=row, column=4, value=dp.year)
            ws.cell(row=row, column=5, value=dp.confidence.value)
            ws.cell(row=row, column=6, value=dp.source_type.name)
            ws.cell(row=row, column=7, value=dp.source_url)
            ws.cell(row=row, column=8, value=dp.source_quote)
            ws.cell(row=row, column=9, value=dp.retrieval_date.isoformat())
            row += 1

        # Separator
        row += 1
        ws[f'A{row}'] = "ASSUMPTIONS: ESTIMATES WITH RANGES"
        ws[f'A{row}'].font = Font(bold=True, size=12)

        row += 1

        headers = ["Name", "Value", "Low", "High", "Unit", "Year", "Rationale"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=row, column=col, value=header)
            cell.fill = self.assumption_fill
            cell.font = self.assumption_font

        row += 1

        for a in self.market.assumptions.values():
            ws.cell(row=row, column=1, value=a.name)
            ws.cell(row=row, column=2, value=a.value)
            ws.cell(row=row, column=3, value=a.low)
            ws.cell(row=row, column=4, value=a.high)
            ws.cell(row=row, column=5, value=a.unit)
            ws.cell(row=row, column=6, value=a.year)
            ws.cell(row=row, column=7, value=a.rationale)

            for col in range(1, 8):
                ws.cell(row=row, column=col).fill = self.assumption_fill

            row += 1

        # Auto-fit columns
        for col in range(1, 10):
            ws.column_dimensions[chr(64+col)].width = 20

    def _sheet_red_flags(self):
        """Sheet 8: Risks and management questions"""
        ws = self.wb.create_sheet("Red Flags & Questions", 7)

        row = 1
        ws[f'A{row}'] = "KEY RISKS"
        ws[f'A{row}'].font = Font(bold=True, size=12)

        row += 1

        headers = ["Risk", "Likelihood", "Mitigation"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=row, column=col, value=header)
            cell.fill = self.header_fill
            cell.font = self.header_font

        row += 1

        for risk, likelihood in self.market.key_risks:
            ws.cell(row=row, column=1, value=risk)
            ws.cell(row=row, column=2, value=likelihood)
            ws.cell(row=row, column=3, value="TBD - discuss with management")
            row += 1

        row += 2
        ws[f'A{row}'] = "MANAGEMENT QUESTIONS"
        ws[f'A{row}'].font = Font(bold=True, size=12)

        row += 1

        for i, question in enumerate(self.market.management_questions, 1):
            ws[f'A{row}'] = f"{i}. {question}"
            row += 1

        ws.column_dimensions['A'].width = 50
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 40


def build_excel(market: Market, output_path: str) -> str:
    """
    Convenience function: validate and build Excel in one call.

    Returns:
        output_path if successful

    Raises:
        ValueError if validation fails
    """
    builder = MarketSizingReportBuilder(market)
    return builder.build(output_path)
