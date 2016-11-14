from flask import Flask, render_template, request, jsonify
import json
import requests
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/score', methods=['POST'])
def score():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
