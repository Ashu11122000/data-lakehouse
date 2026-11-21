from deltalake import DeltaTable

from config.settings import LAKEHOUSE_DIR


DEMO_TABLE_PATH = LAKEHOUSE_DIR / "schema_evolution_demo"


def verify_schema_evolution():
    print("=" * 70)
    print("SCHEMA EVOLUTION VERIFICATION")
    print("=" * 70)

    delta_table = DeltaTable(str(DEMO_TABLE_PATH))

    table = delta_table.to_pyarrow_table()
    df = table.to_pandas()

    print(f"\nCurrent Delta version: {delta_table.version()}")
    print(f"Total records: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    print("\nNEW COLUMN")
    print("-" * 70)

    print(df["customer_lifetime_value_band"].value_counts())

    print("\nDELTA HISTORY")
    print("-" * 70)

    for entry in delta_table.history():
        print(entry)

    print("\nVALIDATION")
    print("-" * 70)

    assert delta_table.version() == 1
    assert len(df) == 100
    assert len(df.columns) == 19

    assert "customer_lifetime_value_band" in df.columns

    assert df["customer_lifetime_value_band"].notna().all()

    assert set(
        df["customer_lifetime_value_band"].unique()
    ).issubset({"Low", "Medium", "High", "VIP"})

    counts = df["customer_lifetime_value_band"].value_counts()

    assert counts.sum() == 100

    print("Delta version validation: PASSED")
    print("Record count validation: PASSED")
    print("Column count validation: PASSED")
    print("New column validation: PASSED")
    print("Classification validation: PASSED")

    print("\nSCHEMA EVOLUTION SUCCESSFULLY VERIFIED!")


if __name__ == "__main__":
    verify_schema_evolution()