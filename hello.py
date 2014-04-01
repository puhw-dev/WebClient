from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, this is first view, or maybe the second? ;-)"

@app.route("/templating")
def templating():
    app.logger.debug("Omg, I'm loggin somethin... ;-)")
    return render_template('hello.html', name="Wiktorek")

@app.route("/json")
def json():
    tab = ['a', 'b']
    return tab 

if __name__ == "__main__":
    app.run(use_debugger=True, use_reloader=True, debug=True)
