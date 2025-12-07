import os
import streamlit as st
import rasterio
import numpy as np
import folium
from streamlit_folium import st_folium
import pandas as pd
from folium.plugins import MiniMap, Fullscreen, MeasureControl
import matplotlib.colors as mcolors
import geopandas as gpd
from folium import Element

st.set_page_config(page_title="WDRI Map Viewer", layout="wide", page_icon="🌊")

st.markdown(
    """
    <style>
    /* Main layout */
    main .block-container {
        padding-top: 0.5rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        padding-bottom: 0rem !important;
    }
    
    /* Map column - professional dark theme */
    [data-testid="column"]:first-child {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
        border-radius: 12px;
        padding: 15px !important;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.4);
    }
    
    [data-testid="column"]:first-child h1 {
        color: #f1f5f9 !important;
        font-size: 1.7rem;
        margin-bottom: 0.5rem;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.8rem;
    }
    
    /* Side panel - clean light theme */
    [data-testid="column"]:nth-child(2) {
        background: linear-gradient(to bottom, #ffffff 0%, #f8fafc 100%) !important;
        border-radius: 12px;
        padding: 15px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        padding: 8px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
    }
    
    /* Better button styling */
    .stButton > button {
        width: 100%;
        margin-top: 10px;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.4) !important;
    }
    
    /* Card-like elements */
    .card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Legend items */
    .legend-item {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
        padding: 6px 10px;
        border-radius: 6px;
        background-color: #f8fafc;
    }
    
    /* Active layer indicator */
    .active-badge {
        display: inline-block;
        padding: 4px 12px;
        background-color: #d1fae5;
        color: #065f46;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-left: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = "."

def get_wsi_colormap():
    colors = ["#00FF00", "#FFFF00", "#FFA500", "#FF0000"]
    return mcolors.ListedColormap(colors)

def get_wdri_colormap():
    colors = ["#00FF00", "#FFA500", "#FF0000"]
    return mcolors.ListedColormap(colors)

def add_raster_to_map(map_obj, tif_path, name, opacity=0.7, layer_type="WSI"):
    try:
        # Check if file exists first
        if not os.path.exists(tif_path):
            st.error(f"❌ File not found: {tif_path}")
            return False, None
            
        with rasterio.open(tif_path) as src:
            arr = src.read(1).astype(float)
            bounds = [[src.bounds.bottom, src.bounds.left],
                      [src.bounds.top, src.bounds.right]]

            nodata = src.nodata
            if nodata is not None:
                arr = np.where(arr == nodata, np.nan, arr)

            if layer_type == "WSI":
                cmap = get_wsi_colormap()
                max_class = 4
            else:
                cmap = get_wdri_colormap()
                max_class = 3

            if np.all(np.isnan(arr)):
                arr_normalized = np.zeros_like(arr)
            else:
                arr_normalized = (arr - 1) / (max_class - 1)
                arr_normalized = np.clip(arr_normalized, 0, 1)

            rgba_img = (cmap(arr_normalized) * 255).astype(np.uint8)
            alpha_mask = (~np.isnan(arr)).astype(np.uint8) * 255
            rgba_img[..., 3] = alpha_mask

            folium.raster_layers.ImageOverlay(
                image=rgba_img,
                bounds=bounds,
                name=name,
                opacity=opacity,
                interactive=True,
                cross_origin=False,
                show=True
            ).add_to(map_obj)
            
            st.success(f"✅ Loaded {name}")
            return True, bounds

    except Exception as e:
        st.error(f"❌ Error loading {name}: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        return False, None

def add_wards_to_map(map_obj):
    """Add Nairobi ward boundaries"""
    wards_path = None
    for ext in ["shp", "geojson"]:
        candidate =  os.path.join(BASE_DIR, "Classified_Maps", f"Nairobi_Wards.{ext}")
        if os.path.exists(candidate):
            wards_path = candidate
            break

    if wards_path is None:
        st.warning("⚠️ Nairobi_Wards shapefile/geojson not found")
        return

    try:
        gdf = gpd.read_file(wards_path)
                
        possible_names = ["name_3"]
        label_field = None
        
        # Check if any column name contains "name_3" (case-insensitive)
        for col in gdf.columns:
            if any(key in col.lower() for key in possible_names):
                label_field = col
                break

        if label_field is None:
            for col in gdf.columns:
                if col.lower() != "geometry":
                    label_field = col
                    break

        folium.GeoJson(
            gdf.to_json(),
            name="Nairobi Wards",
            style_function=lambda feature: {
                "color": "#000000",
                "weight": 0.5,
                "fillOpacity": 0.0,
            },
            highlight_function=lambda feature: {
                "color": "#FF8800",
                "weight": 1.2,
                "fillOpacity": 0.0,
            },
            tooltip=folium.features.GeoJsonTooltip(
                fields=[label_field],
                aliases=["Ward:"],
                localize=True,
                sticky=True,
            ),
        ).add_to(map_obj)

    except Exception as e:
        st.error(f"Error loading Nairobi_Wards layer: {e}")

if "layer_visibility" not in st.session_state:
    st.session_state.layer_visibility = {
        "WSI": True,
        "WDRI Wet": True,
        "WDRI Dry": True,
    }

# SIDEBAR
with st.sidebar:
    st.header("🌍 Map Controls")

    year = st.selectbox("Select Year", [2019, 2024], index=0)

    basemap_options = {
        "CartoDB positron": "CartoDB positron",
        "CartoDB dark_matter": "CartoDB dark_matter",
        "OpenStreetMap": "OpenStreetMap",
    }

    basemap = st.selectbox("Basemap Style", list(basemap_options.keys()))

    st.subheader("📊 Data Layers")
    for layer in ["WSI", "WDRI Wet", "WDRI Dry"]:
        st.session_state.layer_visibility[layer] = st.checkbox(
            f"📍 {layer}",
            value=st.session_state.layer_visibility[layer],
            key=f"checkbox_{layer}",
        )

    show_wards = st.checkbox("Show ward boundaries", value=True)
    opacity = st.slider("Layer Opacity", 0.1, 1.0, 0.7, 0.1)

    st.subheader("⚙️ Map Settings")
    zoom_level = st.slider("Zoom Level", 5, 18, 11)
    show_measure = st.checkbox("Enable Measurement Tool", True)

# MAIN LAYOUT - 2 COLUMNS FOR LARGER MAP
col1, col2 = st.columns([8, 3], gap="small")

with col1:
    st.title(f"🌊 Nairobi Waterborne Disease Risk (WDRI) & Water Scarcity (WSI) Hotspots Map Viewer – {year}")
    
    # Create the map
    m = folium.Map(
        location=[-1.2864, 36.8172],
        zoom_start=zoom_level,
        tiles=basemap_options[basemap],
        control_scale=True,
    )

    # Add map plugins
    minimap = MiniMap()
    m.add_child(minimap)

    if show_measure:
        MeasureControl().add_to(m)

    Fullscreen().add_to(m)

    layer_bounds = []

    # Layer file definitions
    MAPS_FOLDER ="Classified_Maps"
    layer_files = {
        "WSI": {
            2019: os.path.join(MAPS_FOLDER, "WSI_2019_CLASS.tif"),
            2024: os.path.join(MAPS_FOLDER, "WSI_2024_CLASS.tif"),
        },
        "WDRI Wet": {
            2019: os.path.join(MAPS_FOLDER, "WDRI_Wet_2019_CLASS.tif"),
            2024: os.path.join(MAPS_FOLDER, "WDRI_Wet_2024_CLASS.tif"),
        },
        "WDRI Dry": {
            2019: os.path.join(MAPS_FOLDER, "WDRI_Dry_2019_CLASS.tif"),
            2024: os.path.join(MAPS_FOLDER, "WDRI_Dry_2024_CLASS.tif"),
        },
    }

    wsi_active = False
    wdri_active = False

    # Add raster layers to map
    for layer, visible in st.session_state.layer_visibility.items():
        if visible and layer in layer_files:
            filename = layer_files[layer][year]
            tif_path = os.path.join(BASE_DIR, filename)
            
            layer_type = "WSI" if layer == "WSI" else "WDRI"
            
            if layer == "WSI":
                wsi_active = True
            else:
                wdri_active = True

            success, bounds = add_raster_to_map(
                m, tif_path, f"{layer} {year}", opacity=opacity, layer_type=layer_type
            )

            if success and bounds:
                layer_bounds.append(bounds)

    # Add ward boundaries if enabled
    if show_wards:
        add_wards_to_map(m)

    # Fit map bounds to visible layers
    if layer_bounds:
        all_bounds = np.vstack(layer_bounds)
        m.fit_bounds([
            [all_bounds[:, 0].min(), all_bounds[:, 1].min()],
            [all_bounds[:, 0].max(), all_bounds[:, 1].max()],
        ])

    # Add layer control
    folium.LayerControl(position="topright").add_to(m)

    # DEBUG: Show what layers were successfully added
    st.write("**Debug Info:**")
    st.write(f"Number of layers in map: {len(m._children)}")
    st.write(f"Layer bounds collected: {len(layer_bounds)}")
    st.write(f"Show wards: {show_wards}")

    # Display the map - TALLER for better view
    st_folium(m, use_container_width=True, height=750, key="main_map")

with col2:
    # Create tabs for better organization
    tab1, tab2 = st.tabs(["📊 Active Layers", "🛠️ Map Tools"])
    
    with tab1:
        st.markdown("### Active Layers")
        
        active_layers = [
            layer for layer, visible in st.session_state.layer_visibility.items()
            if visible
        ]
        
        if active_layers:
            for layer in active_layers:
                st.markdown(f"**{layer} {year}**")
                st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span>Status: <span class="active-badge">ACTIVE</span></span>
                        <span style="font-size: 0.9rem; color: #64748b;">📍</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No layers active")
        
        if show_wards:
            st.markdown("---")
            st.markdown("**🗺️ Ward Boundaries**")
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span>Status: <span style="background-color: #d1fae5; color: #065f46; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">ENABLED</span></span>
                    <span style="font-size: 0.9rem; color: #64748b;">🗺️</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Map Tools")
        
        # Download button
        map_html = m._repr_html_()
        st.download_button(
            label="📥 Download Map as HTML",
            data=map_html,
            file_name=f"WDRI_Map_Nairobi_{year}.html",
            mime="text/html",
            use_container_width=True
        )
        
        st.markdown("---")
        
        # Current settings
        st.markdown("#### Current Settings")
        st.markdown(f"""
        <div class="card">
            <div class="legend-item">
                <div style="width: 8px; height: 8px; background-color: #3b82f6; border-radius: 50%; margin-right: 10px;"></div>
                <span><strong>Year:</strong> {year}</span>
            </div>
            <div class="legend-item">
                <div style="width: 8px; height: 8px; background-color: #8b5cf6; border-radius: 50%; margin-right: 10px;"></div>
                <span><strong>Basemap:</strong> {basemap}</span>
            </div>
            <div class="legend-item">
                <div style="width: 8px; height: 8px; background-color: #10b981; border-radius: 50%; margin-right: 10px;"></div>
                <span><strong>Opacity:</strong> {opacity}</span>
            </div>
            <div class="legend-item">
                <div style="width: 8px; height: 8px; background-color: #f59e0b; border-radius: 50%; margin-right: 10px;"></div>
                <span><strong>Zoom Level:</strong> {zoom_level}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Map Legends
        st.markdown("#### Map Legends")
        
        if wsi_active:
            st.markdown("**WSI (Water Scarcity)**")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("""
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="width: 20px; height: 20px; background-color: #00FF00; margin-right: 8px; border-radius: 3px;"></div>
                    <span>Low (1)</span>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="width: 20px; height: 20px; background-color: #FFFF00; margin-right: 8px; border-radius: 3px;"></div>
                    <span>Moderate (2)</span>
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                st.markdown("""
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="width: 20px; height: 20px; background-color: #FFA500; margin-right: 8px; border-radius: 3px;"></div>
                    <span>Severe (3)</span>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="width: 20px; height: 20px; background-color: #FF0000; margin-right: 8px; border-radius: 3px;"></div>
                    <span>Extreme (4)</span>
                </div>
                """, unsafe_allow_html=True)
        
        if wdri_active:
            st.markdown("**WDRI (Disease Risk)**")
            st.markdown("""
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="width: 20px; height: 20px; background-color: #00FF00; margin-right: 10px; border-radius: 3px;"></div>
                <span>Low (1)</span>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="width: 20px; height: 20px; background-color: #FFA500; margin-right: 10px; border-radius: 3px;"></div>
                <span>Moderate (2)</span>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="width: 20px; height: 20px; background-color: #FF0000; margin-right: 10px; border-radius: 3px;"></div>
                <span>High (3)</span>
            </div>
            """, unsafe_allow_html=True)
        
        if show_measure:
            st.markdown("---")
            st.markdown("**📏 Measurement Tool**")
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span>Status: <span style="background-color: #fef3c7; color: #92400e; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">ACTIVE</span></span>
                    <span style="font-size: 0.9rem; color: #64748b;">📏</span>
                </div>
                <p style="font-size: 0.85rem; color: #64748b; margin-top: 8px; margin-bottom: 0;">Click and drag to measure distances on the map</p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 0.9rem;">
        <p>WDRI/WSI Map Viewer • Lucy Kamau-PhD • 2025</p>
    </div>
    """,
    unsafe_allow_html=True

)


