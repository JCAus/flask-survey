from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickens-are-cool"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

QUESTIONS = {
    0: satisfaction_survey.questions[0].question,
    1: satisfaction_survey.questions[1].question,
    2: satisfaction_survey.questions[2].question,
    3: satisfaction_survey.questions[3].question
}


RESPONSES = []

@app.route('/')
def show_title_page():   
    title = satisfaction_survey.title
    info = satisfaction_survey.instructions
    return render_template("begin-survey.html", title=title, info=info)

@app.route('/questions/<int:id>')
def show_questions(id):
    if id == len(RESPONSES):
        question = QUESTIONS[id]
        choice_1 = satisfaction_survey.questions[id].choices[0]
        choice_2 = satisfaction_survey.questions[id].choices[1]
        return render_template("questions.html", question=question, choice_1=choice_1, choice_2=choice_2)
    if id > len(RESPONSES) or id < len(RESPONSES):
        flash("Invalid URL! You've been redirected back to the survey.")
        return redirect(f'/questions/{len(RESPONSES)}')
    
    

@app.route('/answer', methods=["POST"])
def save_answer():
    
    answer = request.form["choices"]
    RESPONSES.append(answer)
    
    if len(RESPONSES) == len(QUESTIONS):
        return redirect('/completed')
    if len(RESPONSES) != len(QUESTIONS):
        return redirect(f'/questions/{len(RESPONSES)}')

@app.route('/completed')
def say_thanks():
    return render_template("completed.html")



    

