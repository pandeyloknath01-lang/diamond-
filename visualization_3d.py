"""
3D Diamond visualization module
Interactive 3D rendering of diamond geometry
"""

import plotly.graph_objects as go
import numpy as np
from parameters import DiamondParameters


class Diamond3DVisualizer:
    """Create interactive 3D visualizations of diamond geometry"""
    
    def __init__(self, params: DiamondParameters):
        self.params = params
        self.scale = 10  # Scaling factor for visualization
    
    def generate_facet_coordinates(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate 3D coordinates for diamond facets
        Simplified model of 57-facet round brilliant cut
        """
        vertices = []
        
        # Table (top facet)
        table_radius = self.params.table_percent / 100 * self.scale
        table_height = self.params.crown_height / 100 * self.scale
        
        # Crown facets (8 star facets, 8 upper girdle facets)
        # Pavilion facets (8 lower girdle facets, 8 pavilion facets)
        # Culet facet (bottom point or small facet)
        
        # Simplified: create cone-like structure
        angles = np.linspace(0, 2*np.pi, 17)
        
        # Crown
        for angle in angles[:-1]:
            x = table_radius * np.cos(angle)
            y = table_radius * np.sin(angle)
            z = table_height
            vertices.append([x, y, z])
        
        # Upper girdle
        for angle in angles[:-1]:
            x = self.scale * np.cos(angle)
            y = self.scale * np.sin(angle)
            z = 0
            vertices.append([x, y, z])
        
        # Pavilion (pointed bottom)
        pavilion_depth = self.params.pavilion_depth / 100 * self.scale
        vertices.append([0, 0, -pavilion_depth])
        
        return np.array(vertices)
    
    def create_3d_plot(self) -> go.Figure:
        """Create interactive 3D diamond visualization"""
        
        # Generate diamond coordinates
        vertices = self.generate_facet_coordinates()
        
        # Create surface
        x = vertices[:, 0]
        y = vertices[:, 1]
        z = vertices[:, 2]
        
        # Create convex hull-like structure
        fig = go.Figure(data=[go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers+lines',
            marker=dict(
                size=5,
                color='rgba(100, 200, 255, 0.8)',
                symbol='circle',
            ),
            line=dict(
                color='rgba(50, 100, 200, 0.6)',
                width=2,
            ),
            name='Diamond Facets'
        )])
        
        # Add surface
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers',
            marker=dict(
                size=8,
                color='white',
                symbol='diamond',
            ),
            name='Center'
        ))
        
        fig.update_layout(
            title=f"Diamond 3D Visualization<br>" +
                  f"Table: {self.params.table_percent}% | " +
                  f"Depth: {self.params.total_depth_percent}%",
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z",
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.3)
                )
            ),
            hovermode='closest',
            width=800,
            height=700,
        )
        
        return fig
    
    def create_facet_diagram(self) -> go.Figure:
        """Create 2D proportions diagram"""
        
        # Crown diagram
        fig = go.Figure()
        
        # Draw crown profile
        crown_angles = np.linspace(0, 360, 100)
        crown_radius = self.params.table_percent / 100 * self.scale
        
        crown_x = crown_radius * np.cos(np.radians(crown_angles))
        crown_y = self.params.crown_height / 100 * self.scale * np.ones_like(crown_angles)
        
        fig.add_trace(go.Scatter(
            x=crown_x, y=crown_y,
            mode='lines',
            name='Crown',
            line=dict(color='gold', width=3)
        ))
        
        # Draw table
        table_y = self.params.crown_height / 100 * self.scale
        fig.add_trace(go.Scatter(
            x=[-crown_radius, crown_radius],
            y=[table_y, table_y],
            mode='lines',
            name='Table',
            line=dict(color='blue', width=2, dash='dash')
        ))
        
        # Draw pavilion profile
        pavilion_radius = self.scale
        pavilion_depth = self.params.pavilion_depth / 100 * self.scale
        
        pav_x = [0, pavilion_radius, 0, -pavilion_radius, 0]
        pav_y = [0, -pavilion_depth/2, -pavilion_depth, -pavilion_depth/2, 0]
        
        fig.add_trace(go.Scatter(
            x=pav_x, y=pav_y,
            mode='lines',
            name='Pavilion',
            line=dict(color='purple', width=3)
        ))
        
        fig.update_layout(
            title="Diamond Proportions Profile",
            xaxis_title="Diameter",
            yaxis_title="Height",
            hovermode='closest',
            width=700,
            height=600,
            showlegend=True,
        )
        
        return fig
    
    def create_parameter_heatmap(self, metrics: Dict) -> go.Figure:
        """Create heatmap of parameter variations"""
        
        categories = [
            'Table %',
            'Depth %',
            'Crown °',
            'Pavilion °',
            'Crown Height',
            'Star Length',
        ]
        
        values = [
            self.params.table_percent,
            self.params.total_depth_percent,
            self.params.crown_angle,
            self.params.pavilion_angle,
            self.params.crown_height,
            self.params.star_length,
        ]
        
        # Normalize to 0-100
        normalized = [(v / 100) * 100 for v in values]
        
        fig = go.Figure(data=go.Heatmap(
            z=[normalized],
            x=categories,
            colorscale='RdYlGn',
            showscale=True,
        ))
        
        fig.update_layout(
            title="Parameter Optimization Heatmap",
            xaxis_title="Parameters",
            height=300,
            width=800,
        )
        
        return fig


def create_comparison_view(params1: DiamondParameters, params2: DiamondParameters) -> go.Figure:
    """Compare two diamond designs side-by-side"""
    
    parameters = ['Table %', 'Depth %', 'Crown °', 'Pavilion °', 'Polish', 'Symmetry']
    values1 = [
        params1.table_percent,
        params1.total_depth_percent,
        params1.crown_angle,
        params1.pavilion_angle,
        params1.polish * 20,
        params1.symmetry * 20,
    ]
    values2 = [
        params2.table_percent,
        params2.total_depth_percent,
        params2.crown_angle,
        params2.pavilion_angle,
        params2.polish * 20,
        params2.symmetry * 20,
    ]
    
    fig = go.Figure(data=[
        go.Bar(name='Diamond 1', x=parameters, y=values1, marker_color='rgba(100, 149, 237, 0.7)'),
        go.Bar(name='Diamond 2', x=parameters, y=values2, marker_color='rgba(255, 165, 0, 0.7)'),
    ])
    
    fig.update_layout(
        title="Diamond Comparison",
        barmode='group',
        xaxis_title="Parameters",
        yaxis_title="Value",
        height=500,
        width=900,
    )
    
    return fig
