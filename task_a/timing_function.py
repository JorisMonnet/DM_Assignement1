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
                meter_for_result = f"{meter}_with_{str(len(sum_and_lengths_file[meter]['sum_durations']))}_db"
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
        previous_onset = 0
        for line in symbolic_data:
            line_data = line.split()
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
                # Anacrusis, need to update the previous onset to get a correct first beat onset
                previous_onset = float(line_data[0])
                continue
            if beat_type_meter_key[0] == "db":
                current_beat = 0  # Downbeat
            elif beat_type_meter_key[0] == "b":
                current_beat += 1  # other beats
            elif beat_type_meter_key[0] == "bR":  # Remove beats with type bR (beats that are not in the meter)
                previous_onset = float(line_data[0])
                continue
            new_onset = float(line_data[0]) - previous_onset
            if len(result[current_meter]["sum_durations"]) <= current_beat:
                result[current_meter]["sum_durations"].append(0)
                result[current_meter]["number_of_beats"].append(0)
            result[current_meter]["sum_durations"][current_beat] += new_onset
            result[current_meter]["number_of_beats"][current_beat] += 1
            previous_onset = float(line_data[0])
    return result


def get_average_from_sum_and_lengths(sum_and_lengths: dict) -> dict:
    """
    Get the average timing for each beat of a meter
    :param sum_and_lengths: dict containing the sum of the durations and the number of beats for each beat
    :return: dict with meter as key and the average timing for each beat as list
    """
    return {meter: [sum_and_lengths[meter]["sum_durations"][i] / sum_and_lengths[meter]["number_of_beats"][i]
                    for i in range(len(sum_and_lengths[meter]["sum_durations"]))] for meter in sum_and_lengths}


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


if __name__ == "__main__":
    # symbolic = get_sum_and_lengths_timing_one_bar("../asap-dataset/Bach/Fugue/bwv_846/midi_score_annotations.txt")
    # performance = get_sum_and_lengths_timing_one_bar("../asap-dataset/Bach/Fugue/bwv_846/Shi05M_annotations.txt")
    # print(get_average_from_sum_and_lengths(symbolic))
    # print(get_average_from_sum_and_lengths(performance))

    files_list = get_annotations_files_from_folder("../asap-dataset/")
    perf_files = [file for file in files_list if "midi_score_annotations.txt" not in file]
    sum_and_lengths_list = [get_sum_and_lengths_timing_one_bar(file) for file in perf_files]
    merged_sum_and_lengths = merge_sum_and_lengths_timings(sum_and_lengths_list)
    average = get_average_from_sum_and_lengths(merged_sum_and_lengths)
    print(average)
