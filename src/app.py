from flask import Flask, render_template, request, jsonify
from modeling.outcomes_quiz import outcome_model as om
from modeling.outcomes_quiz import prettify_output as p
import pandas as pd
import numpy as np
import json
import sys
import cPickle as pickle
import requests
import final_questions as fq
app = Flask(__name__)


def load_model(filename):
    """
    Loads and returns trained sklearn random forest model.

    Parameters
    ----------
    filename: str
        The filename/path of the pickled model

    Returns
    -------
    model:
        Trained sklearn random forest model
    """
    with open(filename) as f:
        model = pickle.load(f)
    return model


def make_field_dicts(classes, probas):
    """
    Returns a dictionary with field_of_study: probabilities key-value pairs.
    Can be used to make a dictionary for any sklearn model that outputs an
    array of the classes being predicted and a prediction array of
    probabilities.

    Only works for a single prediction at a time.

    Parameters
    ----------
    classes: 1d numpy array
        The array of classes (strs) being classified by an sklearn model

    probas: 1d numpy array
        The array of probabilities output by an sklearn model for a single
        input.

    Returns
    -------
    field_dict: dictionary
        field_of_study(str):proba(float) key-value pairs.
    """
    field_dict = {}
    for label, proba in zip(classes, probas.reshape(-1,)):
        field_dict[label] = proba
    return field_dict


def parse_interest_ans(answer_list):
    """
    Returns an array of the user's answers formatted for the model to be able
    to make a prediction on it.

    Parses the user answers data sent from the ajax call and changes the
    format, by converting the individual answers from str to int, to one that
    the sklearn model can predict on.

    Parameters
    ----------
    answer_list: list
        The list sent from the ajax call

    Returns
    -------
    model_format_array: numpy array
        Numpy array of 0s and 1s (ints) representing the user's answers
    """
    for i, ans in enumerate(answer_list):
        answer_list[i] = int(ans)
    model_format_array = np.array(answer_list).reshape(1, -1)
    return model_format_array


def calculate_scores(answer_list):
    """
    Returns the score (float) of the user's answers to the risk tolerance and
    income desire questions.

    Parses the user answer data sent from the ajax call and changes the format,
    by converting the individual answers to floats, then sums the score of the
    user's answers.

    Parameters
    ----------
    answer_list: list
        The list sent from the ajax call

    Returns
    -------
    score: float
        The score of the user on the risk tolerance/income desire questions
    """
    for i, ans in enumerate(answer_list):
        answer_list[i] = float(ans)
    np_arr = np.array(answer_list)
    return np.sum(np_arr)


@app.route('/', methods=['GET'])
def index():
    """
    Returns the home page of the project in response to a GET request

    Parameters
    ----------
    None

    Returns
    -------
    rendered index.html page
    """
    return render_template('index.html')


@app.route('/score', methods=['POST'])
def score():
    """
    Returns the recommended majors in response to a POST request containing
    the user's answers to the quiz.

    Parameters
    ----------
    request: POST request data
        JSON string representing array

    Returns
    -------
    JSON dict:
        'table': html formatted pandas dataframe key-value pair
        Table contains the major recommendations to be shown to user
    """
    quiz_answers = request.json
    int_answers, risk_ans, inc_ans = (quiz_answers[0],
                                      quiz_answers[1],
                                      quiz_answers[2])
    answer_array = parse_interest_ans(int_answers)
    risk_score = calculate_scores(risk_ans)
    inc_score = calculate_scores(inc_ans)
    classes = model.classes_
    probas = model.predict_proba(answer_array)
    field_dict = make_field_dicts(classes, probas)
    final_df = om.calculate_final_prob(job_df,
                                       risk_score,
                                       inc_score,
                                       field_dict
                                       ).sort_values(by='final_probs',
                                                     ascending=False)
    pretty_columns = p.prettified_columns
    final_columns = p.final_columns
    pretty_df = p.prettify_final_output(final_df,
                                        pretty_columns,
                                        final_columns,
                                        20)

    return jsonify({'table': pretty_df.to_html(index=False, classes='table')})


@app.route('/quiz', methods=['GET'])
def quiz():
    """
    Returns the quiz page of the project in response to a GET request

    Parameters
    ----------
    None

    Returns
    -------
    rendered quiz.html page
    """
    return render_template('quiz.html',
                           questions=fq.interest_questions,
                           risk_questions=fq.risk_questions,
                           income_desire_questions=fq.income_desire_questions
                           )

model = load_model('modeling/interest_quiz/firstmodel.pkl')
job_df = pd.read_csv('../data/abt_ver1.csv')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
