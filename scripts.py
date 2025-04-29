import numpy as np
import plotly.graph_objects as go
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d, splrep, splev
import seaborn as sns


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


def get_and_plot_interpolated_for_new_n(t, t_new, values):
    # Crear interpolación lineal
    interpolacion_lineal = interp1d(t, values)
    values_interp_lineal = interpolacion_lineal(t_new)

    # Interpolación cúbica (spline en R)
    spline_params = splrep(t, values)
    values_interp_cubica = splev(t_new, spline_params)
    plt.figure(figsize=(12, 8))

    sns.lineplot(x=t, y=values, label='Original', color='black', linestyle='-', linewidth=1)
    plt.scatter(t, values, color='black', s=10)

    sns.lineplot(x=t_new, y=values_interp_lineal, color='red', label='Lineal (approx)', linestyle='--')
    plt.scatter(t_new, values_interp_lineal, color='red', s=5)

    sns.lineplot(x=t_new, y=values_interp_cubica, color='orange', label='Spline cúbico', linestyle='--')
    plt.scatter(t_new, values_interp_cubica, color='orange', s=5)

    plt.title('Valores originales y nueva frecuencia de muestreo')
    plt.xlabel('Días')
    plt.ylabel('Valores')
    plt.legend()
    plt.grid(True)
    plt.show()

    return values_interp_lineal, values_interp_cubica


def fft_interpoladas_y_original(t, t_new, y, y_lin, y_cub):
    # Si t_new tiene una longitud diferente a t, ajustar las señales a la longitud de t
    if len(t_new) != len(t):
        # Interpolamos las señales en la malla de tiempos original t
        y_lin = np.interp(t, t_new, y_lin)  # Reajustar la señal lineal
        y_cub = np.interp(t, t_new, y_cub)  # Reajustar la señal cúbica

    # Realizar FFT de cada señal
    Y = np.fft.fft(y)
    Y_lin = np.fft.fft(y_lin)
    Y_cub = np.fft.fft(y_cub)

    # Calcular las frecuencias asociadas a la señal original
    fs = 1 / (t[1] - t[0])  # Frecuencia de muestreo (asumido que t es uniforme)
    freqs_original = np.fft.fftfreq(len(t), d=(t[1] - t[0]))

    # Calcular el espectro de amplitud (modulo de la FFT)
    amplitude_Y = np.abs(Y)
    amplitude_Y_lin = np.abs(Y_lin)
    amplitude_Y_cub = np.abs(Y_cub)

    # Graficar los espectros de las señales
    plt.figure(figsize=(10, 6))

    # Espectro de la señal original
    plt.plot(freqs_original[:len(freqs_original) // 2], amplitude_Y[:len(freqs_original) // 2], label="Original",
             color="black")

    # Espectro de la señal interpolada linealmente
    plt.plot(freqs_original[:len(freqs_original) // 2], amplitude_Y_lin[:len(freqs_original) // 2],
             label="Interpolada Lineal", color="red")

    # Espectro de la señal interpolada cúbicamente
    plt.plot(freqs_original[:len(freqs_original) // 2], amplitude_Y_cub[:len(freqs_original) // 2],
             label="Interpolada Cúbica", color="orange")

    # Configuración del gráfico
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Amplitud')
    plt.title('FFT de las señales: Original, Lineal y Cúbica')
    plt.legend()
    plt.grid(True)
    plt.show()
