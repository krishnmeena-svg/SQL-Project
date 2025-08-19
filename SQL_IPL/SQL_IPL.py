def main():
 """
 📊 Project: IPL SQL Analysis Project
🧑‍💻 Author: Krishn Meena

This project explores the Indian Premier League (IPL) dataset using SQL queries 
executed via SQLite in a Python (Pandas + SQLite3) environment.

🔍 Objectives:
- Analyze batting and bowling performances using ball-by-ball data
- Generate team-wise and player-wise statistics (runs, wickets, economy, strike rate)
- Apply multi-table joins using `matches` and `deliveries` datasets
- Use SQL functions such as GROUP BY, JOIN, CASE WHEN

📁 Data Files:
- `matches.csv` — match-level information (teams, venue, toss, result, etc.)
- `deliveries.csv` — ball-by-ball data (batsman, bowler, runs, dismissals, etc.)

🛠️ Tools Used:
- Python
- Pandas
- SQLite3
- Google Colab"""

 import pandas as pd
 import sqlite3
 from pathlib import Path

 file_path1 = Path("deliveries.csv")
 file_path2 = Path("matches.csv")
 df1=pd.read_csv( file_path1)
 df2=pd.read_csv( file_path2)
 conn=sqlite3.connect(':memory:')
 df1.to_sql('IPL', conn, index=False, if_exists='replace')
 df2.to_sql('Matches', conn, index=False, if_exists='replace')

 #Batsman Perdformance
 querya1='''SELECT batter,
            SUM(batsman_runs) AS [Total Run]
            FROM IPL
            GROUP BY batter
            ORDER BY [Total Run] DESC
            LIMIT 10'''
 resulta1=pd.read_sql_query(querya1, conn)
 print("\nTop 10 Batsman by Total Runs:")
 print(resulta1)

 querya2='''SELECT batter,
            SUM(batsman_runs) AS [Total Run],
            COUNT(ball) AS [Total Ball],
            ROUND((SUM(batsman_runs)*100.0)/COUNT(ball),2) AS [Strike Rate]
            FROM IPL
            GROUP BY batter
            HAVING COUNT(ball)>500
            ORDER BY [Strike Rate] DESC
            LIMIT 10'''
 resulta2=pd.read_sql_query(querya2, conn)
 print("\nTop 10 Batsman by Strike Rate:")
 print(resulta2)

 querya3='''SELECT batter,
            SUM(CASE WHEN batsman_runs = 4 THEN 1 ELSE 0 END) AS Fours,
            SUM(CASE WHEN batsman_runs = 6 THEN 1 ELSE 0 END) AS Sixes,
            COUNT(ball) AS [Total Boundries]
            FROM IPL
            WHERE batsman_runs IN (4,6)
            GROUP BY batter
            ORDER BY [Total Boundries] DESC
            LIMIT 10'''
 resulta3=pd.read_sql_query(querya3, conn)
 print("\nTop 10 Batsman by Boundaries:")
 print(resulta3)

 querya4='''SELECT a.batter,
            a.season,
            a.[Total Run]

            FROM
            (SELECT IPL.batter,
            Matches.season,
            SUM(IPL.batsman_runs) AS [Total Run]
            FROM IPL
            LEFT JOIN Matches ON IPL.match_id=Matches.id
            GROUP BY Matches.season,IPL.batter
            ) AS a

            WHERE (a.Season,a.[Total Run]) IN

            (SELECT b.season,
            MAX(b.[Total Run])
            FROM
            (SELECT IPL.batter,
            Matches.season,
            SUM(IPL.batsman_runs) AS [Total Run]
            FROM IPL
            LEFT JOIN Matches ON IPL.match_id=Matches.id
            GROUP BY Matches.season,IPL.batter
            ) AS b
            GROUP BY b.Season
            )
            ORDER BY a.Season '''
 resulta4=pd.read_sql_query(querya4, conn)
 print("\nTop Batsman by Season:")
 print(resulta4)

 #Bowler Performance
 queryb1='''SELECT bowler,COUNT(*) AS [Total Wicket]
            FROM IPL
            WHERE dismissal_kind IS NOT NULL AND dismissal_kind NOT IN ('run out', 'retired hurt', 'obstructing the field', 'retired out')
            GROUP BY bowler
            ORDER BY [Total Wicket] DESC
            LIMIT 10'''
 resultb1=pd.read_sql_query(queryb1, conn)
 print("\nTop 10 Bowlers by Total Wickets:")
 print(resultb1)

 queryb2='''SELECT bowler,
            SUM(total_runs) AS [Total Run Given],
            COUNT(ball) AS [Total Ball],
            ROUND((SUM(total_runs)*1.0)/(COUNT(ball)/6.0),2) AS [Economy Rate]
            FROM IPL
            WHERE extras_type NOT IN ("byes","legbyes","penalty")
            GROUP BY bowler
            HAVING COUNT(ball)>50
            ORDER BY [Economy Rate] ASC
            LIMIT 10'''
 resultb2=pd.read_sql_query(queryb2, conn)
 print("\nTop 10 Bowlers by Economy Rate:")
 print(resultb2)

 queryb3='''SELECT bowler,count(*) AS [Total Dots]
            FROM IPL
            WHERE total_runs=0
            GROUP BY bowler
            ORDER BY [Total Dots] DESC
            LIMIT 10'''
 resultb3=pd.read_sql_query(queryb3, conn)
 print("\nTop 10 Bowlers by Total Dot Balls:")
 print(resultb3)

 #Match Level Trends
 queryc1='''SELECT IPL.match_id,
            IPL.inning,
            IPL.batting_team,
            IPL.bowling_team,
            SUM(IPL.total_runs) AS [Total Run],
            Matches.result,
            Matches.result_margin
            FROM IPL
            LEFT JOIN Matches ON IPL.match_id=Matches.id
            GROUP BY IPL.match_id,
            IPL.inning,
            IPL.batting_team,
            IPL.bowling_team,
            Matches.result,
            Matches.result_margin
            ORDER BY IPL.match_id'''
 resultc1=pd.read_sql_query(queryc1, conn)
 print("\nMatch Level Trends:")
 print(resultc1)

 queryc2='''SELECT match_id,
            inning,
            batting_team,
            SUM(total_runs) AS 'Powerplay Runs',
            COUNT(CASE WHEN dismissal_kind IS NOT NULL THEN 1 END) AS 'Wickets lost',
            ROUND((SUM(total_runs)*1.0)/6.0,2) AS [RUN RATE]

            FROM IPL
            WHERE over BETWEEN 0 AND 5
            GROUP BY match_id,
            inning,
            batting_team
            ORDER BY match_id'''
 resultc2=pd.read_sql_query(queryc2, conn)
 print("\nPowerplay Runs and Wickets Lost:")
 print(resultc2)

 #Aggressive Play
 queryd1='''SELECT a.match_id,
            a.batter,
            a.batting_team AS "Batter Team",
            m.winner AS "Winning Team",
            a.sixes AS [Maximum Sixes],
            m.season,
            m.city,
            m.player_of_match

            FROM
            (
            SELECT match_id,
            batting_team,
            batter,
            COUNT(*) AS sixes
            FROM IPL
            WHERE batsman_runs=6
            GROUP BY match_id,
            batter
            ) AS a

            JOIN
            (SELECT b.match_id,
            MAX(b.sixes) AS "max sixes"
            FROM
            (SELECT match_id,
            batter,
            COUNT(*) AS sixes
            FROM IPL
            WHERE batsman_runs=6
            GROUP BY match_id,
            batter) AS b
            GROUP BY b.match_id) AS top_sixes
            ON a.match_id = top_sixes.match_id AND a.sixes = top_sixes."max sixes"
            LEFT JOIN Matches m ON a.match_id = m.id
            ORDER BY a.sixes DESC
            LIMIT 10
            '''
 resultd1=pd.read_sql_query(queryd1, conn)
 print("\nTop 10 Aggressive Players by Maximum Sixes:")
 print(resultd1)

 queryd2='''WITH running_score AS (
            SELECT
            match_id,
            batter,
            batting_team,
            over,
            ball,
            batsman_runs,
            SUM(batsman_runs) OVER (PARTITION BY match_id, batter ORDER BY over, ball
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
            ROW_NUMBER() OVER (PARTITION BY match_id, batter ORDER BY over, ball) AS ball_number
            FROM IPL),

            FirstFifty AS (SELECT*
            FROM
            (SELECT *,
            ROW_NUMBER() OVER (PARTITION BY match_id, batter ORDER BY over, ball) AS rn
            FROM running_score
            WHERE running_total>=50
            )AS sub
            WHERE rn=1)

            SELECT
            match_id,
            batter,
            batting_team,
            ball_number AS balls_to_fifty
            FROM FirstFifty
            ORDER BY balls_to_fifty ASC
            LIMIT 10'''
 resultd2=pd.read_sql_query(queryd2, conn)
 print("\nTop 10 Players by Balls Faced to Reach Fifty:")
 print(resultd2)

 queryd3='''WITH Allbatsman_TotalBoundries AS
           (SELECT batter,COUNT(ball) AS [Total Boundries]
            FROM IPL
            WHERE batsman_runs IN (4,6)
            GROUP BY batter)
            SELECT IPL.batter,Allbatsman_TotalBoundries.[Total Boundries],COUNT(IPL.ball) AS "Total balls Played",ROUND((Allbatsman_TotalBoundries.[Total Boundries]*100.0)/(COUNT(IPL.ball)),2) AS "Percentage of Boundries"
            FROM IPL
            LEFT JOIN Allbatsman_TotalBoundries ON IPL.batter=Allbatsman_TotalBoundries.batter
            WHERE IPL.batsman_runs IN (0,1,2,3,4,5,6) AND (IPL.extras_type IS NULL OR IPL.extras_type != "wides")
            GROUP BY IPL.batter,Allbatsman_TotalBoundries.[Total Boundries]
            HAVING COUNT(IPL.ball)>100
            ORDER BY "Percentage of Boundries" DESC
            LIMIT 10
            '''
 resultd3=pd.read_sql_query(queryd3, conn)
 print("\nTop 10 Players by Percentage of Boundaries:")
 print(resultd3)

 #Dismissal Analysis
 querye1='''SELECT dismissal_kind,
            COUNT(*) AS [Total Dismissal]
            FROM IPL
            WHERE dismissal_kind IS NOT NULL
            GROUP BY dismissal_kind
            ORDER BY [Total Dismissal] DESC
            '''
 resulte1=pd.read_sql_query(querye1, conn)
 print("\nDismissal Analysis:")
 print(resulte1)

 querye2='''SELECT fielder,
            SUM(CASE WHEN dismissal_kind = 'caught' THEN 1 ELSE 0 END) AS catches,
            SUM(CASE WHEN dismissal_kind = 'run out' THEN 1 ELSE 0 END) AS run_outs,
            SUM(CASE WHEN dismissal_kind = 'stumped' THEN 1 ELSE 0 END) AS stumpings,
            COUNT(dismissal_kind) AS "Total"
            FROM IPL
            WHERE dismissal_kind IN ("run out","caught","stumped","caught and bowled") AND fielder IS NOT NULL
            GROUP BY fielder
            ORDER BY "Total" DESC
            LIMIT 10
            '''
 resulte2=pd.read_sql_query(querye2, conn)
 print("\nTop 10 Fielders by Dismissals:")
 print(resulte2)

 querye3='''SELECT bowler,batter,COUNT(*) AS "Total Dismissal"
            FROM IPL
            WHERE dismissal_kind IS NOT NULL AND dismissal_kind NOT IN ('run out', 'retired hurt', 'obstructing the field', 'retired out')
            GROUP BY bowler,batter
            ORDER BY "Total Dismissal" DESC
            LIMIT 10
            '''
 resulte3=pd.read_sql_query(querye3, conn)
 print("\nTop 10 Bowler-Batter Combinations by Dismissals:")
 print(resulte3)

 #Partnership trends
 queryf1='''SELECT IPL.match_id,
            IPL.inning,
            CASE WHEN IPL.batter < IPL.non_striker THEN IPL.batter ||"-"||IPL.non_striker ELSE IPL.non_striker ||"-"||IPL.batter END AS partnership_key,
            SUM(total_runs) AS Partnership,
            IPL.batting_team AS Batting_Team,
            IPL.bowling_team AS Bowling_Team,
            Matches.winner,
            Matches.player_of_match
            FROM IPL
            JOIN Matches ON IPL.match_id = Matches.id
            GROUP BY IPL.match_id, IPL.inning, partnership_key
            ORDER BY Partnership DESC
            LIMIT 10
            '''
 resultf1=pd.read_sql_query(queryf1, conn)
 print("\nTop 10 Partnerships by Runs:")
 print(resultf1)

 queryf2='''SELECT 
            CASE WHEN IPL.batter < IPL.non_striker THEN IPL.batter ||"-"||IPL.non_striker ELSE IPL.non_striker ||"-"||IPL.batter END AS partnership_key,
            SUM(total_runs) AS Partnership   
            FROM IPL
            GROUP BY CASE WHEN IPL.batter < IPL.non_striker THEN IPL.batter ||"-"||IPL.non_striker ELSE IPL.non_striker ||"-"||IPL.batter END
            ORDER BY Partnership DESC
            LIMIT 10
            '''
 resultf2=pd.read_sql_query(queryf2, conn)
 print("\nTop 10 Partnerships by Runs (All Matches):")
 print(resultf2)
            
if __name__ == "__main__":
    main()
      
           









