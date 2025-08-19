# 🛍️ E-Commerce Sales & Marketing Analytics (SQL + Python Project)

## 📖 Overview
This project performs **end-to-end SQL-based analytics** on a synthetic **E-commerce dataset** using **SQLite + pandas**.  
It explores insights into **sales trends, customer behavior, product performance, and ad campaign effectiveness**.  

The project is designed as a **portfolio-ready SQL case study** to demonstrate **intermediate-to-advanced SQL skills** with **realistic business analytics**.

---

## 🎯 Objectives
- 📈 **Sales Analysis** → Revenue by category, region, product, and time (monthly/daily trends).  
- 👥 **Customer Insights** → Repeat customers, retention, top spenders, and segmentation.  
- 📦 **Product Performance** → Discounts, revenue per unit, top products.  
- 🌍 **Regional Trends** → Regional demand, CPC, CTR, and conversions.  
- 📊 **Marketing Effectiveness** → ROI on ad spend, correlations between CPC/CTR/Impressions and conversions.  
- 🧮 **Advanced Analytics** → Window functions, CTEs, cumulative revenue, and percentage growth trends.  

---

## 📂 Dataset
**Columns:**
- **Transaction Data** → Transaction_ID, Customer_ID, Product_ID, Transaction_Date  
- **Sales Data** → Units_Sold, Discount_Applied, Revenue  
- **Marketing Data** → Clicks, Impressions, Ad_Spend, Ad_CTR, Ad_CPC, Conversion_Rate  
- **Attributes** → Category, Region  

---

## 🔑 SQL Concepts Used
- **Aggregation** → `SUM`, `AVG`, `COUNT`, `ROUND`  
- **Filtering & Ranking** → `ORDER BY`, `LIMIT`, `WHERE`, `CASE`  
- **Window Functions** → `RANK()`, `LAG()`, `OVER (PARTITION BY ...)`  
- **CTEs (WITH Clauses)** → for step-by-step query pipelines  
- **Correlation Analysis** → manual Pearson correlation in SQL  
- **Time-based Analysis** → monthly/daily revenue trends, cumulative growth  

---

## 📊 Key Analyses Performed

### 🔹 Sales Performance
- Revenue by **category, region, and product**  
- **Top 10 products** by revenue & units sold  
- Monthly and daily sales trends  
- Actual vs Expected revenue (discount impact)  

### 🔹 Customer Behavior
- Top 10 customers by **total revenue & average spend**  
- Customer segmentation (one-time vs repeat buyers)  
- Retention analysis across months  

### 🔹 Product Insights
- Products & categories with highest **discounts**  
- **Revenue per unit** performance  

### 🔹 Regional Trends
- Regional **top products** by units sold  
- Average **CPC** and ad efficiency by region  

### 🔹 Marketing & Advertising
- ROI on ad spend by **category, region, and product**  
- CTR vs Conversion Rate analysis  
- Correlations: **CPC ↔ Conversion Rate**, **Clicks ↔ Conversion Rate**, **Impressions ↔ Conversion Rate**, **CTR ↔ Conversion Rate**  

### 🔹 Advanced Queries
- **Top 5 customers per region** using `RANK()`  
- **Top 5 products per category** using window functions  
- **Cumulative daily and monthly revenue** with growth %  

---

## ⚙️ How to Run
1. Clone this repo:
   ```bash
   git clone https://github.com/krishnmeena-svg/SQL_E-Product.git
   ```
2. Run the analysis,inside cloned repository:
   ```bash
   python SQL_ECOM.py
   ```

## 📌 Ideal For

💼 Portfolio / GitHub Showcase

📊 SQL & Data Analytics Resume Project

🧑‍💻 Practice for SQL Interviews (aggregation, window functions, CTEs)

🛒 Business Intelligence & Marketing Analytics case study

## 👨‍💻 Author

Krishn Meena

🔗 SQL | Data Analytics | Python Enthusiast