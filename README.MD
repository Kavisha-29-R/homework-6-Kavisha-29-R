# Homework Assignment 6: Interactive Python Apps

This repository contains three Python applications developed using **Dash** and **Streamlit**, along with corresponding demonstration GIFs for each app.  
Each project focuses on building interactive visual tools with real-world data inputs and outputs.

---

## 📁 Contents

| App | Framework | Description | Files |
|-----|------------|--------------|-------|
| **1. BMI Calculator** | Dash | Calculates Body Mass Index (BMI) from user inputs in either metric or imperial units. | `dash_bmi_app.py`, `BMI_Calculator_app.gif` |
| **2. Location Mapper** | Streamlit | Generates an interactive map from user-provided longitude and latitude values with a pinpoint marker. | `location_app.py`, `Location_app.gif` |
| **3. GDP Visualizer** | Streamlit | Displays stacked interactive bar plots of country GDPs by region using IMF, UN, or World Bank data sources. | `gdp_app.py`, `gdp_app.gif` |

---

## ⚙️ 1. Body Mass Index (BMI) Calculator

### Description
A **Dash app** that computes and displays a user’s BMI based on their height and weight.  
Supports both metric (meters, kilograms) and imperial (feet, pounds) units.

### Features
- User selects units for height and weight.  
- Real-time BMI calculation and category display (e.g., Underweight, Normal, Overweight).  
- Responsive, clean UI.

### Files
- `dash_bmi_app.py` — Python source code for the Dash app.  
- `BMI_Calculator_app.gif` — 5–10 second GIF demonstration of the app in use.

---

## 🗺️ 2. Longitude and Latitude Map App

### Description
A **Streamlit app** that allows users to input **longitude** and **latitude**, then visualizes the point on a map.

### Features
- Simple text input boxes for coordinates.  
- Interactive map generated via Streamlit’s built-in mapping features.  
- Marker or icon appears at the exact coordinates.

### Files
- `location_app.py` — Python source code for the Streamlit app.  
- `Location_app.gif` — 5–10 second GIF demonstration of the app in use.

---

## 📊 3. GDP Stacked Bar Plot Visualizer

### Description
A **Streamlit app** that uses web-scraped GDP data (from IMF, UN, and World Bank) to create **stacked interactive bar plots** by region and country using **Plotly**.

### Features
- Dropdown menu for selecting the data source (IMF, UN, or World Bank).  
- Stacked bar chart visualization grouped by region.  
- Interactive hover and zoom functionality.  
- Data pulled from your web-scraping script.

### Files
- `gdp_app.py` — Python source code for the Streamlit app.  
- `GDP_app.gif` — Short demo GIF showing the app’s interactivity.

---

## ▶️ How to Run the Apps

1. **Install dependencies:**
   ```bash
   pip install dash streamlit plotly pandas requests
