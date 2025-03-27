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

def plot_time_series_multiple_y(x, y_dict, title="", x_label="Time", y_label="Values", markers=True):
    fig = go.Figure()

    for label, y_values in y_dict.items():
        fig.add_trace(go.Scatter(
            x=x,
            y=y_values,
            mode=f'lines{'+markers' if markers else ''}',
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


def plot_boxplots(x, y, title="", x_label="Time", y_label="Values"):
    """
    Function to plot boxplots using Plotly for average temperatures across multiple years.

    Parameters:
    x (list): List of months to be displayed on the x-axis (e.g., ['Jan', 'Feb', ...])
    y (list): List of temperature data, where each element is a list of temperatures for a given month across years.
    """
    # Create the boxplot data
    boxplot_data = []

    # Populate the boxplot data for each month
    for i, month in enumerate(x):
        boxplot_data.append(go.Box(
            y=y[i],
            name=month,
            boxmean='sd',  # Show the standard deviation in the box plot (can be adjusted to other options)
            #jitter=0.5,  # Adds jitter to separate the points a little
            pointpos=0,  # Controls the position of individual points
            width=0.6,
        ))

    # Create the layout for the plot
    layout = go.Layout(
        title=title,
        xaxis=dict(title=x_label),
        yaxis=dict(title=y_label),
        boxmode='group',  # To group the boxplots by month
        height=1000,
    )

    # Create the figure and display it
    fig = go.Figure(data=boxplot_data, layout=layout)
    fig.show()
