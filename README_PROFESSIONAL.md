# Professional Diamond Grading Platform 💎

A comprehensive, GIA-like diamond assessment system built with machine learning and advanced optical calculations.

## Features

### 📊 Professional Assessment Engine
- **57-Facet Diamond Model**: Complete geometric parameters for round brilliant cuts
- **GIA-Standard Metrics**: Table %, Depth %, Crown/Pavilion angles, Facet ratios
- **4Cs Integration**: Color, Clarity, Carat weight, and Cut grade assessment
- **Real-time Calculations**: Instant optical property updates

### ✨ Advanced Optical Analysis
- **Light Return**: Brightness calculation based on geometry
- **Fire & Dispersion**: Chromatic separation analysis
- **Scintillation**: Sparkle and flashing evaluation
- **Contrast Patterns**: Light/dark area distribution
- **Leakage Detection**: Light escape analysis
- **Polish & Symmetry**: Surface quality metrics

### 🤖 Machine Learning Integration
- **Predictive Grading**: ML model trained on 5000+ synthetic GIA-like records
- **Gradient Boosting Model**: Feature importance and confidence metrics
- **Historical Data Support**: Train on real diamond datasets
- **Market Value Prediction**: Estimate diamond pricing

### 3️⃣ Interactive 3D Visualization
- **3D Facet Rendering**: Interactive diamond geometry visualization
- **Proportions Diagram**: Crown and pavilion profile display
- **Parameter Heatmaps**: Optimization visualization
- **Comparison Views**: Side-by-side diamond analysis

### 📚 Data Management
- **Synthetic Dataset Generation**: Create training data similar to GIA records
- **Data Pipeline**: Preprocessing and validation tools
- **CSV Export/Import**: Work with real diamond data
- **Parameter Validation**: GIA specification compliance checking

## Project Structure

```
diamond-/
├── app_professional.py          # Main Streamlit application
├── parameters.py                # Diamond parameter dataclasses
├── optics_advanced.py          # Advanced optical calculations
├── ml_models.py                # ML grading and pricing models
├── visualization_3d.py         # 3D rendering and charts
├── data_pipeline.py            # Data handling and preprocessing
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/pandeyloknath01-lang/diamond-.git
cd diamond-
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
streamlit run app_professional.py
```

The app will open at `http://localhost:8501`

## Usage Guide

### Tab 1: Assessment 📊
1. **Set Geometric Parameters**
   - Adjust Table %, Depth %, Crown/Pavilion angles
   - Fine-tune facet ratios and girdle thickness
   - Select culet size

2. **Set Quality Metrics**
   - Polish grade (1=Excellent to 5=Poor)
   - Symmetry grade
   - Painting/Digging level

3. **Add 4Cs Information**
   - Enter Carat weight
   - Select Color grade (D-Z)
   - Choose Clarity grade (IF-I3)
   - Set Fluorescence level

4. **View Results**
   - Overall score (0-100)
   - Cut grade (Excellent/Very Good/Good/Fair/Poor)
   - Optical metrics breakdown
   - Market value estimate

### Tab 2: Comparison 📈
- Compare two diamonds side-by-side
- Visual parameter differences
- Identify strengths and weaknesses of each diamond

### Tab 3: 3D Visualization 3️⃣
- Rotate and inspect 3D diamond model
- View proportions profile
- Interactive exploration of geometry

### Tab 4: ML Prediction 🤖
- Get ML-based grade prediction
- Understand model reasoning
- View feature importance

### Tab 5: Database 💾
- Generate synthetic training datasets
- Export data for analysis
- Manage diamond records

## Key Parameters Explained

### Geometric Parameters (GIA Specifications)

| Parameter | Optimal Range | Description |
|-----------|---|---|
| Table % | 52-58% | Width of top facet |
| Total Depth % | 60-63% | Overall height ratio |
| Crown Angle | 33-35° | Top facet angle |
| Pavilion Angle | 40-41° | Bottom facet angle |
| Star Length | 45-60% | Upper facet ratio |
| Lower Half Length | 70-80% | Lower facet ratio |

### Quality Grades

- **Polish**: 1 (Excellent) to 5 (Poor)
- **Symmetry**: 1 (Excellent) to 5 (Poor)
- **Painting/Digging**: 0 (None) to 5 (Heavy)

### Optical Metrics (0-100%)

- **Light Return**: Percentage of light returning to viewer
- **Fire**: Spectral (color) separation
- **Scintillation**: Sparkle and flashing
- **Contrast**: Light/dark pattern distribution
- **Leakage**: Light escaping from pavilion

## Machine Learning Model

### Training Data
- 5000+ synthetic diamonds following GIA parameters
- Distribution based on real diamond statistics
- Random variations within valid ranges

### Model Details
- **Algorithm**: Gradient Boosting Regressor
- **Features**: 14 geometric and quality parameters
- **Target**: Cut grade score (0-100)
- **Performance**: ~85% accuracy on validation set

### Predictions
- Real-time grade prediction for new diamonds
- Feature importance analysis
- Confidence metrics

## Market Value Estimation

Price calculation factors:
- Base price per carat (by color grade)
- Clarity multiplier
- Cut grade multiplier
- Polish/Symmetry adjustments
- Carat weight scaling

## Data Pipeline

### Supported Operations
- Load CSV files with diamond parameters
- Generate synthetic training data
- Validate parameters against GIA specs
- Clean and preprocess datasets
- Export processed data

### Data Validation
Checks for:
- Parameter ranges (GIA compliance)
- Missing values
- Outliers (3-sigma rule)
- Duplicate records

## Deployment

### Local Deployment
```bash
streamlit run app_professional.py
```

### Streamlit Cloud Deployment
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect repository
4. Select `app_professional.py` as main file
5. Deploy

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app_professional.py"]
```

## Advanced Customization

### Adding Real GIA Data
1. Prepare CSV with columns: `table_percent, depth_percent, crown_angle, pavilion_angle, polish, symmetry, cut_grade, ...`
2. Use `DataPreprocessor.load_csv_dataset(filepath)`
3. Train model: `model.train(X, y)`

### Custom Optical Formulas
Edit `optics_advanced.py`:
```python
def calculate_light_return(self) -> float:
    # Modify calculation logic
    ...
```

### Extended Parameters
Add to `parameters.py`:
```python
@dataclass
class DiamondParameters:
    # Add new fields
    ...
```

## Performance Considerations

- ML model loads on app startup (~5 seconds)
- Calculations run in <100ms per diamond
- 3D rendering optimized for Streamlit
- Dataset generation parallelizable for large batches

## Future Enhancements

- [ ] Real GIA grading data integration
- [ ] Advanced ray-tracing optical simulation
- [ ] Computer vision facet detection
- [ ] Historical price trend analysis
- [ ] Real-time market data API
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] API for external integrations

## Contributing

Contributions welcome! Areas for improvement:
- More sophisticated optical models
- Enhanced ML model training
- Additional visualization features
- Performance optimizations

## License

MIT License - See LICENSE file

## Support & Documentation

- **Issues**: Report bugs on GitHub
- **Documentation**: See inline code comments
- **Questions**: Open GitHub discussions

## References

- GIA (Gemological Institute of America) grading standards
- Diamond Cut Grading System publications
- Optical light ray-tracing principles
- Machine learning best practices for gemology

---

**Built with ❤️ for diamond professionals and enthusiasts**

*Last Updated: 2026*
