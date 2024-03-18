import matplotlib.pyplot as plt
import music21


def timing(unperformed_midi_path: str, performed_midi_path: str) -> dict and dict:
    """
    Maps symbolic time to performance attributes (tempo,velocity),
    so that one can use it to transform the "unperformed" MIDI to the "performed" MIDI.
    :param unperformed_midi_path: str
    :param performed_midi_path: str
    :return: tempo_maps, velocity_maps
    """
    music21_midi_unperformed = music21.converter.parse(unperformed_midi_path)
    music21_midi_performed = music21.converter.parse(performed_midi_path)

    times = {}
    velocities = {}
    tempo_mapping = {}
    velocity_mapping = {}

    for note in music21_midi_unperformed.flat.notes:
        times[note.offset] = note.duration.quarterLength
        velocities[note.offset] = note.volume.velocity

    for note in music21_midi_performed.flat.notes:
        if note.offset in times:
            tempo_mapping[note.offset] = note.duration.quarterLength / times[note.offset]
            velocity_mapping[note.offset] = note.volume.velocity / velocities[note.offset]

    return tempo_mapping, velocity_mapping


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


def plot_timing_as_velocity_curve(velocity_map: dict):
    """
    Plot the velocity_map from the function timing as a velocity curve.
    :param velocity_map: dict
    :return: None
    """
    fig, ax = plt.subplots()
    ax.plot(list(velocity_map.keys()), list(velocity_map.values()))
    ax.set(xlabel='Time', ylabel='Velocity',
           title='Velocity curve')
    ax.grid()
    ax.legend()
    plt.show()


# TODO remove this main, only useful for testing Task A
if __name__ == "__main__":
    tempo_maps, velocity_maps = timing("./asap-dataset/Chopin/Ballades/1/Ali01.mid",
                                       "./asap-dataset/Chopin/Ballades/1/midi_score.mid")
    plot_timing_as_tempo_curve(tempo_maps)
    plot_timing_as_velocity_curve(velocity_maps)
