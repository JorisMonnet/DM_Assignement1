"""
This module contains functions to get the timing attributes for multiple pieces
by averaging the timing attributes for each beat of a meter.

@Author: Joris Monnet
@Date: 2024-03-26
"""
import os


def merge_sum_and_lengths_timings(sum_and_lengths: list[dict]) -> dict:
    """
    Merge the sum of the durations and the number of beats for each beat of a meter of multiple files
    :param sum_and_lengths:
    :return: dict with meter as key and the sum of the durations and the number of beats for each beat as list
    """
    result = {}
    for sum_and_lengths_file in sum_and_lengths:
        for meter in sum_and_lengths_file:
            if meter not in result:
                result[meter] = {
                    "sum_durations": [0 for _ in range(len(sum_and_lengths_file[meter]["sum_durations"]))],
                    "number_of_beats": [0 for _ in range(len(sum_and_lengths_file[meter]["sum_durations"]))],
                }
            meter_for_result = meter
            if len(result[meter]["sum_durations"]) != len(sum_and_lengths_file[meter]["sum_durations"]):
                meter_for_result = (f"{meter}_with_{str(len(sum_and_lengths_file[meter]['sum_durations']))}_downbeat"
                                    f"{'s' if len(sum_and_lengths_file[meter]['sum_durations']) > 1 else ''}")
                result[meter_for_result] = {
                    "sum_durations": [0 for _ in range(len(sum_and_lengths_file[meter]["sum_durations"]))],
                    "number_of_beats": [0 for _ in range(len(sum_and_lengths_file[meter]["sum_durations"]))],
                }
            for i in range(len(sum_and_lengths_file[meter]["sum_durations"])):
                result[meter_for_result]["sum_durations"][i] += sum_and_lengths_file[meter]["sum_durations"][i]
                result[meter_for_result]["number_of_beats"][i] += sum_and_lengths_file[meter]["number_of_beats"][i]
    return result


def get_sum_and_lengths_timing_one_bar(path: str) -> dict:
    """
    Get the sum of the durations and the number of beats for each beat of a meter of a single file
    :param path: to the annotation file
    :return: dict with meter as key and the sum of the durations and the number of beats for each beat as list
    """
    result = {}
    with open(path, "r") as f:
        symbolic_data = f.readlines()
        current_beat = 0
        current_meter = None
        for i in range(len(symbolic_data) - 1):
            line_data = symbolic_data[i].split()
            next_line_data = symbolic_data[i + 1].split()
            beat_type_meter_key = line_data[2].split(',')
            meter = beat_type_meter_key[1] if len(beat_type_meter_key) > 1 else ""
            if meter != current_meter and meter != "":
                current_meter = meter
                if current_meter not in result:
                    result[current_meter] = {
                        "sum_durations": [0],
                        "number_of_beats": [0],
                    }
                current_beat = 0
            elif current_meter is None:
                # Anacrusis
                continue
            if beat_type_meter_key[0] == "db":
                current_beat = 0  # Downbeat
            elif beat_type_meter_key[0] == "b":
                current_beat += 1  # other beats
            elif beat_type_meter_key[0] == "bR":  # Remove beats with type bR (beats that are not in the meter)
                continue
            new_onset = float(next_line_data[0]) - float(line_data[0])
            if len(result[current_meter]["sum_durations"]) <= current_beat:
                result[current_meter]["sum_durations"].append(0)
                result[current_meter]["number_of_beats"].append(0)
            result[current_meter]["sum_durations"][current_beat] += new_onset
            result[current_meter]["number_of_beats"][current_beat] += 1
    return result


def get_average_from_sum_and_lengths(sum_and_lengths: dict) -> dict:
    """
    Get the average timing for each beat of a meter
    :param sum_and_lengths: dict containing the sum of the durations and the number of beats for each beat
    :return: dict with meter as key and the average timing for each beat as list
    """
    return {meter: [sum_and_lengths[meter]["sum_durations"][i] / sum_and_lengths[meter]["number_of_beats"][i]
                    for i in range(len(sum_and_lengths[meter]["sum_durations"]))] for meter in sum_and_lengths}


def get_average_symbolic_and_performed_times(folder_path: str) -> tuple[dict, dict]:
    """
    Get the average symbolic and performed times for each beat of a meter
    :param folder_path: path to the folder containing all the annotations files (can be in sub folders)
    :return: dict with meter as key and the average symbolic times for each beat as list and
    dict with meter as key and the average performed times for each beat as list
    """
    annotations_files = get_annotations_files_from_folder(folder_path)
    symbolic_files = [file for file in annotations_files if "midi_score_annotations.txt" in file]
    perf_files = [file for file in annotations_files if "midi_score_annotations.txt" not in file]
    sum_and_lengths_list = [get_sum_and_lengths_timing_one_bar(file) for file in perf_files]
    merged_sum_and_lengths = merge_sum_and_lengths_timings(sum_and_lengths_list)
    average_perf = get_average_from_sum_and_lengths(merged_sum_and_lengths)
    sum_and_lengths_list = [get_sum_and_lengths_timing_one_bar(file) for file in symbolic_files]
    merged_sum_and_lengths = merge_sum_and_lengths_timings(sum_and_lengths_list)
    average_symbolic = get_average_from_sum_and_lengths(merged_sum_and_lengths)
    return average_symbolic, average_perf


def get_annotations_files_from_folder(folder_path: str) -> list:
    """
    Get the path of all the annotations files in a folder and its sub folders
    :param folder_path: path to the folder
    :return: list of paths to the txt files
    """
    txt_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith("annotations.txt"):
                txt_files.append(os.path.join(root, file))
        for directory in dirs:
            txt_files.extend(get_annotations_files_from_folder(os.path.join(root, directory)))
    return txt_files


def timing(folder_path: str) -> dict:
    """
    Get the tempo ratio between symbolic and performed times for each beat of a meter
    :param folder_path: path to the folder containing all the annotations files (can be in sub folders)
    :return: dict with meter as key and the tempo ratio for each beat as list
    """
    perf_average, symbolic_average = get_average_symbolic_and_performed_times(folder_path)
    return {
        meter: [perf_average[meter][i] / symbolic_average[meter][i] for i in range(len(perf_average[meter]))]
        for meter in perf_average
    }


if __name__ == "__main__":
    print(timing("../asap-dataset"))
