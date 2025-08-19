def main():
    """
    📊 Data Scientist Job Market Analysis (2020–2025)
    -------------------------------------------------
    This script analyzes a global job dataset containing roles, salaries, employment types, remote ratios, and more.

    🔧 Tools Used:
    - pandas
    - sqlite3
    - SQL (aggregations, window functions, CTEs)

    📈 Key Insights:
    - Salary trends by role, region, experience
    - Remote job growth analysis
    - Company and employment breakdowns
    - Year-on-year job growth and top trending titles

    🗂 Dataset: DataScientist.csv (from Kaggle or local source)

    Author: Krishn Meena
    """
    import pandas as pd
    import sqlite3
    from pathlib import Path

    # Load dataset
    file_path = Path("salaries.csv")
    df = pd.read_csv(file_path)
    conn = sqlite3.connect(":memory:")
    df.to_sql("DATA", conn, index=False, if_exists="replace")

    # Salary Analysis
    querya1 = """SELECT job_title,average_salary,MAX_salary,MIN_salary,
            CASE 
                WHEN average_salary<50000 THEN "LOW"
                WHEN average_salary BETWEEN 50000 AND 100000 THEN "MEDIUM"
                ELSE "HIGH"
              END AS salary_level
            FROM
            (SELECT job_title, AVG(salary_in_usd) AS average_salary,MAX(salary_in_usd) AS MAX_salary,MIN(salary_in_usd) AS MIN_salary                            
            FROM DATA
            GROUP BY job_title)
            ORDER BY average_salary DESC
            """
    resulta1 = pd.read_sql_query(querya1, conn)
    print("\nSalary Analysis by Job Title:")
    print(resulta1)

    querya2 = """SELECT experience_level,average_salary,MAX_salary,MIN_salary,
            CASE 
                WHEN average_salary<50000 THEN "LOW"
                WHEN average_salary BETWEEN 50000 AND 100000 THEN "MEDIUM"
                ELSE "HIGH"
              END AS salary_level
            FROM
            (SELECT experience_level, AVG(salary_in_usd) AS average_salary,MAX(salary_in_usd) AS MAX_salary,MIN(salary_in_usd) AS MIN_salary                            
            FROM DATA
            GROUP BY experience_level)
            ORDER BY average_salary DESC
            """
    resulta2 = pd.read_sql_query(querya2, conn)
    print("\nSalary Analysis by Experience Level:")
    print(resulta2)

    querya3 = """SELECT employment_type,average_salary,MAX_salary,MIN_salary,
            CASE 
                WHEN average_salary<50000 THEN "LOW"
                WHEN average_salary BETWEEN 50000 AND 100000 THEN "MEDIUM"
                ELSE "HIGH"
              END AS salary_level
            FROM
            (SELECT employment_type, AVG(salary_in_usd) AS average_salary,MAX(salary_in_usd) AS MAX_salary,MIN(salary_in_usd) AS MIN_salary                            
            FROM DATA
            GROUP BY employment_type)
            ORDER BY average_salary DESC
            """
    resulta3 = pd.read_sql_query(querya3, conn)
    print("\nSalary Analysis by Employment Type:")
    print(resulta3)

    querya4 = """SELECT remote_ratio,average_salary,MAX_salary,MIN_salary,
            CASE 
                WHEN average_salary<50000 THEN "LOW"
                WHEN average_salary BETWEEN 50000 AND 100000 THEN "MEDIUM"
                ELSE "HIGH"
              END AS salary_level
            FROM
            (SELECT remote_ratio, AVG(salary_in_usd) AS average_salary,MAX(salary_in_usd) AS MAX_salary,MIN(salary_in_usd) AS MIN_salary                            
            FROM DATA
            GROUP BY remote_ratio)
            ORDER BY average_salary DESC
            """
    resulta4 = pd.read_sql_query(querya4, conn)
    print("\nSalary Analysis by Remote Ratio:")
    print(resulta4)

    querya5 = """SELECT company_location,average_salary,MAX_salary,MIN_salary,
            CASE 
                WHEN average_salary<50000 THEN "LOW"
                WHEN average_salary BETWEEN 50000 AND 100000 THEN "MEDIUM"
                ELSE "HIGH"
              END AS salary_level
            FROM
            (SELECT company_location, AVG(salary_in_usd) AS average_salary,MAX(salary_in_usd) AS MAX_salary,MIN(salary_in_usd) AS MIN_salary                            
            FROM DATA
            GROUP BY company_location)
            ORDER BY average_salary DESC
           """
    resulta5 = pd.read_sql_query(querya5, conn)
    print("\nSalary Analysis by Company Location:")
    print(resulta5)

    # Role & title trend
    queryb1 = """SELECT job_title,COUNT(*) AS title_count
            FROM DATA 
            GROUP BY job_title
            ORDER BY title_count DESC
            LIMIT 10
            """
    resultb1 = pd.read_sql_query(queryb1, conn)
    print("\nTop 10 Job Titles by Count:")
    print(resultb1)

    queryb2 = """ SELECT work_year, job_title, title_count, rank
             FROM (
             SELECT 
               work_year,
               job_title,
               COUNT(*) AS title_count,
               RANK() OVER (PARTITION BY work_year ORDER BY COUNT(*) DESC) AS rank
               FROM DATA
               GROUP BY work_year, job_title
               ) AS ranked_title
               WHERE rank <= 5
               ORDER BY work_year, rank
               """
    resultb2 = pd.read_sql_query(queryb2, conn)
    print("\nTop 5 Job Titles by Year:")
    print(resultb2)

    queryb3 = """ SELECT experience_level, job_title, title_count, rank
             FROM (
             SELECT 
               experience_level,
               job_title,
               COUNT(*) AS title_count,
               RANK() OVER (PARTITION BY experience_level ORDER BY COUNT(*) DESC) AS rank
               FROM DATA
               GROUP BY experience_level, job_title
               ) AS ranked_title
               WHERE rank <= 5
               ORDER BY experience_level, rank
               """
    resultb3 = pd.read_sql_query(queryb3, conn)
    print("\nTop 5 Job Titles by Experience Level:")
    print(resultb3)

    # Remote Work impact
    queryc1 = """SELECT work_year, COUNT(remote_ratio) AS remote_jobs,
            CASE WHEN remote_ratio="100" THEN "Remote job"
                 WHEN remote_ratio="0" THEN "On-site job"
                 ELSE "Hybrid job"
                 END AS job_type
            FROM DATA
            GROUP BY work_year,remote_ratio
            """
    resultc1 = pd.read_sql_query(queryc1, conn)
    print("\nRemote Work Impact by Year:")
    print(resultc1)

    queryc2 = """SELECT AVG(salary_in_usd) AS average_salary,
            CASE WHEN remote_ratio="100" THEN "Remote job"
                 WHEN remote_ratio="0" THEN "On-site job"
                 ELSE "Hybrid job"
                 END AS job_type
            FROM DATA
            GROUP BY job_type
            ORDER BY average_salary DESC
            """
    resultc2 = pd.read_sql_query(queryc2, conn)
    print("\nAverage Salary by Remote Work Type:")
    print(resultc2)

    queryc3 = """SELECT company_location,COUNT(*) AS remote_jobs
            FROM DATA
            WHERE remote_ratio="100"
            GROUP BY company_location
            ORDER BY remote_jobs DESC
            LIMIT 10
            """
    resultc3 = pd.read_sql_query(queryc3, conn)
    print("\nTop 10 Companies with Remote Jobs:")
    print(resultc3)

    # geographical insight
    queryd1 = """SELECT company_location,COUNT(*) AS total_jobs,AVG(salary_in_usd) AS Average_salary
            FROM DATA
            GROUP BY company_location
            ORDER BY total_jobs DESC,Average_salary DESC
            LIMIT 10
            """
    resultd1 = pd.read_sql_query(queryd1, conn)
    print("\nTop 10 Company location by Job Count and Average Salary:")
    print(resultd1)

    queryd2 = """SELECT COUNT(*) AS ds_jobs,AVG(salary_in_usd) AS Average_salary,company_location
            FROM DATA
            WHERE job_title="Data Scientist"
            GROUP BY company_location           
            ORDER BY Average_salary DESC          
            """
    resultd2 = pd.read_sql_query(queryd2, conn)
    print("\nData Scientist Jobs by Company Location:")
    print(resultd2)

    # experience vs salary
    querye1 = """SELECT experience_level,work_year,COUNT(*) AS total_jobs,AVG(salary_in_usd) AS Average_salary
            FROM DATA
            GROUP BY experience_level,work_year           
            ORDER BY work_year ASC, Average_salary DESC          
            """
    resulte1 = pd.read_sql_query(querye1, conn)
    print("\nExperience Level vs Salary by Year:")
    print(resulte1)

    querye2 = """SELECT experience_level,company_location,COUNT(*) AS total_jobs,AVG(salary_in_usd) AS Average_salary
            FROM DATA
            GROUP BY experience_level,company_location          
            ORDER BY Average_salary DESC          
            """
    resulte2 = pd.read_sql_query(querye2, conn)
    print("\nExperience Level vs Salary by Company Location:")
    print(resulte2)

    querye3 = """SELECT experience_level,job_title,COUNT(*) AS total_jobs,AVG(salary_in_usd) AS Average_salary
            FROM DATA
            GROUP BY experience_level,job_title          
            ORDER BY total_jobs DESC,Average_salary DESC          
            """
    resulte3 = pd.read_sql_query(querye3, conn)
    print("\nExperience Level vs Salary by Job Title:")
    print(resulte3)

    # employment type
    queryf1 = """SELECT employment_type,COUNT(*) AS total_jobs,AVG(salary_in_usd) AS Average_salary
            FROM DATA
            GROUP BY employment_type           
            ORDER BY total_jobs DESC"""
    resultf1 = pd.read_sql_query(queryf1, conn)
    print("\nEmployment Type Analysis:")
    print(resultf1)

    queryf2 = """SELECT company_location,employment_type,COUNT(*) AS total_jobs,AVG(salary_in_usd) AS Average_salary
            FROM DATA
            GROUP BY company_location ,employment_type           
            ORDER BY company_location ASC"""
    resultf2 = pd.read_sql_query(queryf2, conn)
    print("\nEmployment Type by Company Location:")
    print(resultf2)

    queryf3 = """SELECT job_title,employment_type,COUNT(*) AS total_jobs,AVG(salary_in_usd) AS Average_salary
            FROM DATA
            GROUP BY  job_title,employment_type           
            ORDER BY job_title ASC"""
    resultf3 = pd.read_sql_query(queryf3, conn)
    print("\nEmployment Type by Job Title:")
    print(resultf3)

    # company insight
    queryg1 = """SELECT company_location,AVG(salary_in_usd) AS Average_salary,COUNT(*) AS total_jobs
            FROM DATA
            GROUP BY company_location
            ORDER BY Average_salary DESC"""
    resultg1 = pd.read_sql_query(queryg1, conn)
    print("\nCompany Insight by Location:")
    print(resultg1)

    queryg2 = """SELECT company_size,AVG(salary_in_usd) AS Average_salary,COUNT(*) AS total_jobs
            FROM DATA
            GROUP BY company_size
            ORDER BY Average_salary DESC"""
    resultg2 = pd.read_sql_query(queryg2, conn)
    print("\nCompany Insight by Size:")
    print(resultg2)

    # keyword analysis
    queryh1 = """SELECT job_title,COUNT(*) AS total_jobs,AVG(salary_in_usd) AS Average_salary
            FROM DATA
            WHERE job_title LIKE "%Data Scientist%" OR job_title LIKE "%ML%" OR job_title LIKE "%AI%"
            GROUP BY job_title
            ORDER BY Average_salary DESC"""
    resulth1 = pd.read_sql_query(queryh1, conn)
    print("\nKeyword Analysis for Data Scientist, ML, AI:")
    print(resulth1)

    # year on year comparision
    queryi1 = """SELECT work_year,COUNT(*) AS total_jobs,AVG(salary_in_usd) AS Average_salary
            FROM DATA
            GROUP BY work_year
            ORDER BY work_year ASC"""
    resulti1 = pd.read_sql_query(queryi1, conn)
    print("\nYear on Year Job Count and Average Salary:")
    print(resulti1)

    queryi2 = """SELECT work_year,job_title,COUNT(*) AS total_jobs
            FROM DATA
            GROUP BY work_year,job_title
            ORDER BY work_year ASC"""
    resulti2 = pd.read_sql_query(queryi2, conn)
    print("\nYear on Year Job Count by Title:")
    print(resulti2)

    queryi3 = """WITH job_count AS
            (SELECT work_year,job_title,COUNT(*) AS total_jobs
            FROM DATA
            GROUP BY work_year,job_title
             ),
            growth AS 
            (SELECT work_year,job_title,total_jobs,
             LAG(total_jobs) OVER (PARTITION BY job_title ORDER BY work_year ASC) AS previous_total_jobs
             FROM job_count)
             SELECT work_year,job_title,total_jobs,previous_total_jobs,ROUND((total_jobs-previous_total_jobs)*100.00/NULLIF(previous_total_jobs, 0),2) AS year_on_year_growth 
             FROM growth
             WHERE previous_total_jobs IS NOT NULL
             ORDER BY work_year ASC,total_jobs DESC
             """
    resulti3 = pd.read_sql_query(queryi3, conn)
    print("\nYear on Year Growth by Job Title:")
    print(resulti3)

    queryi4 = """WITH base AS
           (SELECT work_year,
            CASE WHEN remote_ratio="100" THEN "Remote job"
                 WHEN remote_ratio="0" THEN "On-site job"
                 ELSE "Hybrid job"
                 END AS job_type
            FROM DATA
            ),
             remote_count AS
            (SELECT work_year,COUNT(*) AS total_jobs,job_type
            FROM base
            GROUP BY work_year,job_type),
            mid AS
            (SELECT work_year,total_jobs,job_type,LAG(total_jobs) OVER (PARTITION BY job_type ORDER BY work_year ASC) AS Previous_total_jobs
            FROM remote_count)
            SELECT work_year,job_type,total_jobs,Previous_total_jobs,ROUND((total_jobs-Previous_total_jobs)*100.00/NULLIF(Previous_total_jobs, 0),2) AS year_on_growth
            FROM mid
            WHERE Previous_total_jobs IS NOT NULL
            ORDER BY work_year ASC,job_type DESC
             """
    resulti4 = pd.read_sql_query(queryi4, conn)
    print("\nYear on Year Growth by Remote Work Type:")
    print(resulti4)

    queryi5 = """WITH start AS
            (SELECT work_year,job_title,COUNT(*) AS total_jobs
            FROM DATA
            GROUP BY work_year,job_title),
            
            mid AS (SELECT  work_year,job_title, total_jobs,LAG(total_jobs) OVER (PARTITION BY job_title ORDER BY work_year ASC) AS previous_total_jobs
            FROM start
            ORDER BY work_year ASC,total_jobs DESC),

            mid2 AS (SELECT work_year,job_title, total_jobs,previous_total_jobs,ROUND(total_jobs-previous_total_jobs,2) AS absolute_growth,
            ROUND((total_jobs-previous_total_jobs)*100.00/NULLIF(previous_total_jobs, 0),2) AS year_on_year_pctgrowth
            FROM mid
            WHERE previous_total_jobs IS NOT NULL),

            mid3 AS (SELECT work_year,job_title,total_jobs,previous_total_jobs,absolute_growth,year_on_year_pctgrowth,
            RANK() OVER(PARTITION BY work_year ORDER BY year_on_year_pctgrowth DESC) AS rank
            FROM mid2
             )

            SELECT work_year,job_title,total_jobs,previous_total_jobs,absolute_growth,year_on_year_pctgrowth,rank
            FROM mid3
            WHERE rank<=5
            ORDER BY work_year ASC,rank ASC
            """
    resulti5 = pd.read_sql_query(queryi5, conn)
    print("\nTop 5 Job Titles by Year on Year Growth(percentage):")
    print(resulti5)


if __name__ == "__main__":
    main()
