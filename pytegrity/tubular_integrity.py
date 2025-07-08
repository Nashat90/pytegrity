import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.express as px
import pandas as pd


def plot_well_integrity(las_file_as_df: pd.DataFrame, fingers: list,
                        plotly_template="plotly_dark", height=1500, width=1000):
    """
    Generates a comprehensive interactive visualization of well integrity data
    using multiple Plotly subplots.

    Parameters
    ----------
    las_file_as_df : pd.DataFrame
        A dataframe representing the LAS file, containing logging data per depth.
        Must include a "GR" column (Gamma Ray) and finger log curves.
        
    fingers : list of str
        A list of column names (as strings) representing finger tool measurements.

    plotly_template : str, optional
        Plotly template to use for layout and color theme. Default is 'plotly_dark'.

    height : int, optional
        Height of the resulting figure in pixels. Default is 1500.

    width : int, optional
        Width of the resulting figure in pixels. Default is 1000.

    Returns
    -------
    fig : plotly.graph_objs._figure.Figure
        A Plotly figure containing:
        - GR log curve
        - Min, Max, Avg statistical curves for selected fingers
        - Overlaid finger logs as line traces (like seismic display)
        - 2D colored heatmap of finger values (depth vs. finger)

    Notes
    -----
    - Y-axis is reversed to reflect depth-based display.
    - Intended for well integrity diagnostics and quick multi-log inspection.
    - Supports thousands of data points with optimized rendering (Scattergl).
    """
    data = las_file_as_df
    fing = fingers

    fig = make_subplots(
        rows=1, cols=4,
        subplot_titles=("GR", "Statistics", "Fing/Pad", "2D Map"),
        horizontal_spacing=0.001,
        shared_yaxes=True
    )

    n_traces = len(fing)
    time = data.index
    trace_spacing = 1  # horizontal spacing between traces

    # Plot finger logs as shifted line traces (like seismic-style wiggles)
    for i in range(n_traces):
        trace_data = data[fing[i]]
        x = trace_data + i * (trace_spacing * 0.2)
        fig.add_trace(go.Scattergl(
            x=x,
            y=list(range(len(data))),
            mode='lines',
            line=dict(color='blue', width=1),
            showlegend=False,
            name=fing[i]
        ), 1, 3)

    # Flip Y-axis globally
    fig.update_layout(
        yaxis=dict(autorange='reversed'),
        title='Well Integrity Tool Plot',
        yaxis_title='Depth',
        height=height,
        width=width
    )

    # Prepare 2D matrix for heatmap
    trace_matrix = data[fing].to_numpy().T
    trace_matrix = trace_matrix.T

    map2d = px.imshow(
        trace_matrix,
        labels=dict(x="Readings", y="Depth", color="Amplitude"),
        aspect="auto",
        origin="upper",
        color_continuous_scale='Turbo'
    )

    # Plot statistical curves (Min, Max, Avg)
    min_curve = go.Line(x=data[fing].min(1), y=list(range(len(time))), name="Minimum", line_width=.51)
    max_curve = go.Line(x=data[fing].max(1), y=list(range(len(time))), name="Maximum", line_width=.51)
    avg_curve = go.Line(x=data[fing].mean(1), y=list(range(len(time))), name="Average", line_width=.51)
    gr = go.Line(x=data["GR"], y=list(range(len(time))), line_color="green", name="GR", line_width=.5)

    fig.add_traces([min_curve, max_curve, avg_curve], rows=1, cols=2)
    fig.add_trace(gr, 1, 1)
    fig.add_trace(map2d.data[0], row=1, col=4)

    fig.update_yaxes(
        tickvals=np.linspace(0, len(time), 10),
        ticktext=np.round(np.linspace(time.min(), time.max(), 10), 2),
        autorange="reversed",
        row=1, col=3
    )

    fig.update_layout(
        template=plotly_template,
        font=dict(family="Arial, sans-serif", size=9),
        legend=dict(x=1.01, y=1, traceorder='normal'),
        margin=dict(r=110,t=40),
        coloraxis_colorbar=dict(x=1, y=0.5, len=0.6)
    )

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

    fig.update_yaxes(
        tickvals=np.linspace(0, len(data.index) - 1, 10),
        ticktext=np.round(np.linspace(data.index.min(), data.index.max(), 10), 2),
        autorange="reversed",
        row=1, col=1
    )

    fig.update_layout(
        coloraxis=dict(colorscale='Turbo'),
        hovermode='closest'
    )

    for axis_name in fig.layout:
        if axis_name.startswith('xaxis') or axis_name.startswith('yaxis'):
            axis = fig.layout[axis_name]
            axis.showspikes = True
            axis.spikecolor = 'grey'
            axis.spikethickness = 1
            axis.spikesnap = 'cursor'
            axis.spikemode = 'across+marker'
            axis.spikedash = 'solid'

    return fig
