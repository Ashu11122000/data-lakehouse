from deltalake import DeltaTable

from config.settings import CUSTOMER_DELTA_TABLE_PATH


def verify_acid_update():
    print("=" * 70)
    print("DELTA LAKE ACID UPDATE VERIFICATION")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. Load the latest Delta table
    # ---------------------------------------------------------
    delta_table = DeltaTable(str(CUSTOMER_DELTA_TABLE_PATH))

    current_version = delta_table.version()

    print(f"\nCurrent Delta version: {current_version}")

    # ---------------------------------------------------------
    # 2. Read the complete table without Arrow filter
    # ---------------------------------------------------------
    table = delta_table.to_pyarrow_table()

    df = table.to_pandas()

    # Filter using Pandas instead of Arrow
    customer_id = "CUST-1001"

    customer_df = df[
        df["customer_id"] == customer_id
    ]

    # ---------------------------------------------------------
    # 3. Display updated customer record
    # ---------------------------------------------------------
    print("\nCUSTOMER RECORD AFTER UPDATE")
    print("-" * 70)

    print(
        customer_df[
            [
                "customer_id",
                "sentiment",
                "support_notes",
            ]
        ].to_string(index=False)
    )

    # ---------------------------------------------------------
    # 4. Verify update
    # ---------------------------------------------------------
    assert len(customer_df) == 1

    updated_sentiment = customer_df.iloc[0]["sentiment"]

    assert updated_sentiment == "Positive"

    assert (
        "resolved successfully"
        in customer_df.iloc[0]["support_notes"]
    )

    # ---------------------------------------------------------
    # 5. Verify table record count
    # ---------------------------------------------------------
    print("\nTABLE VALIDATION")
    print("-" * 70)

    print(f"Total records: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Current Delta version: {current_version}")

    assert len(df) == 100
    assert len(df.columns) == 18
    assert current_version == 1

    # ---------------------------------------------------------
    # 6. Display Delta transaction history
    # ---------------------------------------------------------
    print("\nDELTA TRANSACTION HISTORY")
    print("-" * 70)

    history = delta_table.history()

    for entry in history:
        print(entry)

    # ---------------------------------------------------------
    # 7. Final verification
    # ---------------------------------------------------------
    print("\nFINAL VALIDATION")
    print("-" * 70)

    print("Record count validation: PASSED")
    print("Column count validation: PASSED")
    print("Customer update validation: PASSED")
    print("Delta version validation: PASSED")

    print("\nACID UPDATE SUCCESSFULLY VERIFIED!")
    print("The Delta table is currently at Version 1.")


if __name__ == "__main__":
    verify_acid_update()