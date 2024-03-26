import music21
import pandas as pd
from music21.stream import Score


def parse_score_to_dataframe(score: Score) -> pd.DataFrame:
    """
    Parse a music21 score object into a pandas dataframe
    :param score: music21 score object
    :return: pandas dataframe
    """
    rhythm_data_list = []
    for part_index, part in enumerate(score.parts):
        clefs = part.getElementsByClass('Clef')
        clef_name = clefs[0].sign if clefs else f"Part_{part_index + 1}_NoClef"

        for measure in part.getElementsByClass('Measure'):
            time_signature_str = measure.timeSignature.ratioString if measure.timeSignature else "NoTimeSignature"

            for event in measure.notesAndRests:
                label = "sounded" if isinstance(event, music21.note.Note) else "unsounded"
                tie_info = f"tie_{event.tie.type}" if event.tie else "no_tie"
                # Compute onset
                global_onset = (measure.number - 1) * measure.barDuration.quarterLength + event.offset
                rhythm_data_list.append({
                    'staff': clef_name,
                    'measure_number': measure.number,
                    'time_signature': time_signature_str,
                    'event_type': label,
                    'onset_in_measure': event.offset,
                    'onset_in_score': global_onset,
                    'duration': event.duration.quarterLength,
                    'tie_info': tie_info
                })

    return pd.DataFrame(rhythm_data_list)


def extract_onset_in_measure(rhythm_data_list: pd.DataFrame) -> pd.DataFrame:
    """
    Return a dataframe containing only the onsets of sounded events
    :param rhythm_data_list: input dataframe
    :return: output dataframe
    """
    return rhythm_data_list[(rhythm_data_list['event_type'] == "sounded") &
                            (rhythm_data_list['tie_info'] != "tie_stop")]['onset_in_measure']
