from flask import Flask, render_template, url_for, request, redirect, session, escape, flash
import data_manager
import util
import pass_hash
from werkzeug.utils import secure_filename
app = Flask(__name__)

app.secret_key = 'abcd123'

@app.route('/')
def home_five_question():
    questions = data_manager.home_five_question()
    email = None
    if 'email' in session:
        email = escape(session['email'])
    return render_template("index.html",
                           data=questions,
                           title="Last five questions...",
                           email=email)

@app.route('/registration', methods=['GET', 'POST'])
def sign_up():
    email = None
    if 'email' in session:
        return redirect('/')
    if request.method == 'POST':
        email = request.form['email']
        password = pass_hash.hash_password(request.form['password'])
        data_manager.add_new_user(email, password)
        return redirect('/')
    return render_template("registration.html", email=email)

@app.route('/list')
def all_question():
    order_by_options = {'submission_time': 'Submission time', 'view_number': 'View number',
                        'vote_number': 'Vote number', 'title': 'Title'}
    order_options = ['DESC', 'ASC']
    order_by = request.args.get('order_by')
    order = request.args.get('order')
    questions = util.order_questions(order_by, order)
    return render_template("index.html",
                           data=questions,
                           title="List questions",
                           select_options=order_by_options,
                           order_options=order_options,
                           order_by=order_by,
                           order=order)

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


    return render_template("display_question.html",
                           question_id=question_id,
                           question=question,
                           #answers=answers,
                           #comments=comments,
                           title="Display question")

@app.route('/question/<int:question_id>/vote')
def vote_for_question(question_id):
    vote_type = request.args.get('vote_type')
    title = request.args.get('title')
    vote_number = data_manager.get_question_vote_number(question_id)
    increases_or_decreases_vote_number = util.vote_up_or_down(vote_number, vote_type)
    data_manager.update_question_vote_number(question_id, increases_or_decreases_vote_number)
    if title == 'Main page':
        return redirect(url_for("home_five_question"))
    return redirect(url_for("all_question"))

@app.route('/question/<int:question_id>/edit', methods=["GET"])
def route_edit_question(question_id):
    question_to_edit = data_manager.route_edit_question(question_id)

    return render_template("edit_question.html",
                           title="Edit question",
                           question=question_to_edit,
                           question_id=question_id)

@app.route('/question/<question_id>/edit', methods=["POST"])
def edit_question(question_id):
    edited_title = request.form['title']
    edited_message = request.form['message']
    data_manager.edit_question(question_id, edited_title, edited_message)

    return redirect(url_for("display_question",
                            question_id=question_id))

@app.route('/question/<question_id>/are-you-sure', methods=["GET"])
def confirm_delete_question(question_id):

    return render_template("confirm_delete_question.html",
                           question_id=question_id,
                           title="Are you sure you want to delete this question?")

@app.route("/users")
def list_users():
    if 'email' in session:
        email = escape(session['email'])
        users_data = data_manager.list_users()
        return render_template("users.html", email=email, users_data=users_data)
    return redirect('/')


@app.route("/login", methods=['GET', 'POST'])
def sign_in():
    email = request.form['email']
    password = request.form['password']
    user_record = data_manager.get_record_by_email(email)
    referrer = request.headers.get("Referer")
    if user_record:
        if pass_hash.verify_password(password, user_record['password']):
            session['email'] = email
            session['userid'] = user_record['userid']
            return redirect(referrer)
        flash("Incorrect username or password!")
        return redirect(referrer)
    else:
        flash("Username doesn't exists!")
        return redirect(referrer)


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True
    )
