import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_design_performance(geometry, optics, score):
    labels = ["Symmetry", "Balance", "Brilliance"]
    values = [geometry.get("symmetry", 0), geometry.get("balance", 0), optics.get("brilliance", 0)]

    fig, ax = plt.subplots(figsize=(6, 3), dpi=80)
    ax.bar(labels, values, color=["#4f46e5", "#06b6d4", "#f59e0b"])
    ax.set_ylim(0, 1.0)
    ax.set_title(f"Design score: {score:.1f}/100")
    ax.set_ylabel("Normalized value")
    fig.tight_layout()
    return fig
