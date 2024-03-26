"""
This module contains functions used to plot the results for Task A.

@Author: Joris Monnet
@Date: 2024-03-26
"""

import matplotlib.pyplot as plt


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
    ax.grid()
    plt.show()


def plot_timing(tempo_map: dict):
    """
    Plot the Tempo curve for each meter in the tempo_map
    :param tempo_map: a dict with the meter as key and a list of ratio as value for one bar
    :return: None
    """
    for meter in tempo_map:
        fig, ax = plt.subplots()
        ax.plot(list(range(len(tempo_map[meter]))), tempo_map[meter])
        ax.set(xlabel='Beats', ylabel='Tempo Ratio',
               title=f'Tempo curve for {meter}')
        ax.grid()
        plt.show()
