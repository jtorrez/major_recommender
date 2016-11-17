from flask import Flask, render_template, request, jsonify
import json
import requests
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    questions = [
    {'question' : 'a question',
     'question_num' : 'q3'
     },
    {'question' : 'another question',
     'question_num' : 'q4'}
    ]
    return render_template('home.html', questions=questions)

@app.route('/score', methods=['POST'])
def score():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
