from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SAMPLE_DATA_PATH = PROJECT_ROOT / "data" / "sample_design.csv"

DEFAULT_DESIGN = {
    "facet_angle": 45.0,
    "surface_quality": 0.8,
    "thickness": 4.5,
    "cut_depth": 1.2,
}
