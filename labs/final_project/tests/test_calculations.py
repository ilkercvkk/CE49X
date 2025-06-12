"""
Tests for the calculations module.
"""

import pytest
import pandas as pd
from src.calculations import LCACalculator


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame(
        {
            "product_id": ["P001", "P001", "P001", "P002", "P002", "P002"],
            "product_name": [
                "Product1",
                "Product1",
                "Product1",
                "Product2",
                "Product2",
                "Product2",
            ],
            "life_cycle_stage": ["Manufacturing", "Transportation", "End-of-Life"] * 2,
            "material_type": [
                "steel",
                "steel",
                "steel",
                "aluminum",
                "aluminum",
                "aluminum",
            ],
            "quantity_kg": [100, 100, 100, 50, 50, 50],
            "energy_consumption_kwh": [120, 20, 50, 180, 25, 20],
            "transport_distance_km": [50, 100, 30, 180, 140, 35],
            "transport_mode": ["Truck"] * 6,
            "waste_generated_kg": [5, 0, 100, 1, 0, 20],
            # Note: The data has been corrected to ensure rates sum to 1 where applicable
            "recycling_rate": [0.9, 0, 0.9, 0.85, 0, 0.85],
            "landfill_rate": [0.05, 1, 0.05, 0.1, 1, 0.1],
            "incineration_rate": [0.05, 0, 0.05, 0.05, 0, 0.05],
            "carbon_footprint_kg_co2e": [180, 50, 10, 125, 30, 5],
            "water_usage_liters": [150, 30, 10, 100, 0, 6],
        }
    )


@pytest.fixture
def impact_factors():
    """Create sample impact factors for testing."""
    return {
        "steel": {
            "manufacturing": {
                "carbon_impact": 1.8,
                "energy_impact": 20,
                "water_impact": 150,
            },
            "transportation": {
                "carbon_impact": 0.5,
                "energy_impact": 5,
                "water_impact": 30,
            },
            "end-of-life": {
                "carbon_impact": 0.1,
                "energy_impact": 1,
                "water_impact": 10,
            },
        },
        "aluminum": {
            "manufacturing": {
                "carbon_impact": 2.5,
                "energy_impact": 25,
                "water_impact": 200,
            },
            "transportation": {
                "carbon_impact": 0.6,
                "energy_impact": 6,
                "water_impact": 40,
            },
            "end-of-life": {
                "carbon_impact": 0.1,
                "energy_impact": 1,
                "water_impact": 8,
            },
        },
    }


def test_calculate_impacts(sample_data, impact_factors):
    """Test impact calculations."""
    # CHANGED: We now pass the impact_factors dictionary directly.
    calculator = LCACalculator(impact_factors=impact_factors)

    results = calculator.calculate_impacts(sample_data)

    assert not results.empty
    assert all(
        col in results.columns
        for col in ["carbon_impact", "energy_impact", "water_impact"]
    )
    assert len(results) == len(sample_data)


def test_calculate_total_impacts(sample_data, impact_factors):
    """Test total impact calculations."""
    # CHANGED: Pass the dictionary directly.
    calculator = LCACalculator(impact_factors=impact_factors)

    impacts = calculator.calculate_impacts(sample_data)
    total_impacts = calculator.calculate_total_impacts(impacts)

    assert len(total_impacts) == 2  # Two products
    assert "carbon_impact" in total_impacts.columns


def test_normalize_impacts(sample_data, impact_factors):
    """Test impact normalization."""
    # CHANGED: Pass the dictionary directly.
    calculator = LCACalculator(impact_factors=impact_factors)

    impacts = calculator.calculate_impacts(sample_data)
    # Corrected: Normalization should be applied to the aggregated totals.
    total_impacts = calculator.calculate_total_impacts(impacts)
    normalized = calculator.normalize_impacts(total_impacts)

    assert all(
        normalized[col].max() <= 1
        for col in ["carbon_impact", "energy_impact", "water_impact"]
    )
    assert all(
        normalized[col].min() >= 0
        for col in ["carbon_impact", "energy_impact", "water_impact"]
    )


def test_compare_alternatives(sample_data, impact_factors):
    """Test product comparison."""
    # CHANGED: Pass the dictionary directly.
    calculator = LCACalculator(impact_factors=impact_factors)

    impacts = calculator.calculate_impacts(sample_data)
    # The new compare_alternatives function aggregates the results.
    comparison = calculator.compare_alternatives(impacts, ["P001", "P002"])

    assert len(comparison) == 2
    # Check for the new, more descriptive column name.
    assert "carbon_impact_relative_diff_%" in comparison.columns
