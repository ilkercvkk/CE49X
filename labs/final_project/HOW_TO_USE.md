# Life Cycle Analysis (LCA) Automation Tool

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with flake8](https://img.shields.io/badge/flake8-checked-green.svg)](https://flake8.pycqa.org/en/latest/)

This project is a Python tool developed to analyze, compare, and visualize the environmental impacts of various products, with a focus on construction materials, throughout their life cycles.

## 📜 Table of Contents
* [Overview](#-overview)
* [Features](#-features)
* [Project Structure](#-project-structure)
* [Setup and Installation](#-setup-and-installation)
* [How to Use](#-how-to-use)
* [Detailed Documentation](#-detailed-documentation)
* [License](#-license)

## 📖 Overview

Life Cycle Analysis (LCA) is a methodology for assessing the environmental impacts of a product across its entire life span, from raw material extraction ("cradle") to its final disposal ("grave"). This tool automates the LCA process, enabling a direct and data-driven comparison of different materials' environmental performance. It calculates and visualizes key impact indicators to support engineers and architects in making more sustainable design decisions.

## ✨ Features

#### Data Management
* **Multi-format Support:** Ingests data from CSV, Excel, and JSON files.
* **Data Validation:** Ensures data integrity and completeness before processing.
* **Database Integration:** Utilizes a JSON-based database for environmental impact factors.

#### Impact Analysis
* **Core Metrics:** Calculates Carbon Footprint (kg CO2e), Energy Consumption (kWh), and Water Usage (Liters).
* **Waste Tracking:** Aggregates and tracks waste generated throughout the lifecycle.
* **End-of-Life:** Analyzes end-of-life scenarios, including recycling, landfill, and incineration rates.

#### Visualization
* **Impact Breakdowns:** Pie charts showing impact distribution by material or life cycle stage.
* **Lifecycle Hotspots:** Bar charts to identify the most impactful stages for a single product.
* **Product Comparison:** Radar charts for a head-to-head comparison of multiple products.
* **Correlation Analysis:** Heatmaps to visualize the relationships between different impact categories.

## 📁 Project Structure
The repository follows a standard, modular project structure for clarity and scalability.

```
final_project/
├── data/
│   └── raw/
├── notebooks/
│   └── lca_analysis_example.ipynb
├── outputs/                      <-- Generated automatically upon execution
│   ├── data/
│   └── figures/
├── src/
│   └── ... (source code files)
├── tests/
│   └── ... (test files)
├── .gitignore
├── Documentation.ipynb           <-- Detailed analysis and API reference
├── pytest.ini
├── HOW_TO_USE.md                     <-- You are here
├── requirements.txt
└── README.md
```

## 🛠️ Setup and Installation

Follow these steps to set up and run the project locally.

#### 1. Clone the Repository
```bash
git clone [https://github.com/ilkercvkk/CE49X.git](https://github.com/ilkercvkk/CE49X.git)
cd CE49X/labs/final_project/
```

#### 2. Create a Virtual Environment (Recommended)
```bash
# Create the environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies
Install all required libraries using the `requirements.txt` file.
```bash
pip install -r requirements.txt
```
The project is now ready to run.

## 🚀 How to Use

There are two main ways to use this project: running the automated script or verifying the code with tests.

#### 1. Run the Full Analysis
To execute the entire end-to-end analysis, run the main script from the project root directory. This will load the data, perform all calculations, and save the resulting data and figures into the `outputs/` directory.

```bash
python run_analysis.py
```

#### 2. Run the Tests
To verify that all modules are functioning correctly, you can run the test suite using `pytest`.

```bash
pytest
```
A successful run will show all tests passing.

## 📄 Detailed Documentation

For a complete breakdown of the project, including a step-by-step analysis, detailed API reference for every function, and code examples, please refer to the main documentation notebook.

➡️ **[View Detailed Documentation](./Documentation.ipynb)**

To view it locally, start Jupyter Lab and open the file:
```bash
jupyter lab Documentation.ipynb
```
