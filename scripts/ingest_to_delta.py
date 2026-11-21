import json
from datetime import datetime, timezone

import pandas as pd
import pyarrow as pa
from deltalake import DeltaTable, write_deltalake

from config.settings import (
    STRUCTURED_SOURCE_DIR,
    UNSTRUCTURED_SOURCE_DIR,
    CUSTOMER_DELTA_TABLE_PATH,
)


def ingest_customer_data():
    print("=" * 60)
    print("CUSTOMER DATA INGESTION PIPELINE")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Read structured data
    # ---------------------------------------------------------
    csv_file = STRUCTURED_SOURCE_DIR / "customers.csv"

    customers_df = pd.read_csv(csv_file)

    print(f"\nStructured data loaded: {len(customers_df)} records")

    # ---------------------------------------------------------
    # 2. Read metadata JSON
    # ---------------------------------------------------------
    json_file = UNSTRUCTURED_SOURCE_DIR / "customer_metadata.json"

    with open(json_file, encoding="utf-8") as file:
        metadata_records = json.load(file)

    metadata_df = pd.DataFrame(metadata_records)

    print(f"Metadata loaded: {len(metadata_df)} records")

    # ---------------------------------------------------------
    # 3. Validate the datasets before joining
    # ---------------------------------------------------------
    if customers_df["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer IDs found in CSV")

    if metadata_df["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer IDs found in JSON")

    structured_ids = set(customers_df["customer_id"])
    metadata_ids = set(metadata_df["customer_id"])

    if structured_ids != metadata_ids:
        raise ValueError("Customer IDs do not match between datasets")

    print("\nSource data validation passed.")

    # ---------------------------------------------------------
    # 4. Join structured and metadata datasets
    # ---------------------------------------------------------
    unified_df = customers_df.merge(
        metadata_df,
        on="customer_id",
        how="inner",
        validate="one_to_one",
    )

    print(f"Unified dataset created: {len(unified_df)} records")

    # ---------------------------------------------------------
    # 5. Add ingestion timestamp
    # ---------------------------------------------------------
    ingestion_timestamp = datetime.now(timezone.utc)

    unified_df["ingestion_timestamp"] = ingestion_timestamp

    # ---------------------------------------------------------
    # 6. Convert Pandas DataFrame to PyArrow Table
    # ---------------------------------------------------------
    arrow_table = pa.Table.from_pandas(
        unified_df,
        preserve_index=False,
    )

    # ---------------------------------------------------------
    # 7. Prevent accidental re-creation of an existing table
    # ---------------------------------------------------------
    if CUSTOMER_DELTA_TABLE_PATH.exists():
        try:
            DeltaTable(str(CUSTOMER_DELTA_TABLE_PATH))

            raise RuntimeError(
                "Delta table already exists!\n"
                "Initial ingestion will not overwrite it.\n"
                "We will handle subsequent changes through "
                "Delta Lake operations."
            )

        except RuntimeError:
            raise

        except Exception:
            pass

    # ---------------------------------------------------------
    # 8. Write unified dataset to Delta Lake
    # ---------------------------------------------------------
    write_deltalake(
        str(CUSTOMER_DELTA_TABLE_PATH),
        arrow_table,
        mode="error",
    )

    # ---------------------------------------------------------
    # 9. Report results
    # ---------------------------------------------------------
    print("\n" + "=" * 60)
    print("DELTA LAKE INGESTION COMPLETED")
    print("=" * 60)

    print(f"Records ingested: {len(unified_df)}")
    print(f"Columns ingested: {len(unified_df.columns)}")

    print("\nDelta table location:")
    print(CUSTOMER_DELTA_TABLE_PATH)

    print("\nUnified table columns:")
    for column in unified_df.columns:
        print(f"- {column}")

    print("\nSample unified record:")
    print(unified_df.iloc[0].to_dict())

    print("\nINGESTION SUCCESSFUL!")


if __name__ == "__main__":
    ingest_customer_data()