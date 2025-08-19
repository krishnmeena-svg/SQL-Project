def main():
    """
    📊 Project: SQL Sales Data Analysis with SQLite
    🧑‍💻 Author: Krishn Meena

    🔍 Description:
    This project demonstrates SQL-based analysis on retail sales data using SQLite via Python (pandas + sqlite3).
    Key analyses include:
    - Monthly revenue trends
    - Top products, categories, and states
    - Age-group based buying behavior
    - Month-over-month revenue growth
    - Customer & order performance patterns

    📦 Tools Used:
    - pandas, sqlite3

    📁 Outputs:
    - SQL queries with insights stored in DataFrames
    - Ready for export, charting, or dashboard integration

    ▶️ How to Run:
    1. Place 'sales_data.csv' in your working directory
    2. Run the script or use it inside Jupyter/Colab
    """

    import pandas as pd
    import sqlite3
    from pathlib import Path

    file_path = Path(
        "sales_data.csv"
    )
    df = pd.read_csv(file_path)
    df["Month_Num"] = pd.to_datetime(df["Month"], format="%B", errors="coerce").dt.month
    conn = sqlite3.connect("sales_data.db")
    df.to_sql("sales", conn, index=False, if_exists="replace")

    # monthwise revenue
    query1 = """ SELECT Month,SUM(Revenue) AS [Total Revenue]
    FROM sales
    GROUP BY Month
    ORDER BY [Total Revenue] DESC"""
    result1 = pd.read_sql_query(query1, conn)
    print("\nMonthwise Revenue:")
    print(result1)

    # top 5 product
    query2 = """SELECT Product,SUM(Revenue) AS [Total Revenue]
          FROM sales
          GROUP BY Product
          ORDER BY [Total Revenue] DESC
          LIMIT 5 """
    result2 = pd.read_sql_query(query2, conn)
    print("\nTop 5 product revenue wise")
    print(result2)

    # top 10 state
    query3 = """ SELECT State,SUM(Profit) AS [Total Profit] 
           FROM sales
           GROUP BY State
           ORDER BY [Total Profit] DESC
           LIMIT 10"""
    result3 = pd.read_sql_query(query3, conn)
    print("\n Top 5 state profit wise")
    print(result3)

    # best age group
    query4 = """ SELECT Age_group,SUM(order_Quantity) AS [Total Number of Order] 
           FROM sales
           GROUP BY Age_group
           ORDER BY [Total Number of Order] DESC
           """
    result4 = pd.read_sql_query(query4, conn)
    print("\n Top age_group by number of order")
    print(result4)

    # best product category
    query5 = """ SELECT Product_Category,SUM(Profit) AS [Total Profit] 
           FROM sales
           GROUP BY Product_Category
           ORDER BY [Total Profit] DESC
           """
    result5 = pd.read_sql_query(query5, conn)
    print("\n Top product category profit wise")
    print(result5)

    # monthly revenue per category
    query6 = """ SELECT Month,Product_Category,SUM(Revenue) AS [Total Revenue] 
           FROM sales
           GROUP BY Month,Product_Category
           ORDER BY Month
           """
    result6 = pd.read_sql_query(query6, conn)
    print("\n monthly revenue per product category")
    print(result6)

    # percentage revenue growth month wise
    query7 = """SELECT curr.year,
                 curr.month_num,
                 curr.[Current Month Revenue ],
                 prev.[Previous Month Revenue ],
                 ROUND((curr.[Current Month Revenue ]-prev.[Previous Month Revenue ])*100/prev.[Previous Month Revenue ],2) AS [Percentage change]

          FROM
          (SELECT Year,Month_num,SUM(Revenue) AS [Current Month Revenue ]
          FROM sales
          GROUP BY year,Month_num) curr
          LEFT JOIN
          (
          SELECT Year, Month_num,SUM(Revenue) AS [Previous Month Revenue ]
          FROM sales
          GROUP BY year,Month_num) prev

          ON (curr.Year=prev.Year AND curr.month_num=prev.month_num+1)
            OR (curr.Year=prev.Year+1 AND curr.Month_num=1 AND prev.month_num=12)"""
    result7 = pd.read_sql_query(query7, conn)
    print("\n percentage revenue growth month wise ")
    print(result7)

    # Customer Behaviour
    query8 = """SELECT Age_group,Product_Category,COUNT(*) AS [Toatal Order]
          FROM sales 
          GROUP BY Age_group,Product_Category
          HAVING COUNT(*)>1
          ORDER BY [Toatal Order] DESC"""
    result8 = pd.read_sql_query(query8, conn)
    print("\n Customer Behaviour")
    print(result8)

    # order size avg
    query9 = """SELECT State,ROUND((SUM(Revenue)*1.0)/SUM(order_Quantity),2) AS [Avg. Order Value]
          FROM sales 
          GROUP BY State
          ORDER BY [Avg. Order Value] DESC"""
    result9 = pd.read_sql_query(query9, conn)
    print("\n order size avg ")
    print(result9)

    # top selling product performance
    query10 = """WITH top_product AS
        (SELECT Product, SUM(Revenue) AS total_revenue
        FROM sales
        GROUP BY Product
        ORDER BY total_revenue DESC
        LIMIT 1) 
        
        SELECT 
        sales.year,
        sales.Month_num,
        sales.product,
        SUM(Revenue) AS [Total Revenue]
        FROM sales
        JOIN top_product ON top_product.product=sales.product
        GROUP BY sales.year,sales.Month_num,sales.product
        ORDER BY sales.year, sales.Month_num"""
    result10 = pd.read_sql_query(query10, conn)
    print("\n top selling product performance ")
    print(result10)


if __name__ == "__main__":
    main()
