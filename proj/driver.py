import sys
import pathlib
from markov import identify_speaker

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <k> <hashtable-or-dict>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, k, hashtable_or_dict = sys.argv[1:]
    k = int(k)
    if hashtable_or_dict not in ("hashtable", "dict"):
        print("Final parameter must either be 'hashtable' or 'dict'")
        sys.exit(1)

    # Code here to open files & read text
    fileA = pathlib.Path(__file__).parent / filenameA
    fileB = pathlib.Path(__file__).parent / filenameB
    fileC = pathlib.Path(__file__).parent / filenameC

    text_a = fileA.read_text()
    text_b = fileB.read_text()
    text_c = fileC.read_text()

    if hashtable_or_dict == "hashtable":
        hashtable = True
    else:
        hashtable = False

    # Code to identify speaker
    speaker_a_prob, speaker_b_prob, likely = identify_speaker(text_a, text_b, text_c, 
                                                              k, hashtable_or_dict)

    print(f"Speaker A:{speaker_a_prob}")
    print(f"Speaker B:{speaker_b_prob}")

    print(f"Conclusion: Speaker {likely} is most likely")
    # Speaker A: -2.1670591295191572
    # Speaker B: -2.2363636778055525

    # Conclusion: Speaker A is most likely
