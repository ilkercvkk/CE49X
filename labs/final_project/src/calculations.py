# src/calculations.py
import pandas as pd
from typing import Dict, List


class LCACalculator:
    """
    Handles environmental impact calculations using efficient, vectorized operations.
    """

    def __init__(self, impact_factors: Dict):
        """
        Initializes the calculator with a pre-loaded dictionary of impact factors.
        Args:
            impact_factors: A dictionary containing the impact factors.
        """
        self.impact_factors = impact_factors
        self._factors_df = self._prepare_factors_dataframe()

    def _prepare_factors_dataframe(self) -> pd.DataFrame:
        """Converts the nested impact factors dictionary into a flat DataFrame for merging."""
        factors_list = []
        for material, stages in self.impact_factors.items():
            for stage, impacts in stages.items():
                # Normalize keys for consistency (e.g., 'disposal' -> 'end-of-life')
                stage_key = (
                    "end-of-life"
                    if "end" in stage.lower() or "disposal" in stage.lower()
                    else stage.lower()
                )
                factors_list.append(
                    {
                        "material_type": material.lower(),
                        "life_cycle_stage": stage_key,
                        "carbon_factor": impacts.get("carbon_impact", 0),
                        "energy_factor": impacts.get("energy_impact", 0),
                        "water_factor": impacts.get("water_impact", 0),
                    }
                )
        return pd.DataFrame(factors_list)

    def calculate_impacts(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates environmental impacts using vectorized pandas operations.
        This method is significantly faster than row-by-row iteration.
        """
        # Ensure key columns are lowercase for consistent merging
        data["life_cycle_stage"] = data["life_cycle_stage"].str.lower()
        data["material_type"] = data["material_type"].str.lower()

        # Merge the main data with the factors DataFrame
        merged_df = pd.merge(
            data, self._factors_df, on=["material_type", "life_cycle_stage"], how="left"
        ).fillna(
            0
        )  # Use 0 for any non-matching factors

        # Perform calculations on entire columns at once (vectorization)
        merged_df["carbon_impact"] = (
            merged_df["quantity_kg"] * merged_df["carbon_factor"]
        ) + merged_df["carbon_footprint_kg_co2e"]
        merged_df["energy_impact"] = (
            merged_df["quantity_kg"] * merged_df["energy_factor"]
        ) + merged_df["energy_consumption_kwh"]
        merged_df["water_impact"] = (
            merged_df["quantity_kg"] * merged_df["water_factor"]
        ) + merged_df["water_usage_liters"]

        # Select and return the relevant columns
        result_columns = list(data.columns) + [
            "carbon_impact",
            "energy_impact",
            "water_impact",
        ]
        return merged_df[result_columns]

    def calculate_total_impacts(self, impacts: pd.DataFrame) -> pd.DataFrame:
        """Calculates total impacts across all life cycle stages for each product."""
        total_impacts = (
            impacts.groupby(["product_id", "product_name"])
            .agg(
                {
                    "carbon_impact": "sum",
                    "energy_impact": "sum",
                    "water_impact": "sum",
                    "waste_generated_kg": "sum",
                }
            )
            .reset_index()
        )
        return total_impacts

    def normalize_impacts(self, impacts: pd.DataFrame) -> pd.DataFrame:
        """Normalizes impacts to a common scale (0-1)."""
        normalized = impacts.copy()
        impact_columns = ["carbon_impact", "energy_impact", "water_impact"]
        for col in impact_columns:
            max_value = normalized[col].max()
            if max_value > 0:
                normalized[col] = normalized[col] / max_value
        return normalized

    def compare_alternatives(
        self, impacts: pd.DataFrame, product_ids: List[str]
    ) -> pd.DataFrame:
        """Compares environmental impacts between alternative products on an aggregated level."""
        total_impacts = self.calculate_total_impacts(impacts)
        comparison = total_impacts[total_impacts["product_id"].isin(product_ids)].copy()

        # Calculate relative differences
        for impact_type in ["carbon_impact", "energy_impact", "water_impact"]:
            min_value = comparison[impact_type].min()
            if min_value > 0:
                comparison[f"{impact_type}_relative_diff_%"] = (
                    (comparison[impact_type] - min_value) / min_value
                ) * 100
            else:
                comparison[f"{impact_type}_relative_diff_%"] = 0.0
        return comparison
