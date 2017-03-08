"""
Bot class built to take Loyola University of Chicago quiz.

This class was built for my capstone project for the Galvanize data science
immersive in order to make the process I used to synthesize my dataset
transparent and repeatable.

You can use this script to create your own data set by running the following
command in your terminal:

$ > python <num_times> <num_samples> <num_questions> <out_filename>

num_times:
    The number of times you want to the bot to take the quiz
num_samples:
    The number of samples that you would like the bot to take from the
    probability distribution given the field probabilities given by
    each time it takes the quiz.
num_questions: int
    The number of questions in your quiz.
out_filename:
    The desired filename for the output csv file.

TODO/Future Work
-----------
- Upgrade __name__ == __main__ block to use ArgumentParser to take in
  command line arguments.
- Optimize multi-quiz. The bot slowed as the number of times it had to take
  the quiz increased, most likely from having to continually overwrite the
  running_df and store that in memory.
- Fix hardcoding of i_c (index of Counter dictionary) used in cleaning.
  Methods of this class were originally not written encapsulated in a class
  and I'd like to re-visit the usefulness of this later.
- Revisit hardcoding of cleaning script that creates class attributes.
- Make a QuizBot parent class that this class could inherit from. This
  would allow some flexibility to easily build a bot that can take online
  quizzes with just some minor modifications
"""

from __future__ import division
import random
import numpy as np
import pandas as pd
import interests_cleaning as cl
import raw_loyola
import sys
import operator
import copy
from collections import Counter


class LoyolaQuizBot(object):
    """Bot built to take Loyola University of Chicago quiz.

    Attributes
    ----------
    raw_data:
    fields_dict
    i_c
    clean_data
    majors_set
    mapped_lst

    Methods
    -------
    tbd
    """
    def __init__(self, raw_data, fields_dict):
        self.raw_data = raw_data
        self.fields_dict = fields_dict
        self.i_c = 2
        self.clean_data = cl.majors_string_to_list(self.raw_data)
        self.majors_set = cl.all_majors(self.clean_data)
        self.mapped_lst = cl.create_labels(self.clean_data, self.fields_dict)

    def one_quiz(self):
        """
        Returns the bot's answers to a single quiz and the field probabilities.

        Takes the Loyola quiz once using self.mappedlst.

        Parameters
        ----------
        None

        Returns
        -------
        bot_answers: list
            The answers of the bot to the quiz. 1 = True answer and 0 = False
            answer to the quiz question.

        field_probs: Counter dictionary
            field_of_study(str):prob(float) key-value pairs.
        """
        bot_answers = []
        field_occurences = []
        for question in self.mapped_lst:
            rand_bool = random.choice([True, False])
            bot_answers.append(int(rand_bool))
            if rand_bool:
                field_occurences.append(question[self.i_c])
        total_counts = reduce(operator.add, field_occurences)
        field_probs = self._make_weight_counter(total_counts)

        return bot_answers, field_probs

    def _make_weight_counter(self, cnter_dict):
        """
        Returns a new counter dictionary where the counts of the occurence of
        each field of study have been converted to weights (percentages).

        Parameters
        ----------
        cnter_dict: Counter dictionary
            field_of_study(str):count(int) key-value pairs.

        Returns
        -------
        weight_dict: Counter dictionary
            field_of_study(str):weight(float) key-value pairs.
        """
        weight_dict = copy.deepcopy(cnter_dict)

        total = np.sum(weight_dict.values())

        for k, v in weight_dict.iteritems():
            weight_dict[k] = v / total

        return weight_dict

    def _sample_field_distribution(self, num_samples, field_probs):
        """
        Returns a numpy array of labels sampled from probability distribution
        given by the field_probs dictionary.

        Parameters
        ----------
        num_samples: int
             The number of samples to draw from the distribution

        field_probs: Counter dictionary
            field_of_study(str):prob(float) key-value pairs.

        Returns
        -------
        labels: numpy array of shape = (num_samples,)
            Labels randomly sampled from probability distribution
        """
        fields = []
        weights = []

        for field, prob in field_probs.iteritems():
            fields.append(field)
            weights.append(prob)
        labels = np.random.choice(fields, size=num_samples, p=weights)

        return labels

    def _make_column_names(self, num_questions):
        """
        Returns a list of column names given the num_questions to analyze.

        Parameters
        ----------
        num_questions: int
            The number of questions in the quiz.

        Returns
        -------
        cols: list
            List of column names(str) with format q1, q2, ..., qn
            where n = num_questions.

            ex: num_questions = 3
                cols = ['q1', 'q2', 'q3']
        """
        cols = []

        for i in xrange(num_questions):
            col_name = 'q' + str(i+1)
            cols.append(col_name)

        return cols

    def _build_single_dataframe(self, bot_answers, labels,
                                col_names, quiz_num, field_probs):
        """
        Returns a single dataframe and the names of the probabilities for each
        label being predicted.

        Parameters
        ----------
        bot_answers: list
            List of len(num_questions) with the answers from the bot taking
            the quiz once. Answers are either 1 = True or 0 = False.

        labels: numpy array of shape = (num_samples,)
            Labels randomly sampled from probability distribution

        col_names: list
            List of len(num_questions) with strings in the format q1, ..., qn
            where n = num_questions

        quiz_num: int
            The iteration number of the bot taking the quiz.

        field_probs: Counter dictionary
            field_of_study(str):prob(float) key-value pairs.

        Returns
        -------
        df: Pandas dataframe
            Dataframe containing all pertinent information about each
            observation of the bot taking the quiz/sampling a label.

        proba_col_names: list
            List of converted label names for use in making final dataframe.
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

    def multi_quiz(self, num_times, num_questions, num_samples, it_check=1000):
        """
        Returns a dataframe containing all pertinent information about each
        observation of the bot taking the quiz/sampling a label. There will be
        num_times * num_questions rows in the dataframe.

        Parameters
        ----------
        num_times: int
            The number of times you would like the bot to take the quiz.

        num_questions: int
            The number of questions in your quiz.

        num_samples: int
            The number of samples that you would like the bot to take from the
            probability distribution given the field probabilities given by
            each time it takes the quiz.

        it_check: int, optional(default=1000)
            Allows you to have the bot print it's progress at each iteration
            divisible by it_check.

            ex: it_check = 1000, prints every 1000 iterations

        Returns
        -------
        running_df: Pandas dataframe
            Dataframe containing all pertinent information about each
            observation of the bot taking the quiz/sampling a label for the
            entire run.
        """
        cols = self._make_column_names(num_questions)

        for quiz_num in xrange(1, num_times+1):
            bot_answers, field_probs = self.one_quiz()
            labels = self._sample_field_distribution(num_samples, field_probs)
            single_df, proba_col_names = self._build_single_dataframe(
                                                                bot_answers,
                                                                labels,
                                                                cols,
                                                                quiz_num,
                                                                field_probs)
            if quiz_num == 1:
                running_df = copy.deepcopy(single_df)
            else:
                running_df = running_df.append(single_df, ignore_index=True)
            if quiz_num % it_check == 0:
                print "I've taken the quiz {} times!\n".format(quiz_num)

        correct_order_cols = cols + ['labels', 'quiz_num'] + proba_col_names

        return running_df[correct_order_cols]

    def multi_quiz_and_write_file(self, num_times, num_questions,
                                  num_samples, out_filename, it_check=1000):
        """
        Writes a csv file containing all pertinent information about each
        observation of the bot taking the quiz/sampling a label. There will be
        num_times * num_questions lines in the file.

        Parameters
        ----------
        num_times: int
            The number of times you would like the bot to take the quiz.

        num_questions: int
            The number of questions in your quiz.

        num_samples: int
            The number of samples that you would like the bot to take from the
            probability distribution given the field probabilities given by
            each time it takes the quiz.

        out_filename: str
            The desired filename path of the output csv file.

        it_check: int, optional(default=1000)
            Allows you to have the bot print it's progress at each iteration
            divisible by it_check.

            ex: it_check = 1000, prints every 1000 iterations

        Returns
        -------
        None
        """
        final_df = self.multi_quiz(num_times, num_questions,
                                   num_samples, it_check)
        print "Finished taking quiz, writing file\n"
        final_df.to_csv(out_filename, index=False)
        print "Successfully wrote a file to {}".format(out_filename)

if __name__ == '__main__':
    num_times = int(sys.argv[1])
    num_samples = int(sys.argv[2])
    num_questions = int(sys.argv[3])
    out_filename = sys.argv[4]

    quiz_bot = LoyolaQuizBot(raw_loyola.get_raw_data(), cl.get_fields_dict())
    quiz_bot.multi_quiz_and_write_file(num_times,
                                       num_questions,
                                       num_samples,
                                       out_filename)
