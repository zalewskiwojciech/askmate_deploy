from flask import Flask, render_template, request, redirect, url_for

import data_manager, connection

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def show_list():

    return render_template('list.html',
                           question_list = data_manager.get_question_list(),
                           QUESTION_HEADERS = connection.QUESTION_HEADERS)

@app.route('/question/<question_id>')
def show_question_and_answers(question_id: int):
    single_question=data_manager.get_single_question(question_id, data_manager.get_question_list())
    answers_list_for_single_question = data_manager.get_all_answers_for_single_question(question_id, data_manager.get_answer_list())

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
    return redirect(f'/question/{question_id}')


@app.route('/question/vote_down/<question_id>')
def question_vote_down(question_id: int):
    connection.modify_data(connection.QUESTION_PATH, question_id, -1, 'vote_number', connection.QUESTION_HEADERS)
    return redirect(f'/question/{question_id}')

@app.route('/answer/vote_up/<answer_id>')
def answer_vote_up(answer_id: int):
    connection.modify_data(connection.ANSWER_PATH, answer_id, +1, 'vote_number', connection.ANSWER_HEADERS)
    answer_list = data_manager.get_answer_list()
    question_id = None
    for answer in answer_list:
        if answer['id'] == answer_id:
            question_id = answer['question_id']
            break
    return redirect(f'/question/{question_id}')


@app.route('/answer/vote_down/<answer_id>')
def answer_vote_down(answer_id: int):
    connection.modify_data(connection.ANSWER_PATH, answer_id, -1, 'vote_number', connection.ANSWER_HEADERS)
    return redirect(f'/question/{question_id}')


@app.route('/add-question', methods=['GET', 'POST'])
def new_question():
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        image = request.form['image']
        new_row = data_manager.transform_question_into_dictionary(title, message, image)
        data_list = data_manager.add_new_row_to_data_list(new_row, data_manager.get_question_list())
        connection.export_all_data(connection.QUESTION_PATH, data_list, connection.QUESTION_HEADERS)
        return redirect('/')

    return render_template('add-question.html')



@app.route('/question/<question_id>/new_answer', methods=['GET', 'POST'])
def new_answer(question_id):
    if request.method == 'POST':
        message = request.form['message']
        image = request.form['image']
        answer_in_dictionary_format = data_manager.transform_answer_into_dictionary(question_id, message, image)
        data_to_export = data_manager.add_new_row_to_data_list(answer_in_dictionary_format, data_manager.answer_list)
        connection.export_all_data(connection.ANSWER_PATH, data_to_export, connection.ANSWER_HEADERS)
        return redirect(f'/question/{question_id}')
    return render_template('new_answer.html', question_id = question_id)




if __name__ == '__main__':
    app.run(
        debug = True,
        port = 5000
    )