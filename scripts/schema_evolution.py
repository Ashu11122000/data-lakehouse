from pathlib import Path

import pandas as pd
import pyarrow as pa
from deltalake import DeltaTable, write_deltalake

from config.settings import CUSTOMER_DELTA_TABLE_PATH, LAKEHOUSE_DIR


DEMO_TABLE_PATH = LAKEHOUSE_DIR / "schema_evolution_demo"


def classify_customer(spend):
    if spend >= 250000:
        return "VIP"
    elif spend >= 100000:
        return "High"
    elif spend >= 25000:
        return "Medium"
    else:
        return "Low"


def schema_evolution_demo():
    print("=" * 70)
    print("DELTA LAKE SCHEMA EVOLUTION DEMONSTRATION")
    print("=" * 70)

    # --------------------------------------------------
    # Safety check
    # --------------------------------------------------
    if DEMO_TABLE_PATH.exists():
        raise RuntimeError(
            f"Demo table already exists: {DEMO_TABLE_PATH}\n"
            "Do not rerun this script automatically. "
            "Inspect the existing table first."
        )

    # --------------------------------------------------
    # Load current main Delta table
    # --------------------------------------------------
    print("\nLOADING CURRENT CUSTOMER DELTA TABLE")
    print("-" * 70)

    main_table = DeltaTable(str(CUSTOMER_DELTA_TABLE_PATH))
    main_df = main_table.to_pyarrow_table().to_pandas()

    print(f"Main table version: {main_table.version()}")
    print(f"Records loaded: {len(main_df)}")
    print(f"Original columns: {len(main_df.columns)}")

    # --------------------------------------------------
    # Create schema evolution demonstration table
    # Version 0: Original schema
    # --------------------------------------------------
    print("\nCREATING DEMONSTRATION TABLE - VERSION 0")
    print("-" * 70)

    original_arrow_table = pa.Table.from_pandas(
        main_df,
        preserve_index=False,
    )

    write_deltalake(
        str(DEMO_TABLE_PATH),
        original_arrow_table,
        mode="error",
    )

    demo_v0 = DeltaTable(str(DEMO_TABLE_PATH))

    print(f"Demo Delta version: {demo_v0.version()}")
    print(f"Records: {demo_v0.to_pyarrow_table().num_rows}")
    print(f"Columns: {len(demo_v0.schema().fields)}")

    # --------------------------------------------------
    # Add new column
    # --------------------------------------------------
    print("\nADDING NEW COLUMN")
    print("-" * 70)

    evolved_df = main_df.copy()

    evolved_df["customer_lifetime_value_band"] = (
        evolved_df["total_spend"].apply(classify_customer)
    )

    print("New column: customer_lifetime_value_band")
    print("Classification: Low / Medium / High / VIP")

    # --------------------------------------------------
    # Write evolved schema
    # --------------------------------------------------
    print("\nWRITING EVOLVED SCHEMA")
    print("-" * 70)

    evolved_arrow_table = pa.Table.from_pandas(
        evolved_df,
        preserve_index=False,
    )

    write_deltalake(
        str(DEMO_TABLE_PATH),
        evolved_arrow_table,
        mode="overwrite",
        schema_mode="merge",
    )

    demo_v1 = DeltaTable(str(DEMO_TABLE_PATH))
    evolved_table = demo_v1.to_pyarrow_table()
    evolved_result = evolved_table.to_pandas()

    print(f"New Delta version: {demo_v1.version()}")
    print(f"Records: {len(evolved_result)}")
    print(f"Columns: {len(evolved_result.columns)}")

    print("\nEVOLVED SCHEMA")
    print("-" * 70)

    for field in demo_v1.schema().fields:
        print(f"{field.name}: {field.type}")

    # --------------------------------------------------
    # Show new column values
    # --------------------------------------------------
    print("\nCUSTOMER LIFETIME VALUE CLASSIFICATION")
    print("-" * 70)

    print(
        evolved_result[
            [
                "customer_id",
                "customer_segment",
                "total_spend",
                "customer_lifetime_value_band",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\nCLASSIFICATION COUNTS")
    print("-" * 70)

    print(
        evolved_result[
            "customer_lifetime_value_band"
        ].value_counts().to_string()
    )

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------
    print("\nVALIDATION")
    print("-" * 70)

    assert len(main_df) == 100
    assert len(evolved_result) == 100

    assert demo_v0.version() == 1
    assert len(main_df.columns) == 18
    assert len(evolved_result.columns) == 19

    assert "customer_lifetime_value_band" in evolved_result.columns

    assert evolved_result[
        "customer_lifetime_value_band"
    ].notna().all()

    assert set(
        evolved_result["customer_lifetime_value_band"].unique()
    ).issubset({"Low", "Medium", "High", "VIP"})

    print("Original record count validation: PASSED")
    print("Evolved record count validation: PASSED")
    print("Original schema validation: PASSED")
    print("New column validation: PASSED")
    print("Classification validation: PASSED")

    print("\nSCHEMA EVOLUTION SUCCESSFULLY DEMONSTRATED!")

    print("\nKEY RESULT")
    print("-" * 70)
    print(
        "A new column was added to the Delta table while preserving "
        "the 100 customer records."
    )
    print(
        "The schema change was recorded as a new Delta table version."
    )


if __name__ == "__main__":
    schema_evolution_demo()