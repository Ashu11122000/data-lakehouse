"""
Central configuration for the local Data Lakehouse assignment.

This module defines project directories and storage paths.
"""

from pathlib import Path


# ---------------------------------------------------------
# Project Root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------
# Data Directories
# ---------------------------------------------------------

DATA_DIR = PROJECT_ROOT / "data"

SOURCE_DIR = DATA_DIR / "source"

STRUCTURED_SOURCE_DIR = SOURCE_DIR / "structured"

UNSTRUCTURED_SOURCE_DIR = SOURCE_DIR / "unstructured"

BRONZE_DIR = DATA_DIR / "bronze"

SILVER_DIR = DATA_DIR / "silver"

GOLD_DIR = DATA_DIR / "gold"


# ---------------------------------------------------------
# Lakehouse Storage
# ---------------------------------------------------------

LAKEHOUSE_DIR = PROJECT_ROOT / "lakehouse"

CUSTOMER_DELTA_TABLE_PATH = LAKEHOUSE_DIR / "customer_delta_table"


# ---------------------------------------------------------
# Project Directories
# ---------------------------------------------------------

CONFIG_DIR = PROJECT_ROOT / "config"

SCRIPTS_DIR = PROJECT_ROOT / "scripts"

TESTS_DIR = PROJECT_ROOT / "tests"

DOCS_DIR = PROJECT_ROOT / "docs"

LOGS_DIR = PROJECT_ROOT / "logs"


# ---------------------------------------------------------
# Project Information
# ---------------------------------------------------------

PROJECT_NAME = "Local Data Lakehouse Assignment"

TABLE_NAME = "customer_lakehouse"

DATASET_NAME = "customer_dataset"


# ---------------------------------------------------------
# Dataset Configuration
# ---------------------------------------------------------

SAMPLE_RECORD_COUNT = 100

RANDOM_SEED = 42


# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------

def display_project_paths():
    """Display configured project directories."""

    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Source Data: {SOURCE_DIR}")
    print(f"Bronze Layer: {BRONZE_DIR}")
    print(f"Silver Layer: {SILVER_DIR}")
    print(f"Gold Layer: {GOLD_DIR}")
    print(f"Lakehouse: {LAKEHOUSE_DIR}")
    print(f"Delta Table: {CUSTOMER_DELTA_TABLE_PATH}")