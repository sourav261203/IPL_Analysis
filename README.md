# 🏏 IPL Analysis Dashboard

An interactive **IPL Data Analysis** project built with **Python** and **Streamlit**.  
It provides insights into batting, bowling, and team performances, including **head-to-head faceoffs, season stats, economy rates, strike rates, and more**.  

---

## 📌 Features
- 📊 **Season-wise Analysis** – Explore stats for each IPL season  
- 🥷 **Batsman vs Bowler Faceoff** – Compare runs, strike rate, wickets, boundaries, and economy  
- 🏏 **Player Statistics** – Career runs, wickets, boundaries, and averages  
- 🏆 **Team Performance** – Season performance and head-to-head comparisons  
- 📈 **Interactive Visualizations** – Charts and tables for better insights  

---

## 🛠️ Tech Stack
- **Python 3.8+**
- [Streamlit](https://streamlit.io/) – For interactive UI  
- [Pandas](https://pandas.pydata.org/) – Data processing  
- [NumPy](https://numpy.org/) – Calculations  
- [Matplotlib / Seaborn / Plotly] – (if used) for visualization  
- [PyArrow](https://arrow.apache.org/) – Fast data loading  
```
---

## 📂 Project Structure

IPL_Analysis/
├── data/               # Raw and cleaned datasets
├── src/                # Core Python modules
│   ├── helper.py       # Utility functions (faceoff, stats, etc.)
│   └── preprocessing.py
├── main.py              # Streamlit app entry point
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```
---

## 🚀 Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/IPL_Analysis.git
cd IPL_Analysis
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Run the Streamlit app**
```bash
streamlit run main.py
```

---
