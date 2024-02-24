from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    first_choices = []
    second_choices = []
    for i in range(1, 8):
        first_choices.append(request.form[f'class{i}_first_choice'])
        second_choices.append(request.form[f'class{i}_second_choice'])
    return f'First choice classes: {first_choices} \n Second choice classes: {second_choices}'

if __name__ == '__main__':
    app.run(debug=True)