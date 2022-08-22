import data_manager


def vote_up_or_down(vote_number, vote_type):
    if vote_type == 'up':
        vote_number['vote_number'] += 1
    else:
        vote_number['vote_number'] -= 1
    return vote_number['vote_number']


def deciding_where_to_redirect(comments, comment_id, answer_id, question_id):
    for comment in comments:
        if comment["question_id"] == int(question_id) and comment["id"] == comment_id:
            return "question"

        elif comment["answer_id"] == int(answer_id) and comment["id"] == comment_id:
            return "answer"


def order_questions(order_by, order):
    if order is not None:
        questions = data_manager.list_questions(order_by, order)
    else:
        order_by = 'submission_time'
        order = 'DESC'
        questions = data_manager.list_questions(order_by, order)
    return questions