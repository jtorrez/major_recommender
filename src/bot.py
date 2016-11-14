from __future__ import division
import random
import numpy as np
import cleaning as cl
from collections import Counter


def one_quiz(mapped_lst, i_p, i_s):
    """
    Returns the bot's answers to a single quiz, the raw sum of probabilities
    of the different fields, and the field probabilities.

    Takes the Loyola quiz once given the mapped list containing primary and
    secondary (field, probability) tuple at the input indices.

    Parameters
    ----------
    mapped_lst: list

    i_p: int
        Index of primary label tuple of format (label: str, prob: float)

    i_s: int
        Index of secondary label tuple of format (label: str, prob: float).
        The secondary label can be set to None or contain a value.

    Returns
    -------
    bot_answers: list
        The answers of the bot to the quiz. 1 = True answer and 0 = False
        answer to the quiz question.

    raw: Counter dictionary
        field_of_study(str):sum_probs(float) key-value pairs.

    field_probs: Counter dictionary
        field_of_study(str):prob(float) key-value pairs.
    """
    raw = Counter()
    bot_answers = []
    for question in mapped_lst:
        rand_bool = random.choice([True, False])
        bot_answers.append(int(rand_bool))
        if rand_bool:
            raw[question[i_p][0]] = raw.get(question[i_p][0], 0.0) +\
                                                            question[i_p][1]
            if question[i_s]:
                raw[question[i_s][0]] = raw.get(question[i_s][0], 0.0)\
                                                          + question[i_s][1]
    field_probs = cl.make_weight_counter(raw)

    return bot_answers, raw, field_probs
