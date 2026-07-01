import pandas as pd
import streamlit as st

from config import SAMPLE_DATA_PATH
from geometry import calculate_geometry_metrics
from optics import analyze_optics
from optimizer import optimize_design
from scoring import score_design
from visualization import plot_design_performance


@st.cache_data
def load_design_data(path):
    return pd.read_csv(path)


def main():
    st.set_page_config(page_title="Diamond AI Platform", layout="wide")
    st.title("Diamond AI Platform")
    st.caption("A compact design assistant for diamond optics and geometry exploration.")

    df = load_design_data(SAMPLE_DATA_PATH)

    st.sidebar.header("Design Controls")
    facet_angle = st.sidebar.slider("Facet angle", 20.0, 80.0, 45.0, 0.5)
    surface_quality = st.sidebar.slider("Surface quality", 0.1, 1.0, 0.8, 0.01)
    thickness = st.sidebar.slider("Thickness", 1.0, 10.0, 4.5, 0.1)
    cut_depth = st.sidebar.slider("Cut depth", 0.1, 3.0, 1.2, 0.1)

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

    col1, col2, col3 = st.columns(3)
    col1.metric("Overall score", f"{score:.1f}/100")
    col2.metric("Estimated brilliance", f"{optics['brilliance']:.2f}")
    col3.metric("Suggested angle", f"{optimized['suggested_angle']:.1f}°")

    st.subheader("Design summary")
    st.dataframe(pd.DataFrame([design, optimized]), use_container_width=True)

    st.subheader("Performance chart")
    fig = plot_design_performance(geometry, optics, score)
    st.pyplot(fig)

    st.subheader("Sample design set")
    st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()
