import os

import matplotlib.pyplot as plt
import numpy as np
from music21 import converter
from scipy.stats import entropy
from scipy.stats import ttest_ind


def read_musicxml_and_normalize(path: str) -> dict:
    """
    Reads a MusicXML file and returns normalized time and pitch data.
    :param path: the path or directory of the MusicXML file.
    :return: A dictionary containing music data, with keys being relative paths to files and
    values being dictionaries containing normalized time and pitch.
    """
    music_data = {}
    for dir_path, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.musicxml'):
                file_path = os.path.join(dir_path, filename)
                relative_path = os.path.relpath(file_path, path)

                score = converter.parse(file_path)

                pitches = []
                times = []
                current_time = 0.0

                for part in score.parts:
                    for measure in part.getElementsByClass('Measure'):
                        for note in measure.notes:
                            if note.isNote:
                                pitches.append(note.pitch.midi)
                                times.append(current_time)
                                current_time += note.duration.quarterLength

                total_time = max(times) if times else 1
                if total_time > 0:
                    normalized_times = [t / total_time for t in times]
                    music_data[relative_path] = {"pitches": pitches, "times": normalized_times}
                else:
                    print(f"Warning: '{relative_path}' contains no notes.")
    return music_data


def plot_pitch_contours(music_data: dict, title: str = "Normalized Time Pitch Contour") -> None:
    """
    Plots the pitch contour of given musical data.
    :param music_data: A dictionary containing the music data to plot.
    :param title: The title of the plot.
    :return: None
    """
    plt.figure(figsize=(30, 10))

    for key, data in music_data.items():
        plt.plot(data["times"], data["pitches"], linestyle='-', label=key)

    plt.title(title)
    plt.xlabel('Normalized Time')
    plt.ylabel('Pitch (MIDI Note Number)')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_average_pitch_contours(music_data: dict, title: str = "Normalized Average Time Pitch Contour"):
    """
    Plots the average pitch profile of given music data.
    :param music_data: A dictionary containing normalized time and pitch data for each piece.
    :param title: The title of the plot.
    """
    # Combine pitch data for all tracks into one list
    all_pitches = [data['pitches'] for data in music_data.values()]
    all_times = [data['times'] for data in music_data.values()]

    # Align all time and pitch data to the same timeline
    # Here you need to create a timeline that is common to all tracks
    # Assume that all tracks are already processed with the same normalized time length
    max_time_points = max(len(times) for times in all_times)
    common_time_line = np.linspace(0, 1, max_time_points)

    pitch_values_at_common_times = np.zeros((len(all_pitches), max_time_points))

    # Interpolate
    for i, (times, pitches) in enumerate(zip(all_times, all_pitches)):
        pitch_values_at_common_times[i] = np.interp(common_time_line, times, pitches)

    # Calculate the average pitch at each time point on a universal timeline
    average_pitches = np.mean(pitch_values_at_common_times, axis=0)

    plt.figure(figsize=(12, 6))
    plt.plot(common_time_line, average_pitches, label="Average Pitch Contour")
    plt.title(title)
    plt.xlabel('Normalized Time')
    plt.ylabel('Pitch (MIDI Note Number)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_cdf(music_data: dict, title: str = "CDF of Pitch Frequencies") -> None:
    """
    Plot the pitch's CDF。

    :param music_data: A dictionary containing normalized time and pitch data for each piece.
    :param title: The title of the plot.
    :return: None
    """
    # Summarize the pitches of all works into a list
    all_pitches = [pitch for data in music_data.values() for pitch in data['pitches']]

    # calculate the pdf
    values, base = np.histogram(all_pitches, bins=range(min(all_pitches), max(all_pitches) + 1), density=True)
    cumulative = np.cumsum(values)

    plt.figure(figsize=(10, 7))
    plt.plot(base[:-1], cumulative, c='blue')
    plt.title(title)
    plt.xlabel('Pitch (MIDI Note Number)')
    plt.ylabel('CDF')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_all_average_pitch_contours(musician_data: dict, title: str = "Normalized Average Time Pitch Contour"):
    """
    Plot the average pitch profile of multiple musicians.
    :param musician_data: A dictionary whose keys are musician names and whose values are the corresponding
    dictionary of music data.
    :param title: The title of the chart.
    :return: None
    """
    plt.figure(figsize=(12, 6))

    for musician, music_data in musician_data.items():
        all_pitches = [data['pitches'] for data in music_data.values()]
        all_times = [data['times'] for data in music_data.values()]
        max_time_points = max(len(times) for times in all_times)
        common_time_line = np.linspace(0, 1, max_time_points)
        pitch_values_at_common_times = np.zeros((len(all_pitches), max_time_points))

        for i, (times, pitches) in enumerate(zip(all_times, all_pitches)):
            pitch_values_at_common_times[i] = np.interp(common_time_line, times, pitches)

        average_pitches = np.mean(pitch_values_at_common_times, axis=0)

        plt.plot(common_time_line, average_pitches, label=f"{musician} Average Pitch Contour")

    plt.title(title)
    plt.xlabel('Normalized Time')
    plt.ylabel('Pitch (MIDI Note Number)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_musician_contours_for_era(musician_paths, era_title: str) -> None:
    """
    Plot the average pitch profile of multiple musicians for a given era.
    :param musician_paths: A dictionary whose keys are musician names and whose values are the corresponding paths.
    :param era_title: The title of the era.
    :return: None
    """
    musician_data = {musician: read_musicxml_and_normalize(path) for musician, path in musician_paths.items()}
    plot_all_average_pitch_contours(musician_data, f"Normalized Time Pitch Contour for {era_title} Musicians")


def calculate_entropy(music_data: dict) -> tuple:
    """
    Calculate the entropy of pitch distributions for each work or composer.
    :param music_data: A dictionary with keys representing different works or composers and values containing lists of pitches.
    :return: A tuple containing entropy values for each work or composer and average entropy.
    """
    entropy_results = {}
    entropy_values = []
    for key, data in music_data.items():
        pitch_counts = np.bincount(data['pitches'])
        entropy_results[key] = entropy(pitch_counts, base=2)
        entropy_values.append(entropy_results[key])
    # average entropy for all works
    average_entropy = np.mean(entropy_values) if entropy_values else None

    return entropy_values, average_entropy


def merge_music_data_by_era(all_musician_paths: dict, era_musician_paths: dict) -> dict:
    """
    Merge the musical data of musicians in the same period.
    :param all_musician_paths: A dictionary whose keys are musician names and whose values are the corresponding paths.
    :param era_musician_paths: A dictionary whose keys are periods and whose values are lists of musician names.
    :return: A dictionary containing merged musical data for each period.
    """
    # Create a new dict to conserve merged musical data
    merged_music_data_by_era = {}
    # Traversal every period
    for era, musicians in era_musician_paths.items():
        # Create a list to conserve the pitch data for all musicians in this period
        merged_pitches = []
        merged_times = []

        for musician in musicians:
            if musician in all_musician_paths:
                path = all_musician_paths[musician]
                music_data = read_musicxml_and_normalize(path)
                for work, data in music_data.items():
                    merged_pitches.extend(data['pitches'])
                    merged_times.extend(data['times'])

        merged_music_data_by_era[era] = {'pitches': merged_pitches, 'times': merged_times}

    return merged_music_data_by_era


def perform_t_test(music_data: dict) -> dict:
    """
    Perform t-tests to assess the significance of differences in pitch distributions between different works
    or composers.
    :param music_data: A dictionary with keys representing different works or
    composers and values containing lists of pitches.
    :return: A dictionary with the t-test results, including t-values and p-values.
    """
    results = {}
    keys = list(music_data.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            t_stat, p_val = ttest_ind(music_data[keys[i]]['pitches'], music_data[keys[j]]['pitches'], equal_var=False)
            results[(keys[i], keys[j])] = {'t-statistic': t_stat, 'p-value': p_val}
    return results
