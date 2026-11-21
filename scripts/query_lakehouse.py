import duckdb

from config.settings import CUSTOMER_DELTA_TABLE_PATH


def run_analytics():
    print("=" * 70)
    print("CUSTOMER LAKEHOUSE - SQL ANALYTICS")
    print("=" * 70)

    con = duckdb.connect()

    # Load Delta extension
    con.execute("INSTALL delta")
    con.execute("LOAD delta")

    delta_path = str(CUSTOMER_DELTA_TABLE_PATH).replace("\\", "/")

    # Create a SQL view over the Delta table
    con.execute(
        f"""
        CREATE VIEW customers AS
        SELECT *
        FROM delta_scan('{delta_path}')
        """
    )

    # ---------------------------------------------------------
    # QUERY 1: Overall business summary
    # ---------------------------------------------------------
    print("\n\nQUERY 1: OVERALL CUSTOMER SUMMARY")
    print("-" * 70)

    query_1 = """
        SELECT
            COUNT(*) AS total_customers,
            SUM(total_orders) AS total_orders,
            ROUND(SUM(total_spend), 2) AS total_customer_spend,
            ROUND(AVG(total_spend), 2) AS average_customer_spend,
            ROUND(AVG(total_orders), 2) AS average_orders_per_customer
        FROM customers
    """

    print(con.execute(query_1).fetchdf().to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 2: Customers by segment
    # ---------------------------------------------------------
    print("\n\nQUERY 2: CUSTOMER DISTRIBUTION BY SEGMENT")
    print("-" * 70)

    query_2 = """
        SELECT
            customer_segment,
            COUNT(*) AS customer_count,
            ROUND(
                COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
                2
            ) AS customer_percentage
        FROM customers
        GROUP BY customer_segment
        ORDER BY customer_count DESC
    """

    print(con.execute(query_2).fetchdf().to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 3: Customer distribution by city
    # ---------------------------------------------------------
    print("\n\nQUERY 3: CUSTOMER DISTRIBUTION BY CITY")
    print("-" * 70)

    query_3 = """
        SELECT
            city,
            COUNT(*) AS customer_count,
            ROUND(SUM(total_spend), 2) AS total_spend,
            SUM(total_orders) AS total_orders
        FROM customers
        GROUP BY city
        ORDER BY customer_count DESC
    """

    print(con.execute(query_3).fetchdf().to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 4: Spending by customer segment
    # ---------------------------------------------------------
    print("\n\nQUERY 4: SPENDING ANALYSIS BY SEGMENT")
    print("-" * 70)

    query_4 = """
        SELECT
            customer_segment,
            COUNT(*) AS customer_count,
            ROUND(SUM(total_spend), 2) AS total_spend,
            ROUND(AVG(total_spend), 2) AS average_spend,
            ROUND(AVG(total_orders), 2) AS average_orders
        FROM customers
        GROUP BY customer_segment
        ORDER BY total_spend DESC
    """

    print(con.execute(query_4).fetchdf().to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 5: Active vs inactive customers
    # ---------------------------------------------------------
    print("\n\nQUERY 5: ACTIVE CUSTOMER ANALYSIS")
    print("-" * 70)

    query_5 = """
        SELECT
            is_active,
            COUNT(*) AS customer_count,
            ROUND(
                COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
                2
            ) AS percentage
        FROM customers
        GROUP BY is_active
        ORDER BY is_active DESC
    """

    print(con.execute(query_5).fetchdf().to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 6: Customer sentiment analysis
    # ---------------------------------------------------------
    print("\n\nQUERY 6: CUSTOMER SENTIMENT ANALYSIS")
    print("-" * 70)

    query_6 = """
        SELECT
            sentiment,
            COUNT(*) AS customer_count,
            ROUND(
                COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
                2
            ) AS percentage
        FROM customers
        GROUP BY sentiment
        ORDER BY customer_count DESC
    """

    print(con.execute(query_6).fetchdf().to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 7: Top 10 customers by spending
    # ---------------------------------------------------------
    print("\n\nQUERY 7: TOP 10 HIGH-VALUE CUSTOMERS")
    print("-" * 70)

    query_7 = """
        SELECT
            customer_id,
            first_name,
            last_name,
            city,
            customer_segment,
            total_orders,
            ROUND(total_spend, 2) AS total_spend,
            sentiment
        FROM customers
        ORDER BY total_spend DESC
        LIMIT 10
    """

    print(con.execute(query_7).fetchdf().to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 8: Negative sentiment by city
    # ---------------------------------------------------------
    print("\n\nQUERY 8: NEGATIVE CUSTOMER SENTIMENT BY CITY")
    print("-" * 70)

    query_8 = """
        SELECT
            city,
            COUNT(*) AS negative_customer_count
        FROM customers
        WHERE sentiment = 'Negative'
        GROUP BY city
        ORDER BY negative_customer_count DESC
    """

    print(con.execute(query_8).fetchdf().to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 9: Customer preferences analysis
    # ---------------------------------------------------------
    print("\n\nQUERY 9: CUSTOMER INTEREST ANALYSIS")
    print("-" * 70)

    query_9 = """
        SELECT
            COUNT(*) AS total_customers,

            SUM(
                CASE
                    WHEN preferences LIKE '%Electronics%'
                    THEN 1 ELSE 0
                END
            ) AS electronics_interested,

            SUM(
                CASE
                    WHEN preferences LIKE '%Fashion%'
                    THEN 1 ELSE 0
                END
            ) AS fashion_interested,

            SUM(
                CASE
                    WHEN preferences LIKE '%Beauty%'
                    THEN 1 ELSE 0
                END
            ) AS beauty_interested,

            SUM(
                CASE
                    WHEN preferences LIKE '%Sports%'
                    THEN 1 ELSE 0
                END
            ) AS sports_interested,

            SUM(
                CASE
                    WHEN preferences LIKE '%Gaming%'
                    THEN 1 ELSE 0
                END
            ) AS gaming_interested,

            SUM(
                CASE
                    WHEN preferences LIKE '%Accessories%'
                    THEN 1 ELSE 0
                END
            ) AS accessories_interested

        FROM customers
    """

    print(con.execute(query_9).fetchdf().to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 10: Customer segment and sentiment combination
    # ---------------------------------------------------------
    print("\n\nQUERY 10: SENTIMENT BY CUSTOMER SEGMENT")
    print("-" * 70)

    query_10 = """
        SELECT
            customer_segment,
            sentiment,
            COUNT(*) AS customer_count
        FROM customers
        GROUP BY customer_segment, sentiment
        ORDER BY customer_segment, customer_count DESC
    """

    print(con.execute(query_10).fetchdf().to_string(index=False))

    # ---------------------------------------------------------
    # Final validation
    # ---------------------------------------------------------
    total_records = con.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    print("\n\n" + "=" * 70)
    print("ANALYTICS VALIDATION")
    print("=" * 70)

    print(f"Records queried from Delta Lake: {total_records}")

    assert total_records == 100

    print("Record count validation: PASSED")
    print("All SQL analytics queries executed successfully!")

    con.close()


if __name__ == "__main__":
    run_analytics()