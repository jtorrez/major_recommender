from flask import Flask, render_template, request, jsonify
import numpy as np
import json
import sys
import cPickle as pickle
import requests
import final_questions as fq
app = Flask(__name__)

#need to fix how to dynamically update fields
fields = []

def load_model(filename):
    with open(filename) as f:
        model = pickle.load(f)
    return model

def make_field_dicts(classes, probas):
    del fields[:]
    for label, proba in zip(model.classes_, probas.reshape(-1,)):
        fields.append({'field':label, 'probability':proba})

def parse_quiz_json(answer_list):
    for i, ans in enumerate(answer_list):
        answer_list[i] = int(ans)
    model_format_array = np.array(answer_list).reshape(1, -1)
    return model_format_array

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
                           questions=fq.interest_questions,
                           risk_questions=fq.risk_questions,
                           income_desire_questions=fq.income_desire_questions,
                           fields=fields)

@app.route('/score', methods=['POST'])
def score():
    quiz_answers = request.json
    answer_array = parse_quiz_json(quiz_answers)
    classes = model.classes_
    probas = model.predict_proba(answer_array)
    make_field_dicts(classes, probas)
    return 'OK'

@app.route('/project', methods=['GET'])
def project():
    return render_template('project.html')

@app.route('/author', methods=['GET'])
def author():
    return render_template('author.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')





if __name__ == '__main__':
    filename = sys.argv[1]
    model = load_model(filename)
    app.run(host='0.0.0.0', port=8080, debug=True)
