from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickens-are-cool"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES = "responses"

QUESTIONS = {
    0: satisfaction_survey.questions[0].question,
    1: satisfaction_survey.questions[1].question,
    2: satisfaction_survey.questions[2].question,
    3: satisfaction_survey.questions[3].question
}


@app.route('/')
def show_title_page():   
    title = satisfaction_survey.title
    info = satisfaction_survey.instructions
    
    return render_template("begin-survey.html", title=title, info=info)

@app.route('/list', methods=["POST"])
def make_list():
    session[RESPONSES] = []
    return redirect("/questions/0")

@app.route('/questions/<int:id>')
def show_questions(id):
    responses = session.get(RESPONSES)
    
    if id == len(responses):
        question = QUESTIONS[id]
        choice_1 = satisfaction_survey.questions[id].choices[0]
        choice_2 = satisfaction_survey.questions[id].choices[1]
        return render_template("questions.html", question=question, choice_1=choice_1, choice_2=choice_2)
    
    if id > len(responses) or id < len(responses):
        flash("Invalid URL! You've been redirected back to the survey.")
        return redirect(f'/questions/{len(responses)}')
    
    

@app.route('/answer', methods=["POST"])
def save_answer():
    
    answer = request.form["choices"]
    responses = session[RESPONSES]
    responses.append(answer)
    session[RESPONSES] = responses
    
    if len(responses) == len(QUESTIONS):
        return redirect('/completed')
    if len(responses) != len(QUESTIONS):
        return redirect(f'/questions/{len(responses)}')

@app.route('/completed')
def say_thanks():
    return render_template("completed.html")



    

