import os


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
                current_int_meter = int(meter.split('/')[0])
                if current_meter not in result:
                    result[current_meter] = {
                        "sum_durations": [0 for _ in range(current_int_meter)],
                        "number_of_beats": [0 for _ in range(current_int_meter)],
                    }
                current_beat = 0
            elif current_meter is None:
                # Anacrusis, need to update the previous onset to get a correct first beat onset
                previous_onset = float(line_data[0])
                continue
            new_onset = float(line_data[0]) - previous_onset
            result[current_meter]["sum_durations"][current_beat] += new_onset
            result[current_meter]["number_of_beats"][current_beat] += 1
            previous_onset = float(line_data[0])
            if current_beat == current_int_meter - 1:
                current_beat = 0  # Downbeat
            else:
                current_beat += 1  # Upbeats
    return result


def get_average_from_sum_and_lengths(sum_and_lengths: dict) -> dict:
    """
    Get the average timing for each beat of a meter
    :param sum_and_lengths: dict containing the sum of the durations and the number of beats for each beat
    :return: dict with meter as key and the average timing for each beat as list
    """
    average = {}
    for meter in sum_and_lengths:
        average[meter] = [sum_and_lengths[meter]["sum_durations"][i] / sum_and_lengths[meter]["number_of_beats"][i]
                          for i in range(len(sum_and_lengths[meter]["sum_durations"]))]
    return average


def get_subfolders_with_parent_name(parent_folder):
    """
    Get sub folders with the name of the parent folder.
    :param parent_folder: Path to the parent folder.
    :return: List of sub folders with the name of the parent folder.
    """
    sub_folders = []
    for entry in os.listdir(parent_folder):
        full_path = os.path.join(parent_folder, entry)
        if os.path.isdir(full_path) and entry == os.path.basename(parent_folder):
            sub_folders.append(full_path)
    return sub_folders


def get_average_timing_specific_meter(folder_path: str, meter: str):
    sub_folders = get_subfolders_with_parent_name(folder_path)
    return sub_folders


if __name__ == "__main__":
    symbolic = get_sum_and_lengths_timing_one_bar("./asap-dataset/Chopin/Ballades/1/midi_score_annotations.txt")
    performance = get_sum_and_lengths_timing_one_bar("./asap-dataset/Chopin/Ballades/1/SINKEV05_annotations.txt")
    print(get_average_from_sum_and_lengths(symbolic))
    print(get_average_from_sum_and_lengths(performance))
