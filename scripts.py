import plotly.graph_objects as go

def plot_time_series(x, y, title="", x_label="Time", y_label="Values"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name='Data',
        hovertemplate=f'{x_label}: %{{x}}<br>{y_label}: %{{y}}'
    ))

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        template="seaborn",
        legend_title="Legend"
    )

    fig.show()

def plot_time_series_multiple_y(x, y_dict, title="", x_label="Time", y_label="Values"):
    fig = go.Figure()

    for label, y_values in y_dict.items():
        fig.add_trace(go.Scatter(
            x=x,
            y=y_values,
            mode='lines+markers',
            name=label,  # Use the dictionary key as the series name
            hovertemplate=f'{x_label}: %{{x}}<br>{label}: %{{y}}'
        ))

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        template="seaborn",
        legend_title="Legend"
    )

    fig.show()
