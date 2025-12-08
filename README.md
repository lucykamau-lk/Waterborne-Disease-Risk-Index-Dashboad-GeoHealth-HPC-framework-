# 🌍 Waterborne Disease Risk Index (WDRI) & Water Scarcity Index (WSI) Dashboard

**High-resolution GeoHealth framework for scalable urban health vulnerability assessment**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)]()
[![Dask](https://img.shields.io/badge/Dask-Parallel-orange)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

---

## 📋 Project Overview
This project develops a **Python-based computational framework** to quantify and visualize ward-level waterborne disease risk in **Nairobi, Kenya** at **30m resolution**.  
It integrates **Earth-observation EO and demographic data ** into a weighted composite index (WDRI) and presents results via an **interactive Streamlit dashboard**.  

The framework is designed to be **scalable**, enabling extension from local ward-level analysis to regional or global studies.

---

## 🎯 Objectives
- Build a reproducible pipeline for WDRI computation  
- Normalize, weigh, and aggregate five critical indicators:  
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
- **Water Access**: JMP / NWS  
- Access via **Google Earth Engine (GEE)** and provider portals  

---

## 🛠️ Technical Approach
- **Data Handling**: `xarray`, `pandas`, `geopandas`, `rasterio`  
- **Math & Scaling**: `numpy`, `scikit-learn`  
- **Visualization**: `matplotlib`, `plotly`, `folium`, `streamlit`  
- **HPC Scalability**: `dask` parallel processing for high performance 

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
- **Dashboard**: [Streamlit Cloud deployment link]  



