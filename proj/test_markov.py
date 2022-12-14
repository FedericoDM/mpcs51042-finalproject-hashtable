import pytest
from markov import Markov, identify_speaker
import math
import pathlib


@pytest.mark.parametrize("use_hashtable", [True, False])
def test_markov_readme_k2(use_hashtable):
    """Test the example from the README, using a dictionary."""
    m = Markov(2, "This_is_.", use_hashtable=use_hashtable)
    log_prob = m.log_probability("This")
    assert math.isclose(log_prob, -6.3767269478986)


@pytest.mark.parametrize("use_hashtable", [True, False])
def test_markov_readme_k3(use_hashtable):
    """Test the example from the README, using a dictionary."""
    m = Markov(3, "This_is_.", use_hashtable=use_hashtable)
    log_prob = m.log_probability("This")
    assert math.isclose(log_prob, -6.782192056006)


TEST_DATA = [
    # 0
    # "bush1+2.txt" -> speaker1 file
    # "kerry1+2.txt" -> speaker2 file
    # ""bush-kerry3/BUSH-0.txt" -> unidentified speaker file
    # 2 -> K value
    # "A" -> This what your code should determine who the speaker really is
    # (-2.1670591295191572, -2.2363636778055525) -> expected probabilites
    (
        "bush1+2.txt",
        "kerry1+2.txt",
        "bush-kerry3/BUSH-0.txt",
        2,
        "A",
        -2.1670591295191572,
        -2.2363636778055525,
    ),
    # 1
    # "bush1+2.txt" -> speaker1 file
    # "kerry1+2.txt" -> speaker2 file
    # "bush-kerry3/KERRY-0.txt" -> unidentified speaker file
    # 2 -> K value
    # "B" -> This what your code should determine who the speaker really is
    # (-2.250501358542073, -2.151522255004497) -> expected probabilites
    (
        "bush1+2.txt",
        "kerry1+2.txt",
        "bush-kerry3/KERRY-0.txt",
        2,
        "B",
        -2.250501358542073,
        -2.151522255004497,
    ),
    # 2
    # "bush1+2.txt" -> speaker1 file
    # "kerry1+2.txt" -> speaker2 file
    # "bush-kerry3/BUSH-10.txt" -> unidentified speaker file
    # 1 -> K value
    # "A" -> This what your code should determine who the speaker really is
    # (-2.4587597756771893, -2.4817352688426397) -> expected probabilites
    (
        "bush1+2.txt",
        "kerry1+2.txt",
        "bush-kerry3/BUSH-10.txt",
        1,
        "A",
        -2.4587597756771893,
        -2.4817352688426397,
    ),
    # 3
    # "obama1+2.txt" -> speaker1 file
    # "mccain1+2.txt" -> speaker2 file
    # "obama-mccain3/MCCAIN-5.txt" -> unidentified speaker file
    # 2 -> K value
    # "A" -> This what your code should determine who the speark really is
    # (-1.695522966555955, -1.7481812967778005) -> expected probabilites
    (
        "obama1+2.txt",
        "mccain1+2.txt",
        "obama-mccain3/MCCAIN-5.txt",
        2,
        "A",
        -1.695522966555955,
        -1.7481812967778005,
    ),
    # 4
    # "obama1+2.txt" -> speaker1 file
    # "mccain1+2.txt" -> speaker2 file
    # "obama-mccain3/OBAMA-15.txt" -> unidentified speaker file
    # 3 -> K value
    # "A" -> This what your code should determine who the speark really is
    # (-2.138910249777975, -2.3049185686282305) -> expected probabilites
    (
        "obama1+2.txt",
        "mccain1+2.txt",
        "obama-mccain3/OBAMA-15.txt",
        3,
        "A",
        -2.138910249777975,
        -2.3049185686282305,
    ),
]


@pytest.mark.parametrize("use_hashtable", [True, False])
@pytest.mark.parametrize("fileA, fileB, fileC, k, expected, prob1, prob2", TEST_DATA)
def test_probabilities(fileA, fileB, fileC, k, expected, prob1, prob2, use_hashtable):
    fileA = pathlib.Path(__file__).parent / "speeches" / fileA
    fileB = pathlib.Path(__file__).parent / "speeches" / fileB
    fileC = pathlib.Path(__file__).parent / "speeches" / fileC

    actual = identify_speaker(
        fileA.read_text(), fileB.read_text(), fileC.read_text(), k, use_hashtable
    )

    # Check to make sure a tuple was returned by identify_speaker
    if not isinstance(actual, tuple):
        s = "Actual value returned from identify_speaker must be a tuple"
        pytest.fail(s)

    # Check to make sure three items were retrned by identify_speaker
    if len(actual) != 3:
        s = (
            "Actual value returned from identify_speaker must be a "
            "tuple of three components"
        )
        pytest.fail(s)

    (prob_a, prob_b, got_speaker) = actual

    # Check to to see if the speaker returned by identify_speaker
    # matches the expected speaker

    if got_speaker != expected:
        pytest.fail(
            f"actual speaker ({got_speaker}) and expected speaker "
            f"({expected}) values do not match, use_hashtable=({use_hashtable})"
        )

    # Check to to see if the probabilities returned by identify_speaker
    # matches the expected probabilities

    if not math.isclose(prob_a, prob1):
        s = (
            "actual speaker probability A ({}) and expected probability "
            "({}) values do not match, use_hashtable=({use_hashtable})"
        )
        pytest.fail(s.format(prob_a, prob1))

    if not math.isclose(prob_b, prob2):
        s = (
            "actual speaker probability B ({}) and expected probability "
            " ({}) values do not match, use_hashtable=({use_hashtable})"
        )
        pytest.fail(s.format(prob_b, prob2))
