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


def get_piece_symbolic_to_performed_times(unperformed_path: str, performed_path: str) -> dict:
    """
    Get the symbolic and performed times for a piece
    :param unperformed_path:  path to the annotation file with the symbolic times
    :param performed_path: path to the annotation file with the performed times
    :return: a dict containing the symbolic and performed times for each beat, with their meter, key and beat type
    """
    result_performed = {}
    result_symbolic = {}
    with open(performed_path, "r") as f:
        performed_data = f.readlines()
        current_key = None
        current_meter = None
        current_beat = 0
        for line in performed_data:
            line_data = line.split()
            beat_key_meter = line_data[2].split(',')
            beat_type = beat_key_meter[0]
            if len(beat_key_meter) == 3:
                current_meter = beat_key_meter[1]
                current_key = beat_key_meter[2]
            elif len(beat_key_meter) == 2:
                current_meter = beat_key_meter[1]

            result_performed[current_beat] = {
                "key": current_key,
                "meter": current_meter,
                "onset": line_data[0],
                "beat_type": beat_type
            }
            current_beat += 1

    with open(unperformed_path, "r") as f:
        unperformed_data = f.readlines()
        current_beat = 0
        for line in unperformed_data:
            line_data = line.split()
            result_symbolic[current_beat] = {
                "onset": line_data[0],
            }
            current_beat += 1
    result = {}
    for key in result_performed:
        result[key] = {
            "symbolic": result_symbolic[key],
            "performed": result_performed[key]
        }
    return result


def get_tempo_map(symbolic_to_performed_times: dict) -> dict:
    """
    Get the tempo map from the symbolic to the performed times
    Compute the tempo ratio for each beat
    :param symbolic_to_performed_times:
    :return: dict
    """
    result = {}
    for i in range(len(symbolic_to_performed_times) - 2):
        onset = symbolic_to_performed_times[i]["performed"]["onset"]
        next_onset = symbolic_to_performed_times[i + 1]["performed"]["onset"]
        duration_performed = float(next_onset) - float(onset)
        onset_symbolic = symbolic_to_performed_times[i]["symbolic"]["onset"]
        next_onset_symbolic = symbolic_to_performed_times[i + 1]["symbolic"]["onset"]
        duration_symbolic = float(next_onset_symbolic) - float(onset_symbolic)
        tempo_performed = 1 / duration_performed
        tempo_symbolic = 1 / duration_symbolic
        result[i] = tempo_performed / tempo_symbolic
    return result
