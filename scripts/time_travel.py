from deltalake import DeltaTable

from config.settings import CUSTOMER_DELTA_TABLE_PATH


def time_travel_demo():
    print("=" * 70)
    print("DELTA LAKE TIME TRAVEL DEMONSTRATION")
    print("=" * 70)

    table_path = str(CUSTOMER_DELTA_TABLE_PATH)

    # --------------------------------------------------
    # Read Version 0: Original snapshot
    # --------------------------------------------------
    print("\nREADING HISTORICAL VERSION 0")
    print("-" * 70)

    delta_v0 = DeltaTable(table_path, version=0)
    table_v0 = delta_v0.to_pyarrow_table()
    df_v0 = table_v0.to_pandas()

    customer_id = "CUST-1001"
    customer_v0 = df_v0[df_v0["customer_id"] == customer_id]

    print(f"Delta version: {delta_v0.version()}")
    print(f"Total records: {len(df_v0)}")
    print("\nCustomer record in Version 0:")

    print(
        customer_v0[
            ["customer_id", "sentiment", "support_notes"]
        ].to_string(index=False)
    )

    # --------------------------------------------------
    # Read Version 1: Updated snapshot
    # --------------------------------------------------
    print("\nREADING CURRENT VERSION 1")
    print("-" * 70)

    delta_v1 = DeltaTable(table_path, version=1)
    table_v1 = delta_v1.to_pyarrow_table()
    df_v1 = table_v1.to_pandas()

    customer_v1 = df_v1[df_v1["customer_id"] == customer_id]

    print(f"Delta version: {delta_v1.version()}")
    print(f"Total records: {len(df_v1)}")
    print("\nCustomer record in Version 1:")

    print(
        customer_v1[
            ["customer_id", "sentiment", "support_notes"]
        ].to_string(index=False)
    )

    # --------------------------------------------------
    # Compare historical and current snapshots
    # --------------------------------------------------
    print("\nVERSION COMPARISON")
    print("-" * 70)

    sentiment_v0 = customer_v0.iloc[0]["sentiment"]
    sentiment_v1 = customer_v1.iloc[0]["sentiment"]

    notes_v0 = customer_v0.iloc[0]["support_notes"]
    notes_v1 = customer_v1.iloc[0]["support_notes"]

    print(f"Version 0 sentiment: {sentiment_v0}")
    print(f"Version 1 sentiment: {sentiment_v1}")

    print("\nSupport notes:")
    print(f"Version 0: {notes_v0}")
    print(f"Version 1: {notes_v1}")

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------
    print("\nVALIDATION")
    print("-" * 70)

    assert len(df_v0) == 100
    assert len(df_v1) == 100

    assert delta_v0.version() == 0
    assert delta_v1.version() == 1

    assert len(customer_v0) == 1
    assert len(customer_v1) == 1

    assert sentiment_v0 == "Negative"
    assert sentiment_v1 == "Positive"

    assert "payment status" in notes_v0
    assert "resolved successfully" in notes_v1

    print("Version 0 validation: PASSED")
    print("Version 1 validation: PASSED")
    print("Record count validation: PASSED")
    print("Historical sentiment validation: PASSED")
    print("Updated sentiment validation: PASSED")

    print("\nTIME TRAVEL DEMONSTRATION SUCCESSFULLY COMPLETED!")

    print("\nKEY RESULT")
    print("-" * 70)
    print(
        "Delta Lake successfully retrieved the original Version 0 "
        "snapshot and the updated Version 1 snapshot."
    )


if __name__ == "__main__":
    time_travel_demo()