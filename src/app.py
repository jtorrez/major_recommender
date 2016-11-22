from flask import Flask, render_template, request, jsonify
from modeling.outcomes_quiz import outcome_model as om
import pandas as pd
import numpy as np
import json
import sys
import cPickle as pickle
import requests
import final_questions as fq
app = Flask(__name__)


def load_model(filename):
    with open(filename) as f:
        model = pickle.load(f)
    return model

def make_field_dicts(classes, probas):
    field_dict = {}
    for label, proba in zip(model.classes_, probas.reshape(-1,)):
        field_dict[label] = proba
    return field_dict

def parse_interest_ans(answer_list):
    for i, ans in enumerate(answer_list):
        answer_list[i] = int(ans)
    model_format_array = np.array(answer_list).reshape(1, -1)
    return model_format_array

def calculate_scores(answer_list):
    for i, ans in enumerate(answer_list):
        answer_list[i] = float(ans)
    np_arr = np.array(answer_list)
    return np.sum(np_arr)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/score', methods=['POST'])
def score():
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
    return jsonify({'table':final_df.to_html(index=False, classes='table')})

@app.route('/quiz', methods=['GET'])
def project():
    return render_template('quiz.html',
                           questions=fq.interest_questions,
                           risk_questions=fq.risk_questions,
                           income_desire_questions=fq.income_desire_questions
                           )


if __name__ == '__main__':
    filename = sys.argv[1]
    model = load_model(filename)
    job_df = pd.read_csv('../data/abt_ver1.csv')
    app.run(host='0.0.0.0', port=8080, debug=True)
