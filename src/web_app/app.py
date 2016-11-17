from flask import Flask, render_template, request, jsonify
import json
import requests
import final_questions as fq
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html', questions=fq.questions)

@app.route('/score', methods=['POST'])
def score():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
