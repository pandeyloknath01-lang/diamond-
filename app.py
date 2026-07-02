import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from config import SAMPLE_DATA_PATH
from geometry import calculate_geometry_metrics
from optics import analyze_optics
from optimizer import optimize_design
from scoring import score_design
from visualization import plot_design_performance


@st.cache_data
def load_design_data(path):
    return pd.read_csv(path)


def create_comparison_chart(geometry, optics):
    """Create a radar/comparison chart for design metrics."""
    fig, ax = plt.subplots(figsize=(7, 5))
    
    metrics = ['Symmetry', 'Balance', 'Brilliance', 'Surface Quality']
    values = [
        geometry.get("symmetry", 0),
        geometry.get("balance", 0),
        optics.get("brilliance", 0),
        optics.get("surface_quality", 0)
    ]
    
    colors = ['#4f46e5', '#06b6d4', '#f59e0b', '#ec4899']
    bars = ax.barh(metrics, values, color=colors)
    ax.set_xlim(0, 1.0)
    ax.set_xlabel('Normalized Value')
    ax.set_title('Diamond Design Metrics', fontweight='bold', fontsize=12)
    
    for i, (bar, value) in enumerate(zip(bars, values)):
        ax.text(value + 0.02, i, f'{value:.2f}', va='center', fontweight='bold')
    
    fig.tight_layout()
    return fig


def main():
    # Page config
    st.set_page_config(
        page_title="Diamond AI Platform",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom styling
    st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title and description
    st.title("💎 Diamond AI Platform")
    st.markdown("*A compact design assistant for diamond optics and geometry exploration*")
    
    # Load data
    df = load_design_data(SAMPLE_DATA_PATH)
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Design Controls")
        st.markdown("---")
        
        facet_angle = st.slider(
            "Facet Angle (°)",
            min_value=20.0,
            max_value=80.0,
            value=45.0,
            step=0.5,
            help="The angle of diamond facets affects brilliance"
        )
        
        surface_quality = st.slider(
            "Surface Quality",
            min_value=0.1,
            max_value=1.0,
            value=0.8,
            step=0.01,
            help="Higher values indicate better polish"
        )
        
        thickness = st.slider(
            "Thickness (mm)",
            min_value=1.0,
            max_value=10.0,
            value=4.5,
            step=0.1,
            help="Diamond thickness in millimeters"
        )
        
        cut_depth = st.slider(
            "Cut Depth (mm)",
            min_value=0.1,
            max_value=3.0,
            value=1.2,
            step=0.1,
            help="Depth of the diamond cut"
        )
        
        st.markdown("---")
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.rerun()

    # Calculate metrics
    design = {
        "facet_angle": facet_angle,
        "surface_quality": surface_quality,
        "thickness": thickness,
        "cut_depth": cut_depth,
    }

    geometry = calculate_geometry_metrics(design)
    optics = analyze_optics(design)
    score = score_design(geometry, optics)
    optimized = optimize_design(geometry, optics, score)

    # Main metrics display
    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall Score",
            f"{score:.1f}/100",
            delta=f"{score - 75:.1f}" if score >= 75 else f"{score - 75:.1f}",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            "Brilliance",
            f"{optics['brilliance']:.3f}",
            help="Light reflection quality"
        )
    
    with col3:
        st.metric(
            "Dispersion",
            f"{optics['dispersion']:.3f}",
            help="Color separation quality"
        )
    
    with col4:
        st.metric(
            "Suggested Angle",
            f"{optimized['suggested_angle']:.1f}°",
            help="Optimal facet angle"
        )

    # Two-column layout for detailed info
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📈 Current Design")
        design_df = pd.DataFrame([design]).T
        design_df.columns = ["Value"]
        st.dataframe(design_df, use_container_width=True)
        
        st.subheader("✨ Geometry Metrics")
        geometry_df = pd.DataFrame([geometry]).T
        geometry_df.columns = ["Value"]
        st.dataframe(geometry_df, use_container_width=True)
    
    with col_right:
        st.subheader("🎯 Optimization Recommendations")
        rec_df = pd.DataFrame([optimized]).T
        rec_df.columns = ["Recommended Value"]
        st.dataframe(rec_df, use_container_width=True)
        
        st.subheader("🔬 Optical Properties")
        optics_df = pd.DataFrame([optics]).T
        optics_df.columns = ["Value"]
        st.dataframe(optics_df, use_container_width=True)

    # Visualizations
    st.markdown("---")
    st.subheader("📉 Performance Visualization")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        fig1 = plot_design_performance(geometry, optics, score)
        st.pyplot(fig1)
        plt.close(fig1)
    
    with viz_col2:
        fig2 = create_comparison_chart(geometry, optics)
        st.pyplot(fig2)
        plt.close(fig2)

    # Data comparison section
    st.markdown("---")
    st.subheader("📋 Sample Design Dataset")
    
    if st.checkbox("Show full dataset", value=False):
        st.dataframe(df, use_container_width=True)
    
    # Summary statistics
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        st.metric("Total samples", len(df))
    with col_stats2:
        st.metric("Avg score", f"{df['estimated_score'].mean():.1f}")
    with col_stats3:
        st.metric("Max score", f"{df['estimated_score'].max():.1f}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p style='color: #888; font-size: 12px;'>
            Diamond AI Platform v1.0 | Powered by Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    from app_professional import main as professional_main
    professional_main()
