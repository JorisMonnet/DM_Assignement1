"""
This module contains functions used to plot the results for Task A.

@Author: Joris Monnet
@Date: 2024-03-26
"""

import matplotlib.pyplot as plt
import seaborn as sns


def plot_timing_for_one_piece(tempo_map: dict):
    """
    Plot the tempo curve from the dict of tempo ratios (for one piece) with each beat as x-axis
    :param tempo_map: dict
    :return: None
    """
    fig, ax = plt.subplots()
    ax.plot(list(tempo_map.keys()), list(tempo_map.values()))
    ax.set(xlabel='Beats', ylabel='Tempo Ratio',
           title='Tempo curve')
    plt.grid(True)
    plt.show()


def plot_timing(tempo_map: dict):
    """
    Plot the Tempo curve for each meter in the tempo_map
    :param tempo_map: a dict with the meter as key and a list of ratio as value for one bar
    :return: None
    """
    longest_meter = max(tempo_map, key=lambda x: len(tempo_map[x]))
    for meter in tempo_map:
        sns.lineplot(x=list(range(len(tempo_map[meter]))), y=tempo_map[meter], label=meter, marker='o')
    plt.xlabel('Beats')
    plt.ylabel('Tempo Ratio')
    plt.title('Tempo curve')
    plt.xticks(range(len(longest_meter) + 1))
    plt.grid(True)
    # Put legend outside the plot
    plt.legend(title='Meter', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()
