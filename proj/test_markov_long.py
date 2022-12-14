import pytest
from markov import identify_speaker
import pathlib

USE_HASHTABLE = [False]
# Uncomment this to run w/ Hashtable impl.  Warning: will take a long time!
# USE_HASHTABLE = [True]

bush_kerry_files = [
    str(p)
    for p in (pathlib.Path(__file__).parent / "speeches" / "bush-kerry3").glob("*.txt")
]

obama_mccain_raw = [
    str(p)
    for p in (pathlib.Path(__file__).parent / "speeches" / "obama-mccain3").glob(
        "*.txt"
    )
]
obama_mccain_exclude = [
    "MCCAIN-1.txt",
    "MCCAIN-15.txt",
    "MCCAIN-18.txt",
    "MCCAIN-25.txt",
    "MCCAIN-26.txt",
    "MCCAIN-35.txt",
    "MCCAIN-36.txt",
    "MCCAIN-42.txt",
    "MCCAIN-57.txt",
    "MCCAIN-3.txt",
    "MCCAIN-22.txt",
    "MCCAIN-32.txt",
    "MCCAIN-30.txt",
    "MCCAIN-33.txt",
    "MCCAIN-46.txt",
    "MCCAIN-46.txt",
    "MCCAIN-48.txt",
    "MCCAIN-5.txt",
    "MCCAIN-6.txt",
    "MCCAIN-63.txt",
    "OBAMA-12.txt",
    "OBAMA-16.txt",
    "OBAMA-17.txt",
    "OBAMA-18.txt",
    "OBAMA-19.txt",
    "OBAMA-3.txt",
    "OBAMA-37.txt",
    "OBAMA-38.txt",
    "OBAMA-6.txt",
]
obama_mccain_files = []
for fn in obama_mccain_raw:
    for exclude in obama_mccain_exclude:
        if exclude in fn:
            break
    else:
        obama_mccain_files.append(fn)


@pytest.mark.parametrize("k", [2, 3])
@pytest.mark.parametrize("use_hashtable", USE_HASHTABLE)
@pytest.mark.parametrize("filename", bush_kerry_files)
def test_2004(filename, use_hashtable, k):
    bush = open("speeches/bush1+2.txt").read()
    kerry = open("speeches/kerry1+2.txt").read()

    # the classifier is not 100% accurate, here are cases where it will fail on k=3
    exceptions = (
        ("BUSH-27.txt", 2),
        ("BUSH-19.txt", 2),
        ("BUSH-19.txt", 3),
        ("BUSH-21.txt", 2),
        ("BUSH-21.txt", 3),
        ("BUSH-15.txt", 2),
        ("BUSH-17.txt", 2),
        ("KERRY-20.txt", 2),
        ("BUSH-3.txt", 2),
        ("BUSH-3.txt", 3),
        ("BUSH-4.txt", 2),
        ("BUSH-4.txt", 3),
        ("BUSH-2.txt", 2),
        ("BUSH-2.txt", 3),
    )

    for xfile, xk in exceptions:
        if xfile in filename and k == xk:
            raise pytest.skip("OK")

    text = open(filename).read()
    if "BUSH" in filename:
        expected = "A"
    else:
        expected = "B"
    probA, probB, predicted = identify_speaker(
        bush, kerry, text, k, use_hashtable=use_hashtable
    )
    assert predicted == expected, f"{filename}: expected {predicted}, got {expected}"


@pytest.mark.parametrize("k", [3, 4])
@pytest.mark.parametrize("use_hashtable", USE_HASHTABLE)
@pytest.mark.parametrize("filename", obama_mccain_files)
def test_2008(filename, use_hashtable, k):
    obama = open("speeches/obama1+2.txt").read()
    mccain = open("speeches/mccain1+2.txt").read()

    # the classifier is not 100% accurate, here are cases where it will fail on k=3
    exceptions = (
        ("BUSH-27.txt", 2),
        ("BUSH-19.txt", 2),
        ("BUSH-19.txt", 3),
        ("BUSH-21.txt", 2),
        ("BUSH-21.txt", 3),
        ("BUSH-15.txt", 2),
        ("BUSH-17.txt", 2),
        ("KERRY-20.txt", 2),
        ("BUSH-3.txt", 2),
        ("BUSH-3.txt", 3),
        ("BUSH-4.txt", 2),
        ("BUSH-4.txt", 3),
        ("BUSH-2.txt", 2),
        ("BUSH-2.txt", 3),
    )

    for xfile, xk in exceptions:
        if xfile in filename and k == xk:
            raise pytest.skip("OK")

    text = open(filename).read()
    if "OBAMA" in filename:
        expected = "A"
    else:
        expected = "B"
    probA, probB, predicted = identify_speaker(
        obama, mccain, text, k, use_hashtable=use_hashtable
    )
    assert predicted == expected, f"{filename}: expected {predicted}, got {expected}"
