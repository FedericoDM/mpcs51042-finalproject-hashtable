import sys
import time
import pathlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from markov import identify_speaker

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <max-k> <runs>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, max_k, runs = sys.argv[1:]
    max_k = int(max_k)
    runs = int(runs)

    # fileA = "bush1+2.txt"
    # fileB = "kerry1+2.txt"
    # fileC = "bush-kerry3/BUSH-0.txt"

    fileA = pathlib.Path(__file__).parent / filenameA
    fileB = pathlib.Path(__file__).parent / filenameB
    fileC = pathlib.Path(__file__).parent / filenameC

    text_a = fileA.read_text()
    text_b = fileB.read_text()
    text_c = fileC.read_text()

    # Run performance tests as outlined in README.md
    num_runs = range(1, runs + 1)
    num_ks = range(1, max_k + 1)

    dicts_list = []

    for num_k in num_ks:

        for num_run in num_runs:

            htable_start = time.perf_counter()
            tup = identify_speaker(text_a, text_b, text_c, num_k, use_hashtable=True)
            htable_stop = time.perf_counter()
            htable_elapsed = htable_stop - htable_start

            htable_dict = {
                "Implementation": "Hashtable",
                "K": num_k,
                "Run": num_run,
                "Time": htable_elapsed,
            }

            dicts_list.append(htable_dict)

            dict_start = time.perf_counter()
            tup = identify_speaker(text_a, text_b, text_c, num_k, use_hashtable=False)
            dict_stop = time.perf_counter()
            dict_elapsed = dict_stop - dict_start
            dict_dict = {
                "Implementation": "Dict",
                "K": num_k,
                "Run": num_run,
                "Time": dict_elapsed,
            }

            dicts_list.append(dict_dict)

    # Getting pandas DF and Seaborn Graph

    df = pd.DataFrame.from_dict(dicts_list)

    avg_times = df.groupby(by=["Implementation", "K"]).mean().reset_index()
    avg_times.drop(columns=["Run"], inplace=True)

    # Saving Seaborn Plot
    sns.set_theme()
    fig, ax = plt.subplots()
    ax1 = sns.pointplot(
        x="K",
        y="Time",
        linestyles="-",
        markers="o",
        hue="Implementation",
        data=avg_times,
    )

    ax.set_title("Hashtable vs Python Dict")
    ax.set_xlabel("K")
    ax.set_ylabel(f"Average Time (Runs = {runs})")

    plt.savefig("performance_graph.png")
