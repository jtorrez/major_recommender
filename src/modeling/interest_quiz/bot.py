from __future__ import division
import random
import numpy as np
import pandas as pd
import cleaning as cl
import raw_loyola
import sys
import operator
import copy
from collections import Counter


class LoyolaQuizBot(object):
    def __init__(self, raw_data, fields_dict):
        self.raw_data = raw_data
        self.fields_dict = fields_dict
        self.i_c = 2
        self.clean_data = cl.majors_string_to_list(self.raw_data)
        self.majors_set = cl.all_majors(self.clean_data)
        self.mapped_lst = cl.create_labels(self.clean_data, self.fields_dict)

    def one_quiz(self):
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

    def _sample_field_distribution(self, num_samples, field_probs):
        """
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
        """
        cols = []

        for i in xrange(num_questions):
            col_name = 'q' + str(i+1)
            cols.append(col_name)

        return cols

    def _build_single_dataframe(self, bot_answers, labels, col_names, quiz_num, field_probs):
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

    def multi_quiz(self, num_times, num_questions, num_samples, run_check=1000):
        """
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
            if quiz_num % run_check == 0:
                print "I've taken the quiz {} times!\n".format(quiz_num)

        correct_order_cols = cols + ['labels', 'quiz_num'] + proba_col_names

        return running_df[correct_order_cols]

    def multi_quiz_and_write_file(self, num_times, num_questions, num_samples, filename, run_check=1000):
        """
        """
        final_df = self.multi_quiz(num_times, num_questions, num_samples, run_check)
        print "Finished taking quiz, writing file\n"
        final_df.to_csv(filename, index=False)
        print "Successfully wrote a file to {}".format(filename)

if __name__ == '__main__':
    num_times = int(sys.argv[1])
    num_samples = int(sys.argv[2])
    num_questions = int(sys.argv[3])
    filename = sys.argv[4]

    quiz_bot = LoyolaQuizBot(raw_loyola.get_raw_data(), cl.get_fields_dict())
    quiz_bot.multi_quiz_and_write_file(num_times, num_questions, num_samples, filename)
