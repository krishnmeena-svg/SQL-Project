# 📊 IPL SQL Analysis Project

### 🧑‍💻 Author: Krishn Meena  

This project explores the **Indian Premier League (IPL)** dataset using **SQL queries** executed in a Python environment with **Pandas + SQLite3**.  
It provides insights into batting, bowling, and match-level trends by combining ball-by-ball (`deliveries.csv`) and match-level (`matches.csv`) data.  

---

## 🔍 Objectives
- Analyze **batting and bowling performances** using ball-by-ball data  
- Generate **team-wise and player-wise statistics** (runs, wickets, economy, strike rate)  
- Apply **multi-table joins** (`matches` and `deliveries`)  
- Use SQL operations such as:
  - `GROUP BY`
  - `JOIN`
  - `CASE WHEN`
  - `WINDOW FUNCTIONS`  

---

## 📁 Dataset
- **`matches.csv`** → Match-level data (teams, venue, toss, results, etc.)  
- **`deliveries.csv`** → Ball-by-ball data (batsman, bowler, runs, dismissals, etc.)  

---

## 🛠️ Tools Used
- Python 3  
- Pandas  
- SQLite3  
- Google Colab / Jupyter Notebook  

---

## 📌 Analysis Performed

### 🏏 Batting Performance
- **Top 10 batsmen by runs**  
- **Top 10 batsmen by strike rate** (min 500 balls)  
- **Top boundary hitters (fours & sixes)**  
- **Orange cap winners** (top run-scorer per season)  

### 🎯 Bowling Performance
- **Top 10 bowlers by wickets**  
- **Best economy rates** (min 50 balls)  
- **Most dot balls bowled**  

### 📈 Match Level Trends
- Team-wise **total runs & results**  
- **Powerplay analysis** (runs + wickets in overs 1–6)  

### 💥 Aggressive Play
- **Maximum sixes in a match**  
- **Fastest fifties (balls faced)**  
- **Boundary percentage analysis**  

### 🧹 Dismissal Analysis
- Breakdown of **types of dismissals**  
- **Top fielders** (catches, run-outs, stumpings)  
- **Top bowler-batsman dismissal combos**  

### 🤝 Partnership Trends
- **Top partnerships per match**  
- **All-time top partnerships**  

---

## ▶️ How to Run
1. Clone/download this repository.  
```bash
git clone https://github.com/krishnmeena-svg/SQL_IPL.git
```  
2. download the dataset from kaggle and place it in the same directory as the script(size was more than 25mb).
```Link
https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020
```

3. Run the Python script,inside cloned repository:  
   ```bash
   python SQL_IPL.py


## 📜 License

This project is for educational purposes only.
IPL dataset is publicly available and used here for analysis practice.