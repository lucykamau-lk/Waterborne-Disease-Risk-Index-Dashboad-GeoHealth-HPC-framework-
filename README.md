# 🌍 Waterborne Disease Risk Index (WDRI) & Water Scarcity Index (WSI) Dashboard

**High-resolution GeoHealth framework for scalable urban health vulnerability assessment**

---

## 📋 Project Overview
This project develops a **Python-based computational framework** to quantify and visualize ward-level waterborne disease risk in **Nairobi, Kenya** at **30m resolution**.  
It integrates Earth-observation EO and water access data into a weighted composite index (WDRI) and presents results via an **interactive Streamlit dashboard**.  

The framework is designed to be **scalable**, enabling extension from local ward-level analysis to regional or global studies.

---

## 🎯 Objectives
- Build a reproducible pipeline for WDRI/WSI computation  
- Reprroject, Clip, Normalize, Resample and Weigh, and aggregate EO data:  
  - 🌧️ Rainfall variability  
  - 🌡️ Land-surface temperature (LST)  
  - 🏙️ Built-up area (LULC)  
  - 👥 Population density  
  - 🚰 Water access 
  - socioeconomic vulnerability
  - Validate results against known cholera hotspots  
  - Provide exportable risk maps as HTML

---

## 🌐 Data Sources
All datasets are **open-source and publicly available**:
- **Satellite EO**: Landsat, VIIRS, MODIS, IMERG  
- **Demographics**: SEDAC / WorldPop  
- **Boundaries**: GADM4  
- **Water Access**: NWS  
- Access via **Google Earth Engine (GEE)**   

---

## 🛠️ Technical Approach
- **Data Handling**: `xarray`, `pandas`, `geopandas`, `rasterio`  
- **Math & Scaling**: `numpy`, `scikit-learn`  
- **Visualization**: `matplotlib`, `plotly`, `streamlit`  
- **HPC**: Processing for high performance 

Pipeline features:
- Automated data ingestion  
- Spatial alignment of indicators  
- Normalization and weighted composite indexing  
- Interactive visualization via Streamlit  

---

## 📊 Dashboard
- Interactive visualization of WDRI and WSI maps  
- Zoommable maps 
---

## ✅ Success Criteria
- Automated pipeline generates normalized 30m resolution maps  
- Spatial correlation with cholera hotspots  
- Exportable maps as HTML for policy and research  
---

## 🔒 Ethics & Safety
- No human-subject data involved  
- All datasets are anonymized and open-source  
- Clear communication of limitations to avoid misinterpretation  

---

## 🎬 Live Demo
- **Slides**: [Link to presentation slides]  
- **Dashboard**: [Streamlit Cloud deployment link](https://csc-593-programming-for-scientist-jjsiyxj7dngjhkddetpyjh.streamlit.app/)  



