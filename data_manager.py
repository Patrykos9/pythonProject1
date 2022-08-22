from psycopg2.extras import RealDictCursor
from datetime import datetime
import connection

@connection.connection_handler
def list_questions(cursor, order_by, order):
    cursor.execute(f"""
                    SELECT * FROM question 
                    ORDER BY {order_by} {order};
                    """)
    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def display_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    question = cursor.fetchall()
    return question

@connection.connection_handler
def home_five_question(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;
                    """)
    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def add_new_data(cursor, dict, type):
    from datetime import datetime
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")

    if type == "question":
        cursor.execute("""
                        INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
                        VALUES(%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);
                         """,
                       {'submission_time': dt,
                        'view_number': dict['view_number'],
                        'vote_number': dict['vote_number'],
                        'title': dict['title'],
                        'message': dict['message'],
                        'image': dict['image']})
    elif type == "answer":
        cursor.execute("""
                        INSERT INTO answer(submission_time, vote_number, question_id, message, image)
                        VALUES(%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s);
                        """,
                       {'submission_time': dt,
                        'vote_number': dict['vote_number'],
                        'question_id': dict['question_id'],
                        'message': dict['message'],
                        'image': dict['image']})

    elif type == "comment":
        cursor.execute("""
                        INSERT INTO comment(question_id, answer_id, message, submission_time, edited_count)
                        VALUES(%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s);
                        """,
                       {'question_id': dict['question_id'],
                        'answer_id': dict['answer_id'],
                        'message': dict['message'],
                        'submission_time': dt,
                        'edited_count': dict['edited_count']})

@connection.connection_handler
def get_question_vote_number(cursor, question_id):
    cursor.execute("""
                    SELECT vote_number FROM question
                    WHERE id = %(question_id)s;
                    """,
                     {'question_id': question_id})
    vote_number = cursor.fetchall()
    return vote_number[0]

@connection.connection_handler
def update_question_vote_number(cursor, question_id, vote_number):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = %(vote_number)s
                    WHERE id = %(question_id)s;
                    """,
                    {'question_id': question_id,
                    'vote_number': vote_number})

@connection.connection_handler
def route_edit_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})

    question_to_edit = cursor.fetchall()
    return question_to_edit[0]

@connection.connection_handler
def edit_question(cursor, question_id, edited_title, edited_message):
    cursor.execute("""
                    UPDATE question
                    SET title = %(edited_title)s, message = %(edited_message)s
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id,
                    'edited_title': edited_title,
                    'edited_message': edited_message})


@connection.connection_handler
def add_new_user(cursor: RealDictCursor, email, password):
    date = datetime.now().strftime("%b %d %Y %H:%M:%S")
    query = """
        INSERT INTO users (email, password, registration_time, reputation)
        VALUES (%(email)s, %(password)s, %(date)s, 0)
    """
    data = {
        'email': email,
        'password': password,
        'date': date
    }
    cursor.execute(query, data)

@connection.connection_handler
def list_users(cursor: RealDictCursor, userid=None):
    where = f'WHERE userid = {userid}' if userid else ''
    query = f"""
    SELECT
    users.userid AS userid,
    users.email AS email,
    users.registration_time AS regtime,
    users.reputation AS reputation,
    COUNT(DISTINCT question.id) AS question_count,
    COUNT(DISTINCT answer.id) AS answer_count,
    COUNT(DISTINCT comment.id) AS comment_count
    FROM users
    LEFT JOIN question
    ON users.userid = question.user_id
    LEFT JOIN answer
    ON users.userid = answer.user_id
    LEFT JOIN comment
    ON users.userid = comment.user_id
    {where}
    GROUP BY userid
    ORDER BY reputation DESC
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_record_by_email(cursor: RealDictCursor, email):
    query = """
        SELECT * FROM users
        WHERE email = %(email)s
    """
    data = {
        'email': email
    }
    cursor.execute(query, data)
    return cursor.fetchone()