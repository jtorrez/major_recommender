from __future__ import division
import random
import numpy as np
import pandas as pd
import cleaning as cl
import operator
import copy
from collections import Counter


class QuizBot(object):
    def __init__(self, raw_data, fields_dict):
        self.raw_data = raw_data
        self.fields_dict = fields_dict
        self.clean_data = cl.majors_string_to_list(self.raw_data)
        self.majors_set = cl.all_majors(self.clean_data)
        self.mapped_lst = cl.create_labels(self.clean_data, self.fields_dict)



def one_quiz(mapped_lst, i_c):
    """
    Returns the bot's answers to a single quiz, the raw sum of probabilities
    of the different fields, and the field probabilities.

    Takes the Loyola quiz once given the mapped list containing primary and
    secondary (field, probability) tuple at the input indices.

    Parameters
    ----------
    mapped_lst: list

    i_c: int
        Index of Counter dictionary containing field of study counts associated
        with each question

    Returns
    -------
    bot_answers: list
        The answers of the bot to the quiz. 1 = True answer and 0 = False
        answer to the quiz question.

    total_counts: Counter dictionary
        field_of_study(str):raw_counts(int) key-value pairs.

    field_probs: Counter dictionary
        field_of_study(str):prob(float) key-value pairs.
    """
    bot_answers = []
    field_occurences = []
    for question in mapped_lst:
        rand_bool = random.choice([True, False])
        bot_answers.append(int(rand_bool))
        if rand_bool:
            field_occurences.append(question[i_c])
    total_counts = reduce(operator.add, field_occurences)
    field_probs = make_weight_counter(total_counts)

    return bot_answers, field_probs

def make_weight_counter(cnter_dict):
    """
    Returns a new counter dictionary where the counts of the occurence of each
    field of study have been converted to weights (percentages).

    Parameters
    ----------
    cnter_dict: Counter dictionary
        field_of_study(str):count(int) key-value pairs.

    weight_dict: Counter dictionary
        field_of_study(str):weight(float) key-value pairs.
    """
    weight_dict = copy.deepcopy(cnter_dict)

    total = np.sum(weight_dict.values())

    for k,v in weight_dict.iteritems():
        weight_dict[k] = v / total

    return weight_dict

def sample_field_distribution(num_samples, field_probs):
    """
    """
    fields = []
    weights = []

    for field, prob in field_probs.iteritems():
        fields.append(field)
        weights.append(prob)
    labels = np.random.choice(fields, size=num_samples, p=weights)

    return labels

def make_column_names(num_questions):
    """
    """
    cols = []

    for i in xrange(num_questions):
        col_name = 'q' + str(i+1)
        cols.append(col_name)

    return cols

def build_single_dataframe(bot_answers, labels, col_names, quiz_num, field_probs):
    """
    """
    size = labels.shape[0]
    df = pd.DataFrame([bot_answers], index=range(size), columns=col_names)
    df['labels'] = labels
    df['quiz_num'] = np.full(size, quiz_num, dtype=int)
    proba_col_names = []
    for k, v in field_probs.iteritems():
        col_name = k.lower().replace(' ', '_').replace(',', '') + '_proba'
        df[col_name] = np.full(size, field_probs[k], dtype=float)
        proba_col_names.append(col_name)

    return df, proba_col_names

def take_quiz(num_times, num_questions, num_samples, mapped_lst, i_c):
    """
    """
    cols = make_column_names(num_questions)

    for quiz_num in xrange(1, num_times+1):
        bot_answers, field_probs = one_quiz(mapped_lst, i_c)
        labels = sample_field_distribution(num_samples, field_probs)
        single_df, proba_col_names = build_single_dataframe(bot_answers,
                                                            labels,
                                                            cols,
                                                            quiz_num,
                                                            field_probs)
        if quiz_num == 1:
            running_df = copy.deepcopy(single_df)
        else:
            running_df = running_df.append(single_df, ignore_index=True)

    correct_order_cols = cols + ['labels', 'quiz_num'] + proba_col_names

    return running_df[correct_order_cols]

def take_quiz_and_write_file(num_times, num_questions, num_samples, mapped_lst, i_c, filename):
    final_df = take_quiz(num_times, num_questions, num_samples, mapped_lst, i_c)
    final_df.to_csv(filename, index=False)
