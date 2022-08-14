from flask import Flask, render_template, url_for, request, redirect
import data_manager

app = Flask(__name__)

@app.route('/')
def home_five_question():
    questions = data_manager.home_five_question()
    return render_template("index.html",
                           data=questions,
                           title="Last five questions...")

@app.route('/list')
def all_question():
    questions = data_manager.list_questions()
    return render_template("index.html",
                           data=questions,
                           title="All questions...")

@app.route('/add-question', methods=["GET"])
def route_question():

    return render_template("add_question.html",
                           title="Add question")

@app.route('/add_question', methods=["POST"])
def add_question():
    new_question = {"view_number": 0,
                    "vote_number": 0,
                    "title": request.form.get("title"),
                    "message": request.form.get("message"),
                    "image": None}
    data_manager.add_new_data(new_question, 'question')

    return redirect('/list')

@app.route('/question/<int:question_id>')
def display_question(question_id):
    question = data_manager.display_question(question_id)


    return render_template("index.html",
                           question_id=question_id,
                           question=question,
                           #answers=answers,
                           #comments=comments,
                           title="Display question")

if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True
    )
