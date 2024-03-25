import matplotlib.pyplot as plt


# def get_mapping(unperformed_midi_path: str, performed_midi_path: str) -> dict:
#     """
#     Maps unperformed symbolic attributes(offset, duration, velocity) to performed attributes (offset,velocity).
#     :param unperformed_midi_path: str
#     :param performed_midi_path: str
#     :return: note_mapping: dict
#     """
#     music21_midi_unperformed = music21.converter.parse(unperformed_midi_path)
#     music21_midi_performed = music21.converter.parse(performed_midi_path)
#
#     # Extract symbolic times from music sheet MIDI
#     symbolic_times = []
#     for element in music21_midi_unperformed.recurse():
#         if isinstance(element, note.Note):
#             symbolic_times.append((element.offset, element.duration.quarterLength, element.volume.velocity))
#
#     # Extract performance attributes from recorded MIDI
#     performance_attributes = []
#     for element in music21_midi_performed.recurse():
#         if isinstance(element, note.Note):
#             performance_attributes.append((element.offset, element.volume.velocity))
#
#     # Map symbolic times to performance attributes
#     mapped_data = []
#     for i, symbolic_time in enumerate(symbolic_times):
#         for j, performance_attr in enumerate(performance_attributes):
#             if symbolic_time[0] == performance_attr[0]:
#                 mapped_data.append((symbolic_time, performance_attr))
#                 break
#
#     print(mapped_data[:10])
#     return {symbolic_time: performance_attr for symbolic_time, performance_attr in mapped_data}
#
#
# def timing(unperformed_midi_path: str, performed_midi_path: str) -> dict:
#     """
#     Maps symbolic time to performance attributes (tempo,velocity),
#     so that one can use it to transform the "unperformed" MIDI to the "performed" MIDI.
#     :param unperformed_midi_path: str
#     :param performed_midi_path: str
#     :return: time_map: dict containing symbolic time to performance attributes (tempo,velocity)
#     """
#     note_mapping = get_mapping(unperformed_midi_path, performed_midi_path)
#     return {unperf_note[0]: {
#         "tempo": perf_note[0],
#         "velocity": perf_note[1] / unperf_note[2] if unperf_note[2] != 0 else 0
#     } for unperf_note, perf_note in note_mapping.items()}
#
def plot_timing_as_tempo_curve(tempo_map: dict):
    """
    Plot the tempo_map from timing function as a tempo curve.
    :param tempo_map: dict
    :return: None
    """
    fig, ax = plt.subplots()
    ax.plot(list(tempo_map.keys()), list(tempo_map.values()))
    ax.set(xlabel='Time', ylabel='Tempo',
           title='Tempo curve')
    ax.grid()
    ax.legend()
    plt.show()


# def plot_timing_as_velocity_curve(velocity_map: dict):
#     """
#     Plot the velocity_map from the function timing as a velocity curve.
#     :param velocity_map: dict
#     :return: None
#     """
#     fig, ax = plt.subplots()
#     ax.plot(list(velocity_map.keys()), list(velocity_map.values()))
#     ax.set(xlabel='Time', ylabel='Velocity',
#            title='Velocity curve')
#     ax.grid()
#     ax.legend()
#     plt.show()

def get_piece_symbolic_to_performed_times(unperformed_path: str, performed_path: str) -> dict:
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
    result = {}
    first_timestamp = symbolic_to_performed_times[0]["symbolic"]["onset"]
    last_timestamp = symbolic_to_performed_times[len(symbolic_to_performed_times) - 1]["symbolic"]["onset"]
    duration = float(last_timestamp) - float(first_timestamp)
    symbolic_tempo = len(symbolic_to_performed_times) / duration
    print(symbolic_tempo)
    for i in range(len(symbolic_to_performed_times) - 2):
        onset = symbolic_to_performed_times[i]["performed"]["onset"]
        next_onset = symbolic_to_performed_times[i + 1]["performed"]["onset"]
        duration_performed = float(next_onset) - float(onset)
        onset_symbolic = symbolic_to_performed_times[i]["symbolic"]["onset"]
        next_onset_symbolic = symbolic_to_performed_times[i + 1]["symbolic"]["onset"]
        duration_symbolic = float(next_onset_symbolic) - float(onset_symbolic)
        tempo_performed = 1/duration_performed
        tempo_symbolic = 1/duration_symbolic
        print(tempo_performed, tempo_symbolic)
        result[i] = tempo_performed/tempo_symbolic

    return result


# TODO remove this main, only useful for testing Task A
if __name__ == "__main__":
    symbolic_to_performed_times = get_piece_symbolic_to_performed_times(
        "./asap-dataset/Bach/Fugue/bwv_846/Shi05M_annotations.txt",
        "./asap-dataset/Bach/Fugue/bwv_846/midi_score_annotations.txt"
    )
    tempo_map = get_tempo_map(symbolic_to_performed_times)
    plot_timing_as_tempo_curve(tempo_map)

    symbolic_to_performed_times = get_piece_symbolic_to_performed_times(
        "./asap-dataset/Chopin/Ballades/1/Ali01_annotations.txt",
        "./asap-dataset/Chopin/Ballades/1/midi_score_annotations.txt"
    )
    tempo_map = get_tempo_map(symbolic_to_performed_times)
    plot_timing_as_tempo_curve(tempo_map)

# time_map = timing("./asap-dataset/Chopin/Ballades/1/Ali01.mid",
#                   "./asap-dataset/Chopin/Ballades/1/midi_score.mid")
# tempo_maps = {time: time_map[time]["tempo"] for time in time_map}
# velocity_maps = {time: time_map[time]["velocity"] for time in time_map}
# plot_timing_as_tempo_curve(tempo_maps)
# plot_timing_as_velocity_curve(velocity_maps)
