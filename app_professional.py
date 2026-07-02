"""
Professional Diamond Grading Platform - GIA-like System
Enhanced Streamlit interface with advanced parameters and 3D visualization
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go

from parameters import DiamondParameters, OpticalMetrics
from optics_advanced import DiamondOpticsCalculator, assess_cut_grade
from ml_models import DiamondGradingModel, MarketValuePredictor
from visualization_3d import Diamond3DVisualizer, create_comparison_view
from data_pipeline import DataPreprocessor, DiamondDataGenerator


# Page configuration
st.set_page_config(
    page_title="Professional Diamond Grading Platform",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .grade-excellent {
        background-color: #00AA00;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .grade-very-good {
        background-color: #66BB6A;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .grade-good {
        background-color: #FDD835;
        color: black;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .grade-fair {
        background-color: #FB8C00;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_ml_model():
    """Load or create ML model"""
    model = DiamondGradingModel()
    
    # Generate training data if model not exists
    if model.model is None:
        st.info("⚠️ Training ML model on synthetic data...")
        df, grades = DiamondDataGenerator.generate_synthetic_dataset(n_samples=3000)
        
        # Prepare features
        feature_cols = [
            'table_percent', 'total_depth_percent', 'crown_angle', 'pavilion_angle',
            'crown_height', 'pavilion_depth', 'star_length', 'lower_half_length',
            'girdle_thickness_min', 'girdle_thickness_max', 'polish', 'symmetry',
            'painting_digging', 'carat_weight'
        ]
        X = df[feature_cols].values
        model.train(X, grades.values)
        st.success("✅ ML model trained successfully!")
    
    return model


def main():
    st.title("💎 Professional Diamond Grading Platform")
    st.markdown("*Advanced GIA-like Diamond Assessment System*")
    
    # Load ML model
    ml_model = load_ml_model()
    market_predictor = MarketValuePredictor()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Assessment",
        "📈 Comparison",
        "3️⃣ 3D Visualization",
        "🤖 ML Prediction",
        "📚 Database"
    ])
    
    # ============== TAB 1: ASSESSMENT ==============
    with tab1:
        st.header("Diamond Assessment")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📐 Geometric Parameters")
            
            table_percent = st.slider(
                "Table %",
                min_value=43.0, max_value=65.0, value=55.0, step=0.1,
                help="Optimal range: 52-58%"
            )
            
            total_depth_percent = st.slider(
                "Total Depth %",
                min_value=58.0, max_value=66.0, value=61.5, step=0.1,
                help="Optimal range: 60-63%"
            )
            
            crown_angle = st.slider(
                "Crown Angle (°)",
                min_value=30.0, max_value=36.0, value=33.5, step=0.1,
                help="Optimal: 33-34°"
            )
            
            pavilion_angle = st.slider(
                "Pavilion Angle (°)",
                min_value=38.0, max_value=42.0, value=40.75, step=0.1,
                help="Optimal: 40.75-41°"
            )
            
            crown_height = st.slider(
                "Crown Height % of Table",
                min_value=7.4, max_value=20.8, value=14.0, step=0.1
            )
            
            pavilion_depth = st.slider(
                "Pavilion Depth % of Depth",
                min_value=42.0, max_value=44.0, value=43.3, step=0.1
            )
        
        with col_right:
            st.subheader("✨ Facet Ratios & Quality")
            
            star_length = st.slider(
                "Star Length % of Table",
                min_value=40.0, max_value=65.0, value=50.0, step=1.0,
                help="Optimal: 45-60%"
            )
            
            lower_half_length = st.slider(
                "Lower Half Length % of Star",
                min_value=70.0, max_value=80.0, value=75.0, step=1.0
            )
            
            girdle_min = st.slider(
                "Girdle Thickness Min %",
                min_value=0.5, max_value=1.5, value=1.0, step=0.1
            )
            
            girdle_max = st.slider(
                "Girdle Thickness Max %",
                min_value=1.5, max_value=3.5, value=2.5, step=0.1
            )
            
            culet_size = st.selectbox(
                "Culet Size",
                ["none", "pointed", "very_small", "small", "medium", "large", "very_large"]
            )
            
            polish = st.select_slider(
                "Polish Grade",
                options=[1, 2, 3, 4, 5],
                value=1,
                help="1=Excellent, 5=Poor"
            )
            
            symmetry = st.select_slider(
                "Symmetry Grade",
                options=[1, 2, 3, 4, 5],
                value=1,
                help="1=Excellent, 5=Poor"
            )
            
            painting_digging = st.select_slider(
                "Painting/Digging",
                options=[0, 1, 2, 3, 4, 5],
                value=0
            )
        
        # 4Cs and Additional Info
        st.divider()
        col_4c1, col_4c2, col_4c3, col_4c4 = st.columns(4)
        
        with col_4c1:
            carat_weight = st.number_input("Carat Weight", min_value=0.1, value=1.0, step=0.1)
        
        with col_4c2:
            color_grade = st.selectbox("Color Grade", list("DEFGHIJKLMNOPQRSTUVWXYZ"))
        
        with col_4c3:
            clarity_grade = st.selectbox(
                "Clarity Grade",
                ["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I1", "I2", "I3"]
            )
        
        with col_4c4:
            fluorescence = st.selectbox(
                "Fluorescence",
                ["None", "Faint", "Medium", "Strong", "Very Strong"]
            )
        
        # Create parameters object
        params = DiamondParameters(
            table_percent=table_percent,
            total_depth_percent=total_depth_percent,
            crown_angle=crown_angle,
            pavilion_angle=pavilion_angle,
            crown_height=crown_height,
            pavilion_depth=pavilion_depth,
            star_length=star_length,
            lower_half_length=lower_half_length,
            girdle_thickness_min=girdle_min,
            girdle_thickness_max=girdle_max,
            culet_size=culet_size,
            polish=polish,
            symmetry=symmetry,
            painting_digging=painting_digging,
            carat_weight=carat_weight,
            color_grade=color_grade,
            clarity_grade=clarity_grade,
            fluorescence=fluorescence,
        )
        
        # Calculate metrics
        calculator = DiamondOpticsCalculator(params)
        metrics = calculator.calculate_all_metrics()
        cut_grade = assess_cut_grade(metrics, params)
        
        # Display Results
        st.divider()
        st.header("📊 Assessment Results")
        
        col_r1, col_r2, col_r3, col_r4, col_r5 = st.columns(5)
        
        with col_r1:
            st.metric("Overall Score", f"{metrics.overall_score():.1f}/100")
        
        with col_r2:
            grade_color = {
                'Excellent': 'green',
                'Very Good': 'lightgreen',
                'Good': 'orange',
                'Fair': 'darkorange',
                'Poor': 'red'
            }
            st.metric("Cut Grade", cut_grade)
        
        with col_r3:
            st.metric("Light Return", f"{metrics.light_return:.1f}%")
        
        with col_r4:
            st.metric("Fire (Dispersion)", f"{metrics.fire_dispersion:.1f}%")
        
        with col_r5:
            st.metric("Scintillation", f"{metrics.scintillation:.1f}%")
        
        # Detailed metrics
        metrics_col1, metrics_col2 = st.columns(2)
        
        with metrics_col1:
            st.subheader("Optical Metrics")
            metrics_data = {
                'Metric': ['Light Return', 'Fire/Dispersion', 'Scintillation', 'Contrast Pattern', 'Leakage', 'Brightness'],
                'Value': [
                    f"{metrics.light_return:.1f}%",
                    f"{metrics.fire_dispersion:.1f}%",
                    f"{metrics.scintillation:.1f}%",
                    f"{metrics.contrast_pattern:.1f}%",
                    f"{metrics.leakage:.1f}%",
                    f"{metrics.brightness:.1f}%",
                ]
            }
            st.dataframe(pd.DataFrame(metrics_data), use_container_width=True)
        
        with metrics_col2:
            st.subheader("Market Value Estimate")
            value_estimate = market_predictor.estimate_price(params, cut_grade)
            price_data = {
                'Category': ['Per Carat', 'Total Value', 'Currency'],
                'Amount': [
                    f"${value_estimate['price_per_carat']:,.0f}",
                    f"${value_estimate['total_price']:,.0f}",
                    value_estimate['currency']
                ]
            }
            st.dataframe(pd.DataFrame(price_data), use_container_width=True)
        
        # Validation
        is_valid, issues = DataPreprocessor.validate_parameters(params)
        if not is_valid:
            st.warning(f"⚠️ Parameter Issues:\n" + "\n".join(f"• {issue}" for issue in issues))
        else:
            st.success("✅ All parameters within GIA specifications")
    
    # ============== TAB 2: COMPARISON ==============
    with tab2:
        st.header("Compare Two Diamonds")
        
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.subheader("Diamond 1 (Current)")
            d1_table = st.slider("Diamond 1 - Table %", 43.0, 65.0, 55.0, key="d1_table")
            d1_depth = st.slider("Diamond 1 - Depth %", 58.0, 66.0, 61.5, key="d1_depth")
            d1_crown = st.slider("Diamond 1 - Crown Angle", 30.0, 36.0, 33.5, key="d1_crown")
            d1_pavilion = st.slider("Diamond 1 - Pavilion Angle", 38.0, 42.0, 40.75, key="d1_pavilion")
        
        with col_c2:
            st.subheader("Diamond 2 (Comparison)")
            d2_table = st.slider("Diamond 2 - Table %", 43.0, 65.0, 54.0, key="d2_table")
            d2_depth = st.slider("Diamond 2 - Depth %", 58.0, 66.0, 61.0, key="d2_depth")
            d2_crown = st.slider("Diamond 2 - Crown Angle", 30.0, 36.0, 34.0, key="d2_crown")
            d2_pavilion = st.slider("Diamond 2 - Pavilion Angle", 38.0, 42.0, 40.5, key="d2_pavilion")
        
        params1 = DiamondParameters(
            table_percent=d1_table, total_depth_percent=d1_depth,
            crown_angle=d1_crown, pavilion_angle=d1_pavilion,
            crown_height=14.0, pavilion_depth=43.3, star_length=50.0,
            lower_half_length=75.0, girdle_thickness_min=1.0,
            girdle_thickness_max=2.5, culet_size="small",
            polish=1, symmetry=1, painting_digging=0,
            carat_weight=1.0, color_grade="E", clarity_grade="VS1",
            fluorescence="None"
        )
        
        params2 = DiamondParameters(
            table_percent=d2_table, total_depth_percent=d2_depth,
            crown_angle=d2_crown, pavilion_angle=d2_pavilion,
            crown_height=14.0, pavilion_depth=43.3, star_length=50.0,
            lower_half_length=75.0, girdle_thickness_min=1.0,
            girdle_thickness_max=2.5, culet_size="small",
            polish=1, symmetry=1, painting_digging=0,
            carat_weight=1.0, color_grade="E", clarity_grade="VS1",
            fluorescence="None"
        )
        
        fig = create_comparison_view(params1, params2)
        st.plotly_chart(fig, use_container_width=True)
    
    # ============== TAB 3: 3D VISUALIZATION ==============
    with tab3:
        st.header("3D Diamond Visualization")
        
        visualizer = Diamond3DVisualizer(params)
        
        col_3d1, col_3d2 = st.columns(2)
        
        with col_3d1:
            st.subheader("3D Facet Structure")
            fig_3d = visualizer.create_3d_plot()
            st.plotly_chart(fig_3d, use_container_width=True)
        
        with col_3d2:
            st.subheader("Proportions Profile")
            fig_profile = visualizer.create_facet_diagram()
            st.plotly_chart(fig_profile, use_container_width=True)
    
    # ============== TAB 4: ML PREDICTION ==============
    with tab4:
        st.header("🤖 ML-Based Prediction")
        
        try:
            ml_score, confidence_info = ml_model.predict(params)
            
            col_ml1, col_ml2 = st.columns(2)
            
            with col_ml1:
                st.metric("ML Predicted Score", f"{ml_score:.1f}/100")
                st.info(f"**Model Type:** {confidence_info['model_type']}")
            
            with col_ml2:
                st.subheader("Top Contributing Factors")
                for factor in confidence_info['top_factors']:
                    st.write(f"• {factor}")
        
        except Exception as e:
            st.error(f"Error in ML prediction: {e}")
    
    # ============== TAB 5: DATABASE ==============
    with tab5:
        st.header("💾 Diamond Database")
        
        col_db1, col_db2 = st.columns(2)
        
        with col_db1:
            if st.button("📥 Generate Synthetic Dataset (5000 diamonds)"):
                with st.spinner("Generating dataset..."):
                    df, _ = DiamondDataGenerator.generate_synthetic_dataset(n_samples=5000)
                    st.dataframe(df, use_container_width=True)
                    
                    # Download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="diamond_dataset.csv",
                        mime="text/csv"
                    )
        
        with col_db2:
            st.info("**Dataset Information:**\n- 5000+ synthetic diamond records\n- Based on GIA standards\n- Includes all 57-facet parameters")


if __name__ == "__main__":
    main()
