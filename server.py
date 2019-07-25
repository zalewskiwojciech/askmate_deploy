from flask import Flask, render_template, request, redirect, url_for

import data_manager, connection

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def show_list():

    return render_template('list.html',
                           question_list = data_manager.question_list,
                           QUESTION_HEADERS = connection.QUESTION_HEADERS)

@app.route('/question/<question_id>')
def show_question_and_answers(question_id: int):
    single_question=data_manager.get_single_question(question_id, data_manager.question_list)
    answers_list_for_single_question = data_manager.get_all_answers_for_single_question(question_id, data_manager.answer_list)

    return render_template('question.html',
                           question_id=question_id,
                           single_question=single_question,
                           QUESTION_HEADERS=connection.QUESTION_HEADERS,
                           all_answers=answers_list_for_single_question,
                           ANSWER_HEADERS=connection.ANSWER_HEADERS
                           )

@app.route('/question/vote_up/<question_id>')
def question_vote_up(question_id: int):
    connection.modify_data(connection.QUESTION_PATH, question_id, +1, 'vote_number', connection.QUESTION_HEADERS)
    return render_template('list.html',
                           question_list=data_manager.question_list,
                           QUESTION_HEADERS=connection.QUESTION_HEADERS)

@app.route('/question/vote_down/<question_id>')
def question_vote_down(question_id: int):
    connection.modify_data(connection.QUESTION_PATH, question_id, -1, 'vote_number', connection.QUESTION_HEADERS)
    return render_template('list.html',
                           question_list=data_manager.question_list,
                           QUESTION_HEADERS=connection.QUESTION_HEADERS)

@app.route('/answer/vote_up/<answer_id>')
def answer_vote_up(answer_id: int):
    connection.modify_data(connection.ANSWER_PATH, answer_id, +1, 'vote_number', connection.ANSWER_HEADERS)
    return render_template('list.html',
                           question_list=data_manager.question_list,
                           QUESTION_HEADERS=connection.QUESTION_HEADERS)
@app.route('/answer/vote_down/<answer_id>')

def answer_vote_down(answer_id: int):
    connection.modify_data(connection.ANSWER_PATH, answer_id, +-1, 'vote_number', connection.ANSWER_HEADERS)
    return render_template('list.html',
                           question_list=data_manager.question_list,
                           QUESTION_HEADERS=connection.QUESTION_HEADERS)

if __name__ == '__main__':
    app.run(
        debug = True,
        port = 5000
    )