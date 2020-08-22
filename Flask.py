#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('graph.html')

app.run(host='0.0.0.0', debug=True)
