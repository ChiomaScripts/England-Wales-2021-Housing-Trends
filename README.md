# 🏠 Household Tenure Data Exploration & Interactive Dashboard

## 📌 Project Overview
This project performs **Data Preparation, Exploratory Data Analysis (EDA), and Interactive Visualisation** on **household tenure statistics** in England and Wales. 

The analysis explores **homeownership vs renting trends** across different administrative levels:
- **Nation-wide (England vs Wales)**
- **Across the 9 English Regions**
- **At the Local District Level**
- **By household characteristics** (family composition, size, ethnicity, age, multi-generational households)

Additionally, this project includes an **interactive dashboard built with Streamlit** to allow users to explore the data dynamically.

---

## 🔍 Key Features
- 📊 **Exploratory Data Analysis (EDA)** using Pandas & Seaborn.  
- 📈 **Streamlit Interactive Dashboard** for real-time data exploration.  
- 🏙️ **Regional & Local Trends Visualisation**.  
- 👨‍👩‍👧‍👦 **Household Size, Composition, & Ethnicity Analysis**.  

---

## 📂 Project Structure
```
|-- Data Prep & EDA.ipynb # Jupyter Notebook for data analysis 
|-- streamlit_dashboard.py # Streamlit dashboard script 
|-- housingdata.csv # Household tenure dataset 
|-- README.md # Project documentation
```


---

## 🚀 Technologies Used
- **Python**
- **Pandas** → Data manipulation
- **NumPy** → Numerical computations
- **Matplotlib & Seaborn** → Data visualization
- **Streamlit** → Interactive Dashboard
- **Google Colab / Jupyter Notebook** → For analysis

---

## 📜 Usage

1. **Clone the Repository**
```sh
git clone https://github.com/yourusername/household-tenure-analysis.git
cd household-tenure-analysis

2. **Run the Data Analysis Notebook**

3. **Install Required Dependencies**
``pip install pandas numpy matplotlib seaborn streamlit``

4. **Run the Interactive Dashboard**
Launch the **Streamlit Dashboard** by running:
`streamlit run _dashboard.py`
```

---
## 📊 Sample Analysis & Visualisations
```
1️⃣ Homeownership vs Renting in England & Wales
📌 Bar charts comparing homeownership vs renting rates across both nations.

2️⃣ Regional Differences in Tenure
📌 Heatmaps showing variations in tenure distribution across the 9 English regions.

3️⃣ Local District-Level Trends
📌 Scatter plots and bubble maps analysing housing tenure at a granular district level.

4️⃣ Interactive Streamlit Dashboard
📌 Filter & visualise homeownership trends by region, household type, and demographics in real time.
```

---

## 🛠 Future Improvements
-🔹 **Expand Analysis to Scotland & Northern Ireland**.
-🔹 **Include Census Data** to enrich demographic insights.
-🔹 **Enhance Dashboard UI** with more interactive filters & visualisations.
-🔹 **Predictive Modelling** for tenure forecasting.

---

## ⚠️ Important Notes
- This project uses **publicly available housing data**.
- The analysis is **descriptive and exploratory**, with no predictive modelling (yet).

---

## 📜 License
This project is licensed under the **MIT License**.
