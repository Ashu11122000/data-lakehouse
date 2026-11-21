from deltalake import DeltaTable

from config.settings import CUSTOMER_DELTA_TABLE_PATH


def demonstrate_acid_update():
    print("=" * 70)
    print("DELTA LAKE ACID UPDATE DEMONSTRATION")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. Load the Delta table
    # ---------------------------------------------------------
    delta_table = DeltaTable(str(CUSTOMER_DELTA_TABLE_PATH))

    initial_version = delta_table.version()

    print(f"\nCurrent Delta version: {initial_version}")

    # Safety check: this demonstration is intended to run once
    if initial_version != 0:
        raise RuntimeError(
            "This demonstration expects Delta version 0.\n"
            f"Current version is {initial_version}.\n"
            "The update demonstration may already have been executed."
        )

    # ---------------------------------------------------------
    # 2. Display the record before update
    # ---------------------------------------------------------
    customer_id = "CUST-1001"

    print("\nCUSTOMER RECORD BEFORE UPDATE")
    print("-" * 70)

    before_table = delta_table.to_pyarrow_table(
        filters=[("customer_id", "=", customer_id)]
    )

    before_df = before_table.to_pandas()

    print(before_df[
        [
            "customer_id",
            "sentiment",
            "support_notes",
        ]
    ].to_string(index=False))

    assert len(before_df) == 1

    original_sentiment = before_df.iloc[0]["sentiment"]

    # ---------------------------------------------------------
    # 3. Perform the Delta Lake update
    # ---------------------------------------------------------
    print("\nEXECUTING DELTA UPDATE")
    print("-" * 70)

    update_metrics = delta_table.update(
        predicate=f"customer_id = '{customer_id}'",
        new_values={
            "sentiment": "Positive",
            "support_notes": (
                "Support issue resolved successfully. "
                "Customer received assistance and confirmation."
            ),
        },
    )

    print("Update operation metrics:")
    print(update_metrics)

    # ---------------------------------------------------------
    # 4. Load the latest table state
    # ---------------------------------------------------------
    updated_delta_table = DeltaTable(
        str(CUSTOMER_DELTA_TABLE_PATH)
    )

    latest_version = updated_delta_table.version()

    print(f"\nNew Delta version: {latest_version}")

    # ---------------------------------------------------------
    # 5. Verify the updated record
    # ---------------------------------------------------------
    print("\nCUSTOMER RECORD AFTER UPDATE")
    print("-" * 70)

    after_table = updated_delta_table.to_pyarrow_table(
        filters=[("customer_id", "=", customer_id)]
    )

    after_df = after_table.to_pandas()

    print(after_df[
        [
            "customer_id",
            "sentiment",
            "support_notes",
        ]
    ].to_string(index=False))

    # ---------------------------------------------------------
    # 6. Verify update correctness
    # ---------------------------------------------------------
    updated_sentiment = after_df.iloc[0]["sentiment"]

    assert len(after_df) == 1
    assert updated_sentiment == "Positive"
    assert original_sentiment != updated_sentiment
    assert latest_version == initial_version + 1

    # ---------------------------------------------------------
    # 7. Display transaction history
    # ---------------------------------------------------------
    print("\nDELTA TRANSACTION HISTORY")
    print("-" * 70)

    history = updated_delta_table.history()

    for entry in history:
        print(entry)

    # ---------------------------------------------------------
    # 8. Final validation
    # ---------------------------------------------------------
    print("\nVALIDATION")
    print("-" * 70)

    print(f"Original Delta version: {initial_version}")
    print(f"Latest Delta version: {latest_version}")
    print(f"Original sentiment: {original_sentiment}")
    print(f"Updated sentiment: {updated_sentiment}")

    assert latest_version == 1

    print("\nACID UPDATE VALIDATION PASSED!")
    print("Delta Lake successfully committed the update.")
    print("The table is now at version 1.")


if __name__ == "__main__":
    demonstrate_acid_update()