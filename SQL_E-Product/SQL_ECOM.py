def main():
    """
    E-Commerce Sales & Marketing Analytics (SQL Project)
    ----------------------------------------------------

    Overview:
    This project performs end-to-end SQL-based analysis on a synthetic e-commerce dataset using SQLite and pandas.
    It explores key business insights across sales, customer behavior, product performance, and ad campaign effectiveness.

    Objectives:
    - 🛍️ Analyze sales performance by month, region, category, and product.
    - 👥 Understand customer purchase patterns, retention, and revenue contribution.
    - 📦 Identify top-performing products and categories based on units sold, revenue, and discount strategies.
    - 📈 Evaluate marketing performance via ad spend, CPC, CTR, and conversion rates.
    - 📊 Use SQL window functions, CTEs, and aggregation to uncover trends and actionable insights.

    Key Techniques Used:
    - SQL queries via pandas `read_sql_query()`
    - GROUP BY, ORDER BY, LIMIT, and WHERE filters
    - Window Functions: `RANK()`, `LAG()`
    - CTEs for layered queries
    - Correlation analysis (Ad Spend vs Revenue, CTR vs Conversion Rate, etc.)
    - Ranking and time-based trend analysis

    Dataset Columns:
    - Transaction_ID, Customer_ID, Product_ID, Transaction_Date
    - Units_Sold, Discount_Applied, Revenue
    - Clicks, Impressions, Conversion_Rate
    - Category, Region, Ad_CTR, Ad_CPC, Ad_Spend

    Ideal For:
    - SQL Portfolio Project
    - GitHub resume enhancement
    - Demonstrating intermediate-to-advanced SQL skills in real-world e-commerce context

    Author: Krishn Meena"""

    import pandas as pd
    import sqlite3
    from pathlib import Path

    file_path = Path(
        'synthetic_ecommerce_data.csv'
    )
    df = pd.read_csv(file_path)
    df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"])
    df["year"] = df["Transaction_Date"].dt.year
    df["month"] = df["Transaction_Date"].dt.month
    df["day"] = df["Transaction_Date"].dt.day
    conn = sqlite3.connect(":memory:")
    df.to_sql("ECOM", conn, index=False, if_exists="replace")

    # Sales Performance
    querya1 = """SELECT Category,SUM(Revenue) as Revenue
            FROM ECOM
            GROUP BY Category
            ORDER BY Revenue DESC"""
    resulta1 = pd.read_sql_query(querya1, conn)
    print("Sales Performance by Category:")
    print(resulta1)

    querya2 = """SELECT  Region,SUM(Revenue) as Revenue
            FROM ECOM
            GROUP BY  Region
            ORDER BY Revenue DESC """
    resulta2 = pd.read_sql_query(querya2, conn)
    print("\nSales Performance by Region:")
    print(resulta2)

    querya3 = """SELECT  Product_ID,SUM(Revenue) as Revenue
            FROM ECOM
            GROUP BY  Product_ID
            ORDER BY Revenue DESC
            LIMIT 10 """
    resulta3 = pd.read_sql_query(querya3, conn)
    print("\nTop 10 Products by Revenue:")
    print(resulta3)

    querya4 = """SELECT  year,month,SUM(Revenue) as Revenue
            FROM ECOM
            GROUP BY  year,month
              """
    resulta4 = pd.read_sql_query(querya4, conn)
    print("\nMonthly Sales Performance:")
    print(resulta4)

    querya5 = """SELECT Product_ID,COUNT(Units_Sold) AS Total_Quantity
            FROM ECOM
            GROUP BY Product_ID
            ORDER BY Total_Quantity DESC
            LIMIT 10"""
    resulta5 = pd.read_sql_query(querya5, conn)
    print("\nTop 10 Products by Quantity Sold:")
    print(resulta5)

    querya6 = """SELECT Category,AVG(Discount_Applied) AS Average_Discount
            FROM ECOM
            GROUP BY Category
            ORDER BY Average_Discount DESC
            LIMIT 10"""
    resulta6 = pd.read_sql_query(querya6, conn)
    print("\nTop 10 Categories by Average Discount Applied:")
    print(resulta6)

    querya7 = """SELECT SUM(Revenue) AS Actual_Revenue,
            SUM(Revenue/(1-Discount_Applied)) AS Expected_Revenue
            FROM ECOM
            """
    resulta7 = pd.read_sql_query(querya7, conn)
    print("\nActual vs Expected Revenue:")
    print(resulta7)

    # Customer Behaviour
    queryb1 = """SELECT Customer_ID,SUM(Revenue) AS Total_Revenue
            FROM ECOM
            GROUP BY Customer_ID
            ORDER BY Total_Revenue DESC
            LIMIT 10"""
    resultb1 = pd.read_sql_query(queryb1, conn)
    print("\nTop 10 Customers by Total Revenue:")
    print(resultb1)

    queryb2 = """SELECT Customer_ID,COUNT(*) AS Total_Transactions,
            CASE WHEN COUNT(*)>1 THEN 'Repeat customer' ELSE 'One time buyer' END  AS Customer_type
            FROM ECOM
            GROUP BY Customer_ID
            ORDER BY Total_Transactions DESC
           """
    resultb2 = pd.read_sql_query(queryb2, conn)
    print("\nCustomer Segmentation by Transaction Count:")
    print(resultb2)

    queryb3 = """SELECT Customer_ID,COUNT(DISTINCT year||"-"||month) AS Active_Months,
            CASE WHEN COUNT(DISTINCT year||"-"||month)>1 THEN 'Retained' ELSE 'Not Retained' END  AS Retaintion_status
            FROM ECOM
            GROUP BY Customer_ID
            HAVING Retaintion_status='Retained'
            ORDER BY Active_Months DESC
           """
    resultb3 = pd.read_sql_query(queryb3, conn)
    print("\nCustomer Retention Analysis:")
    print(resultb3)

    queryb4 = """SELECT Customer_ID,AVG(Revenue) AS Average_Revenue
            FROM ECOM
            GROUP BY Customer_ID
            ORDER BY Average_Revenue DESC
            LIMIT 10
           """
    resultb4 = pd.read_sql_query(queryb4, conn)
    print("\nTop 10 Customers by Average Revenue:")
    print(resultb4)

    # Product Insight
    queryc1 = """SELECT Product_ID,AVG(Discount_Applied) AS Average_Discount
            FROM ECOM
            GROUP BY Product_ID
            ORDER BY Average_Discount DESC
            LIMIT 10"""
    resultc1 = pd.read_sql_query(queryc1, conn)
    print("\nTop 10 Products by Average Discount Applied:")
    print(resultc1)

    queryc2 = """SELECT Product_ID,ROUND(SUM(Revenue)*1.0/SUM(units_sold),2) AS Revenue_Per_Unit
            FROM ECOM
            GROUP BY Product_ID
            ORDER BY Revenue_Per_Unit DESC
            LIMIT 10"""
    resultc2 = pd.read_sql_query(queryc2, conn)
    print("\nTop 10 Products by Revenue Per Unit:")
    print(resultc2)

    # Regional Trends
    queryd1 = """SELECT Region,product_ID,SUM(Units_Sold) AS Total_Units
            FROM ECOM
            GROUP BY Region,product_ID
            ORDER BY Region,Total_Units DESC
            """
    resultd1 = pd.read_sql_query(queryd1, conn)
    print("\nRegional Product Performance:")
    print(resultd1)

    queryd2 = """SELECT Region, AVG(Ad_CPC) AS Average_CPC
             FROM ECOM
             GROUP BY Region
             ORDER BY Average_CPC DESC
            """
    resultd2 = pd.read_sql_query(queryd2, conn)
    print("\nAverage Ad CPC by Region:")
    print(resultd2)

    # Advertising & Marketing Effectiveness
    querye1 = """SELECT Category,SUM(Ad_Spend) AS AD_Spend,SUM(Revenue) AS Revenue,
            ROUND(SUM(Revenue)*1.0/SUM(Ad_Spend),2) AS Revenue_Per_Spend
            FROM ECOM
            GROUP BY Category
            ORDER BY  Revenue_Per_Spend DESC
            LIMIT 5
            """
    resulte1 = pd.read_sql_query(querye1, conn)
    print("\nTop 5 Categories by Revenue Per Ad Spend:")
    print(resulte1)

    querye2 = """SELECT Region,AVG(Ad_CTR) as Avg_CTR,AVG(Conversion_Rate) AS Avg_Conversion_Rate
            FROM ECOM
            GROUP BY Region
            ORDER BY Avg_CTR DESC,Avg_Conversion_Rate DESC
            """
    resulte2 = pd.read_sql_query(querye2, conn)
    print("\nAverage Ad CTR and Conversion Rate by Region:")
    print(resulte2)

    querye3 = """WITH states AS (
            SELECT
            AVG(Ad_CPC) AS ad_cpc,
            AVG(Conversion_Rate) AS conversion_rate
            FROM ECOM
             ),
           cal AS (
           SELECT 
           ECOM.Ad_CPC - states.ad_cpc AS x,
          ECOM.Conversion_Rate - states.conversion_rate AS y
          FROM ECOM, states
           )
          SELECT 
          (SUM(x * y)) / (SQRT(SUM(x * x)) * SQRT(SUM(y * y))) AS r
           FROM cal"""
    resulte3 = pd.read_sql_query(querye3, conn)
    print("\nCorrelation between Ad CPC and Conversion Rate:")
    print(resulte3)

    querye4 = """SELECT Region,SUM(Ad_Spend) AS AD_Spend,SUM(Revenue) AS Revenue,
            ROUND(SUM(Revenue)*1.0/SUM(Ad_Spend),2) AS Revenue_Per_Spend
            FROM ECOM
            GROUP BY Region
            ORDER BY  Revenue_Per_Spend DESC
            LIMIT 5
            """
    resulte4 = pd.read_sql_query(querye4, conn)
    print("\nTop 5 Regions by Revenue Per Ad Spend:")
    print(resulte4)

    querye5 = """SELECT Product_ID,SUM(Ad_Spend) AS AD_Spend,SUM(Revenue) AS Revenue,
            ROUND(SUM(Revenue)*1.0/SUM(Ad_Spend),2) AS Revenue_Per_Spend
            FROM ECOM
            GROUP BY Product_ID
            ORDER BY  Revenue_Per_Spend DESC
            LIMIT 5
            """
    resulte5 = pd.read_sql_query(querye5, conn)
    print("\nTop 5 Products by Revenue Per Ad Spend:")
    print(resulte5)

    # Advance Query
    queryf1 = """SELECT* 
            FROM (
            SELECT Customer_ID,region,SUM(Revenue) AS Customer_Revenue_Region,RANK() OVER (PARTITION BY Region ORDER BY SUM(Revenue) DESC) AS Customer_Rank
            FROM ECOM
            GROUP BY Customer_ID,region
             )  AS ranked_customers
            WHERE Customer_Rank<=5"""

    resultf1 = pd.read_sql_query(queryf1, conn)
    print("\nTop 5 Customers by Revenue in Each Region:")
    print(resultf1)

    queryf2 = """SELECT* 
            FROM (
            SELECT Product_ID,category,SUM(Revenue) AS product_Revenue_category,RANK() OVER (PARTITION BY category ORDER BY SUM(Revenue) DESC) AS product_Rank
            FROM ECOM
            GROUP BY Product_ID,category
             )  AS ranked_Product
            WHERE product_Rank<=5"""

    resultf2 = pd.read_sql_query(queryf2, conn)
    print("\nTop 5 Products by Revenue in Each Category:")
    print(resultf2)

    queryf3 = """SELECT Transaction_Date,
            SUM(Revenue) AS daily_revenue,
            SUM(SUM(Revenue)) OVER (ORDER BY Transaction_Date) AS Cumulative_Revenue
            FROM ECOM
            GROUP BY Transaction_Date
            ORDER BY Transaction_Date
            """
    resultf3 = pd.read_sql_query(queryf3, conn)
    print("\nDaily Revenue and Cumulative Revenue:")
    print(resultf3)

    queryf4 = """WITH states AS
            (SELECT 
            year,month,
            SUM(Revenue) AS month_revenue  
            FROM ECOM
            GROUP BY year,month
            ),
           cal as(
            SELECT year,month,month_revenue,
            SUM(month_revenue) OVER (ORDER BY year,month) AS Cumulative_monthRevenue,
            LAG(month_revenue) OVER (ORDER BY year,month) AS previous_month_revenue
            FROM states
           ),
           final AS (
           SELECT year,month,month_revenue,Cumulative_monthRevenue,previous_month_revenue,
           ROUND((month_revenue-previous_month_revenue)*100.0/previous_month_revenue,2) AS percentage_change_month,
           LAG(Cumulative_monthRevenue) OVER (ORDER BY year,month) AS previous_month_revenue_cumulative
           FROM cal
           )

           SELECT year,month,month_revenue,percentage_change_month,Cumulative_monthRevenue,
           ROUND((Cumulative_monthRevenue-previous_month_revenue_cumulative)*100.0/previous_month_revenue_cumulative,2) AS percentage_change_cumulative
           FROM final
           ORDER BY year,month          
            """
    resultf4 = pd.read_sql_query(queryf4, conn)
    print("\nMonthly Revenue with Percentage Change:")
    print(resultf4)

    queryf5 = """WITH states AS (
            SELECT
            AVG(Clicks) AS avg_Clicks,
            AVG(Conversion_Rate) AS conversion_rate
            FROM ECOM
             ),
           cal AS (
           SELECT 
           ECOM.Clicks - states.avg_Clicks AS x,
          ECOM.Conversion_Rate - states.conversion_rate AS y
          FROM ECOM, states
           )
          SELECT 
          (SUM(x * y)) / (SQRT(SUM(x * x)) * SQRT(SUM(y * y))) AS r
           FROM cal"""
    resultf5 = pd.read_sql_query(queryf5, conn)
    print("\nCorrelation between Clicks and Conversion Rate:")
    print(resultf5)

    queryf6 = """WITH states AS (
            SELECT
            AVG(Impressions) AS avg_Impressions,
            AVG(Conversion_Rate) AS conversion_rate
            FROM ECOM
             ),
           cal AS (
           SELECT 
           ECOM.Impressions - states.avg_Impressions AS x,
          ECOM.Conversion_Rate - states.conversion_rate AS y
          FROM ECOM, states
           )
          SELECT 
          (SUM(x * y)) / (SQRT(SUM(x * x)) * SQRT(SUM(y * y))) AS r
           FROM cal"""
    resultf6 = pd.read_sql_query(queryf6, conn)
    print("\nCorrelation between Impressions and Conversion Rate:")
    print(resultf6)

    queryf7 = """WITH states AS (
            SELECT
            AVG(Ad_CTR) AS avg_Ad_CTR,
            AVG(Conversion_Rate) AS conversion_rate
            FROM ECOM
             ),
           cal AS (
           SELECT 
           ECOM.Ad_CTR - states.avg_Ad_CTR AS x,
          ECOM.Conversion_Rate - states.conversion_rate AS y
          FROM ECOM, states
           )
          SELECT 
          (SUM(x * y)) / (SQRT(SUM(x * x)) * SQRT(SUM(y * y))) AS r
           FROM cal"""
    resultf7 = pd.read_sql_query(queryf7, conn)
    print("\nCorrelation between Ad CTR and Conversion Rate:")
    print(resultf7)


if __name__ == "__main__":
    main()
