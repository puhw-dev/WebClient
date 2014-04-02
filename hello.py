from flask import Flask
from flask import render_template, jsonify, Response
import json
import math
from random import random
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')
    
@app.route("/json_sin")
def json_sin():
    values = [["x", "y"]]
    for x in range(0, 100):
        values.append([x/10., math.sin(x/10.) + random()])
    return Response(json.dumps(values), mimetype='application/json')

if __name__ == "__main__":
    app.run(use_debugger=True, use_reloader=True, debug=True)
