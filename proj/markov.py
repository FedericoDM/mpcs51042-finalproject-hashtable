# Federico Dominguez Molina
# CNET ID: 12351429


# Imports
import math
from hashtable import Hashtable

# Constants
HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2


class Markov:
    def __init__(self, k, text, use_hashtable):
        """
        Construct a new k-order markov model using the text 'text'.
        """
        self.k = k
        self.text = text
        unique_chars = set(text)
        self.len_unique = len(unique_chars)

        if use_hashtable:
            self.model = Hashtable(HASH_CELLS, 0, TOO_FULL, GROWTH_RATIO)
        else:
            self.model = dict()

        index = 0
        while index < len(text):
            # Wrapping around
            final_str, final_str_1 = self.wrap_around_text(text, index)
            # Add strings to model
            strings = [final_str, final_str_1]
            for string in strings:
                if self.model.get(string, 0) != 0:
                    self.model[string] += 1
                else:
                    self.model[string] = 1

            index += 1

    def wrap_around_text(self, text, index):
        """

        Wraps around a specified text

        Parameters
        ----------
        text : str
            Text to analyse
        """

        # Wrapping around
        if index + self.k + 1 >= len(text):
            wrap_around = (index + self.k + 1) - len(text)
            wrap_around_2 = (index + self.k) - len(text)

            final_str_1 = text[index:len(text)] + text[0:(wrap_around)]
            # Check if index + k needs wrap around
            if wrap_around_2 >= 0:
                final_str = text[index:len(text)] + text[0:(wrap_around_2)]
            else:
                final_str = text[index:(index + self.k)]
        else:
            final_str = text[index:index + self.k]
            final_str_1 = text[index:index + self.k + 1]

        return final_str, final_str_1

    def log_probability(self, s):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        """

        index = 0
        sum_log_probs = 0

        index = 0
        while index < len(s):
            # Wrapping around
            final_str, final_str_1 = self.wrap_around_text(s, index)
            # Compute probabilities
            if self.model.get(final_str, 0) != 0:
                n_val = self.model[final_str]
            else:
                n_val = 0

            if self.model.get(final_str_1, 0) != 0:
                m_val = self.model[final_str_1]
            else:
                m_val = 0

            log_prob = math.log((m_val + 1) / (n_val + self.len_unique))
            sum_log_probs += log_prob

            index += 1

        return sum_log_probs


def identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under a "order" order
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.
    """
    # Instantiate models for speech 1 and speech 2
    model1 = Markov(k, speech1, use_hashtable=use_hashtable)
    model2 = Markov(k, speech2, use_hashtable=use_hashtable)

    # Calculate probabilities for speech3
    m1_prob = model1.log_probability(speech3) / len(speech3)
    m2_prob = model2.log_probability(speech3) / len(speech3)

    # Return will depend on probabilities
    if m1_prob > m2_prob:
        return (m1_prob, m2_prob, "A")
    else:
        return (m1_prob, m2_prob, "B")
