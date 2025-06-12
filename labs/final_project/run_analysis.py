"""
Main execution script for the Life Cycle Analysis (LCA) Automation Tool.

This script performs a full, end-to-end analysis by:
1. Loading product data and environmental impact factors.
2. Performing LCA calculations to determine impacts (carbon, water, energy).
3. Generating and saving a series of visualizations for analysis.
4. Saving the calculated dataframes as CSV files for further use.

To run, execute `python run_analysis.py` from the project's root directory.
"""

import os
import matplotlib.pyplot as plt
from src.data_input import DataInput
from src.calculations import LCACalculator
from src.visualization import LCAVisualizer

# --- CONFIGURATION ---
# Centralized configuration for file paths and analysis parameters.
# This makes the script easier to manage and adapt.
CONFIG = {
    "paths": {
        "input_data": "data/raw/sample_data.csv",
        "impact_factors": "data/raw/impact_factors.json",
        "output_data_dir": "outputs/data",
        "output_figures_dir": "outputs/figures",
    },
    "analysis_products": {
        "comparison_ids": ["P002", "P003"],  # e.g., Steel vs. Wood
        "lifecycle_id": "P001",  # Product for lifecycle breakdown
        "eole_id": "P001",  # Product for end-of-life breakdown
    },
}


def main():
    """
    Main function to orchestrate the LCA workflow.
    """
    # --- 1. SETUP ---
    # Create output directories if they don't already exist.
    print("Setting up output directories...")
    os.makedirs(CONFIG["paths"]["output_data_dir"], exist_ok=True)
    os.makedirs(CONFIG["paths"]["output_figures_dir"], exist_ok=True)

    # --- 2. DATA LOADING ---
    print("Loading input data and impact factors...")
    data_input = DataInput()
    product_data = data_input.read_data(CONFIG["paths"]["input_data"])
    impact_factors = data_input.read_impact_factors(CONFIG["paths"]["impact_factors"])
    print("Data loading complete.")
    print(f"Loaded {len(product_data)} data rows.")

    # --- 3. CALCULATIONS ---
    # The LCACalculator now uses a high-performance vectorized method.
    print("\nPerforming LCA calculations...")
    calculator = LCACalculator(impact_factors=impact_factors)

    impacts_df = calculator.calculate_impacts(product_data)
    total_impacts_df = calculator.calculate_total_impacts(impacts_df)

    # Save the calculated dataframes for reporting or further analysis.
    impacts_df.to_csv(
        f"{CONFIG['paths']['output_data_dir']}/detailed_impacts.csv", index=False
    )
    total_impacts_df.to_csv(
        f"{CONFIG['paths']['output_data_dir']}/total_impacts_summary.csv", index=False
    )
    print("Calculations complete. Results saved to 'outputs/data/'.")
    print("\n--- Total Impacts Summary (Top 5) ---")
    print(total_impacts_df.head())
    print("-" * 40)

    # --- 4. VISUALIZATION & SAVING PLOTS ---
    # Generate all required visuals for the analysis report.
    print("\nGenerating and saving visualizations to 'outputs/figures/'...")
    visualizer = LCAVisualizer()

    # Plot 1: Overall Carbon Impact Breakdown by Material
    fig1 = visualizer.plot_impact_breakdown(
        impacts_df, "carbon_impact", "material_type"
    )
    fig1.suptitle("Carbon Impact Breakdown by Material Type", fontsize=16)
    fig1.savefig(
        f"{CONFIG['paths']['output_figures_dir']}/carbon_breakdown_by_material.png"
    )
    plt.close(fig1)

    # Plot 2: Detailed Lifecycle Impacts for a specific product
    p_id_lifecycle = CONFIG["analysis_products"]["lifecycle_id"]
    fig2 = visualizer.plot_life_cycle_impacts(impacts_df, p_id_lifecycle)
    fig2.suptitle(
        f"Lifecycle Impact Breakdown for Product {p_id_lifecycle}", fontsize=16
    )
    fig2.savefig(
        f"{CONFIG['paths']['output_figures_dir']}/lifecycle_impacts_{p_id_lifecycle}.png"
    )
    plt.close(fig2)

    # Plot 3: Head-to-head Product Comparison
    p_ids_compare = CONFIG["analysis_products"]["comparison_ids"]
    fig3 = visualizer.plot_product_comparison(impacts_df, p_ids_compare)
    fig3.suptitle(f"Product Comparison: {' vs '.join(p_ids_compare)}", fontsize=16)
    fig3.savefig(f"{CONFIG['paths']['output_figures_dir']}/product_comparison.png")
    plt.close(fig3)

    # Plot 4: End-of-Life Management Breakdown
    p_id_eole = CONFIG["analysis_products"]["eole_id"]
    fig4 = visualizer.plot_end_of_life_breakdown(impacts_df, p_id_eole)
    fig4.suptitle(f"End-of-Life Management for Product {p_id_eole}", fontsize=16)
    fig4.savefig(f"{CONFIG['paths']['output_figures_dir']}/end_of_life_{p_id_eole}.png")
    plt.close(fig4)

    # Plot 5: Correlation Matrix of Impact Categories
    fig5 = visualizer.plot_impact_correlation(impacts_df)
    fig5.suptitle("Correlation Matrix of Environmental Impacts", fontsize=16)
    fig5.savefig(
        f"{CONFIG['paths']['output_figures_dir']}/impact_correlation_matrix.png"
    )
    plt.close(fig5)

    print("All visualizations have been saved successfully.")
    print("\nAnalysis finished. 🚀")


main()
