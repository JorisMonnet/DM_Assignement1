import matplotlib.pyplot as plt


def plot_timing_as_tempo_curve(tempo_map: dict):
    """
    Plot the tempo curve from the dict of tempo ratios
    :param tempo_map: dict
    :return: None
    """
    fig, ax = plt.subplots()
    ax.plot(list(tempo_map.keys()), list(tempo_map.values()))
    ax.set(xlabel='Beats', ylabel='Tempo Ratio',
           title='Tempo curve')
    ax.grid()
    plt.show()
