from flask import Flask
from flask import render_template, jsonify, Response
import json
import math
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, this is first view, or maybe the second? ;-)"

@app.route("/templating")
def templating():
    app.logger.debug("Omg, I'm loggin somethin... ;-)")
    return render_template('hello.html', name="Wiktorek")

@app.route("/json_sin")
def json_sin():
    values = [["y", "y"]]
    for x in range(0, 100):
        values.append([x/10., math.sin(x/10.)])
    return Response(json.dumps(values), mimetype='application/json')

if __name__ == "__main__":
    app.run(use_debugger=True, use_reloader=True, debug=True)
