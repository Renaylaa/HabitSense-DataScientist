# HabitSense

## Setup Environment - Anaconda
```bash
conda create --name airquality-env python=3.9
conda activate airquality-env
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```bash
streamlit run dashboard/dashboard_airquality.py
```

## Project Overview
HabitSense is a web-based habit tracking platform designed to help users build healthier daily routines through progress monitoring, reminders, and personalized habit recommendations. The project focuses on promoting healthy lifestyles and improving self-awareness related to physical and mental well-being.

## Problem Statement
Many people struggle to maintain healthy habits due to inconsistent routines, lack of motivation, and limited awareness of their daily health behaviors. Existing health applications often focus only on tracking data without providing meaningful recommendations or actionable insights.

## Research Questions
1. How do sleep duration, stress level, and daily step count relate to users’ BMI categories during the health program?
2. Do users with different health goals have different daily calorie target requirements throughout the program?
3. How does program duration influence user's target weight changes during the health program?

## Dataset Information
The dataset contains 10,200 records related to user's health and lifestyle habits during the health program.

Main Variables:
- Gender
- Age
- Occupation
- Height_cm
- Weight_kg
- Target_Weight_kg
- BMI_Value
- BMI_Category
- Goal_Type
- Program_Duration_Days
- Target_Calorie_Day
- Sleep_Duration
- Stress_Level
- Daily_Steps
- Sleep_Disorder

## Project Workflow
**1. Business Understanding**
Defined business problems and research questions related to user's health habits, BMI categories, calorie targets, and program duration.

**2. Data Wrangling**
Performed:

- Data gathering
- Data assessment
- Data cleaning
- Handling missing values
- Data preprocessing

**3. Exploratory Data Analysis (EDA)**
Conducted exploratory analysis to identify:

- Relationships between health variables
- User behavior patterns
- BMI category trends
- Differences between health goals
- Program duration impacts

**4. Visualization & Explanatory Analysis**
Created visualizations to communicate analytical findings and support data interpretation.

**5. Interactive Dashboard Development**
Built an interactive dashboard using Python and Streamlit to help users explore health trends, BMI patterns, and program insights dynamically.

## Features
- Health habit monitoring
- BMI trend analysis
- Health goal comparison
- Interactive data visualization
- User health insight dashboard
- Progress tracking

## Technologies Used
**1. Programming Languages**
- Python
- SQL

**2. Libraries & Frameworks**
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

**Tools**
- Jupyter Notebook
- Visual Studio Code
- GitHub

## Data Scientist Role
1. Business problem identification
2. Research question formulation
3. Data cleaning and preprocessing
4. Exploratory Data Analysis (EDA)
5. Feature Engineering
6. A/B Testing
7. Data visualization
8. Dashboard development using Streamlit
9. Insight generation and reporting

## Team Members
- Full-Stack Developers
- Data Scientists
- AI Engineers

Coding Camp 2026 powered by DBS Foundation
