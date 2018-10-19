from flask import Flask, render_template, send_from_directory, request, jsonify
import json


app = Flask(__name__, static_folder='static', static_url_path='')


@app.route('/js/jquery-3.3.1.js')
def jsfile():
    return send_from_directory('static/js', 'jquery-3.3.1.js')


@app.route('/js/bootstrap.min.js')
def jsbootstrapfile():
    return send_from_directory('static/js', 'bootstrap.min.js')


@app.route('/css/bootstrap.min.css')
def cssbootstrapfile():
    return send_from_directory('static/css', 'bootstrap.min.css')


@app.route('/')
def index():
    return render_template('index.html')

app.run(host='localhost', port="5000")
