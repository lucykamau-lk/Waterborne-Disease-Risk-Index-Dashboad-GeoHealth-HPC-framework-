# 🌍 Waterborne Disease Risk Index (WDRI) Dashboard

**High-resolution GeoHealth framework for scalable urban health vulnerability assessment**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)]()
[![Dask](https://img.shields.io/badge/Dask-Parallel-orange)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

---

## 📋 Project Overview
This project develops a **Python-based computational framework** to quantify and visualize ward-level waterborne disease risk in **Nairobi, Kenya** at **30m resolution**.  
It integrates **Earth-observation and demographic data** into a weighted composite index (WDRI) and presents results via an **interactive Streamlit dashboard**.  

The framework is designed to be **scalable**, enabling extension from local ward-level analysis to regional or global studies.

---

## 🎯 Objectives
- Build a reproducible pipeline for WDRI computation  
- Normalize, weigh, and aggregate five critical indicators:  
  - 🌧️ Rainfall variability  
  - 🌡️ Land-surface temperature (LST)  
  - 🏙️ Built-up area (LULC)  
  - 👥 Population density  
  - 🚰 Water access deficiency  
- Validate results against known cholera hotspots  
- Provide exportable risk maps and tables  

---

## 🌐 Data Sources
All datasets are **open-source and publicly available**:
- **Satellite EO**: Landsat, VIIRS, MODIS, IMERG  
- **Demographics**: SEDAC / WorldPop  
- **Boundaries**: GADM4  
- **Water Access**: JMP / KNBS  
- Access via **Google Earth Engine (GEE)** and provider portals  

---

## 🛠️ Technical Approach
- **Data Handling**: `xarray`, `pandas`, `geopandas`, `rasterio`  
- **Math & Scaling**: `numpy`, `scikit-learn`  
- **Visualization**: `matplotlib`, `plotly`, `folium`, `streamlit`  
- **HPC Scalability**: `dask` parallel processing for performance gains  

Pipeline features:
- Automated data ingestion  
- Spatial alignment of indicators  
- Normalization and weighted composite indexing  
- Interactive visualization via Streamlit  

---

## 📊 Dashboard
- Interactive visualization of WDRI maps  
- Ward-level risk tables  
- Scalable from local to regional/global analysis  

---

## ✅ Success Criteria
- Automated pipeline generates normalized 30m resolution maps  
- Spatial correlation with cholera hotspots  
- Exportable results for policy and research  

---

## 🔒 Ethics & Safety
- No human-subject data involved  
- All datasets are anonymized and open-source  
- Clear communication of limitations to avoid misinterpretation  

---

## 🎬 Live Demo
- **Slides**: [Link to presentation slides]  
- **Video**: [YouTube demo link]  
- **Dashboard**: [Streamlit Cloud deployment link]  

---

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/wdri-dashboard.git
cd wdri-dashboard

# Install dependencies
pip install -r requirements.txt
