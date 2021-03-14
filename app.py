from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'notmuchofasecret'
debug = DebugToolbarExtension(app)

survey = satisfaction_survey

@app.route('/')
def start():
    # display the survey start page
    return render_template('start.html', title=survey.title, instructions=survey.instructions)      # could have passed in the survey object to shorten this up

@app.route('/session_init')
def session_init():
    # reset the session to an empty list
    responses = []
    session['responses'] = responses        # could have just set to [] instead of declaring a variable

    # ask for the first question in the survey
    return redirect('/questions/0')

@app.route('/questions/<int:index>')
def question(index):
    # get the list of responses from the session
    responses = session['responses']
    # check how many questions have been answered, we'll use this to make sure the user isn't accessing question out of order or that don't exist
    questions_answered = len(responses)
    if not index == questions_answered:
        flash('Naughty, naughty! No attempting access questions out of order!')
        return redirect('/questions/' + str(questions_answered))
    # get and display the requested question
    question = survey.questions[index]
    return render_template('question.html', title=survey.title, question=question.question, choices=question.choices, index=index)      # could have shortened this by passing in the question object

@app.route('/answer', methods=['POST'])
def answer():
    # get the user's answer from the form
    answer = request.form.get('answer')
    # get the hidden question index from the form. this is used to track which question is being answesred and what the next question is, could have used the len(responses) to do the same thing
    index = int(request.form.get('index'))
    # get the session responses, append the current answer, and update the session
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    # determine the next question id
    next_index = index + 1
    #check if the user has answered all the questions
    if next_index >= len(survey.questions):
        return redirect('/end')
    else:
        return redirect('/questions/' + str(next_index))

@app.route('/end')
def end():
    return render_template('end.html')