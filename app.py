from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'notmuchofasecret'
debug = DebugToolbarExtension(app)

# responses = []

survey = satisfaction_survey

@app.route('/')
def start():
    # responses.clear()
    return render_template('start.html', title=survey.title, instructions=survey.instructions)

@app.route('/session_init')
def session_init():
    responses = []
    session['responses'] = responses
    return redirect('/questions/0')

@app.route('/questions/<int:index>')
def question(index):
    responses = session['responses']
    questions_answered = len(responses)
    if not index == questions_answered:
        flash('Naughty, naughty! No attempting access questions out of order!')
        return redirect('/questions/' + str(questions_answered))
    question = survey.questions[index]
    return render_template('question.html', title=survey.title, question=question.question, choices=question.choices, index=index)

@app.route('/answer', methods=['POST'])
def answer():
    answer = request.form.get('answer')
    index = int(request.form.get('index'))
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    next_index = index + 1
    if next_index >= len(survey.questions):
        return redirect('/end')
    else:
        return redirect('/questions/' + str(next_index))

@app.route('/end')
def end():
    return render_template('end.html')