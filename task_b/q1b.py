import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_rawdata(path: str) -> pd.DataFrame:
    """
    Read the data from the path and return it as a DataFrame.
    :param path: str
    :return: pd.DataFrame
    """
    scores = pd.read_table(path, sep='\t', names=["start", "end", "b"])
    scores["b"] = scores["b"].apply(lambda x: x.split(",")[0])
    return scores


def get_duration(score: pd.DataFrame) -> list:
    """
    Return the duration of each sound.
    :param score:
    :return:
    """
    return [score["start"][i + 1] - score["start"][i] for i in range(len(score) - 1)]


def violin_plot_each_part(scores: pd.DataFrame, original_scores: pd.DataFrame, artist: str) -> None:
    """
    Plot the distribution of sound duration for each part.
    :param scores: pd.DataFrame
    :param original_scores: pd.DataFrame
    :param artist: str
    :return: None
    """
    list_original = get_duration(original_scores)
    list_db_b_b_ = get_duration(scores)
    list_db_b_b = []
    for i in range(0, len(list_db_b_b_), 3):
        try:
            tmp_list = [list_db_b_b_[i] - list_original[i], list_db_b_b_[i + 1] - list_original[i + 1],
                        list_db_b_b_[i + 2] - list_original[i + 2]]
            list_db_b_b.append(tmp_list)
        except IndexError:
            pass
    x, y, z = zip(*list_db_b_b)
    list_labels = ["db", "2b", "3b"]
    dividing_point = [0, len(z) // 4, len(z) // 4 * 2, len(z) // 4 * 3, len(z)]
    fig, ax = plt.subplots()
    ax.set_ylim([-0.5, 0.5])
    ax.set_title(f"Distribution of sound duration by {artist}")
    ax.set_ylabel("shorter        -        original        -        longer")
    ax.set_xticks(np.arange(1, len(list_labels) + 1), labels=list_labels)
    ax.violinplot([list(x), list(y), list(z)])
    fig, ax = plt.subplots(1, len(dividing_point) - 1, figsize=(20, 5))
    for i in range(len(dividing_point) - 1):
        list_all = [list(x)[dividing_point[i]:dividing_point[i + 1]],
                    list(y)[dividing_point[i]:dividing_point[i + 1]],
                    list(z)[dividing_point[i]:dividing_point[i + 1]]]
        ax[i].set_ylim([-0.5, 0.5])
        ax[i].violinplot(list_all)
        ax[i].set_xticks(np.arange(1, len(list_labels) + 1))
        ax[i].set_xticklabels(list_labels)
        ax[i].set_title(f"distribution in {i + 1} / 4 part by {artist}")
        ax[i].set_ylabel("shorter        -        original        -        longer")

    plt.tight_layout()
    plt.show()


def plot_third_part(scores: pd.DataFrame, original: pd.DataFrame) -> None:
    """
    Plot the duration of the third part.
    :param scores: pd.DataFrame
    :param original: pd.DataFrame
    :return: None
    """
    list_db_b_b_ = get_duration(scores)
    list_original = get_duration(original)
    list_db_b_b = [list_db_b_b_[i] - list_original[i] for i in range(len(list_db_b_b_))]
    part_length = len(list_db_b_b) // 4
    plt.plot(list(scores["start"][part_length * 2:part_length * 3]), list_db_b_b[part_length * 2:part_length * 3])
    plt.xlabel("Elapsed time")
    plt.ylabel("Duration compared to original scores")
    plt.show()
