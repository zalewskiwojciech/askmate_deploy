from flask import Flask, render_template, request, redirect, url_for

import data_manager, connection, util

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def show_list():

    return render_template('list.html',
                           question_list = data_manager.get_question_list(),
                           QUESTION_HEADERS = connection.QUESTION_HEADERS)



@app.route('/search_result', methods=['POST'])
def show_search_result():
    if request.method=='POST':
        search_phrase = f'%{request.form["search"]}%'
        # search_result_questions = data_manager.search_question_id_from_questions(search_phrase)
        # search_result_answers = data_manager.search_question_id_from_answers(search_phrase)
        # search_result = (search_result_questions) + (search_result_answers)
        complete_questions_search_list = data_manager.search_question_list(search_phrase)
        len_list = len(complete_questions_search_list)
        return render_template('search_result.html', len_list=len_list, complete_questions_search_list=complete_questions_search_list,  QUESTION_HEADERS = connection.QUESTION_HEADERS)

@app.route('/question/<question_id>')
def show_question_and_answers(question_id: int):
    single_question=data_manager.get_single_question(question_id)
    answers_list_for_single_question = data_manager.get_all_answers_for_single_question(question_id)
    comments_for_single_question = data_manager.get_all_comments_for_single_question(question_id)
    comment_for_single_answer = data_manager.get_all_comments_for_single_answer()
    return render_template('question.html',
                           question_id=question_id,
                           single_question=single_question,
                           QUESTION_HEADERS=connection.QUESTION_HEADERS,
                           all_answers=answers_list_for_single_question,
                           ANSWER_HEADERS=connection.ANSWER_HEADERS,
                           comments_for_single_question=comments_for_single_question
                           )


@app.route('/question/vote_up/<question_id>')
def question_vote_up(question_id: int):
    # connection.modify_data(connection.QUESTION_PATH, question_id, +1, 'vote_number', connection.QUESTION_HEADERS)
    data_manager.update_question_vote_up(question_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/vote_down/<question_id>')
def question_vote_down(question_id: int):
    # connection.modify_data(connection.QUESTION_PATH, question_id, -1, 'vote_number', connection.QUESTION_HEADERS)
    data_manager.update_question_vote_down(question_id)
    return redirect(f'/question/{question_id}')

@app.route('/answer/vote_up/<answer_id>')
def answer_vote_up(answer_id: int):
    #connection.modify_data(connection.ANSWER_PATH, answer_id, +1, 'vote_number', connection.ANSWER_HEADERS)
    question_id = ((data_manager.get_question_id_from_answer_id(answer_id))[0])['question_id']
    data_manager.update_answer_vote_up(answer_id)

    return redirect(f'/question/{question_id}')


@app.route('/answer/vote_down/<answer_id>')
def answer_vote_down(answer_id: int):
    #connection.modify_data(connection.ANSWER_PATH, answer_id, -1, 'vote_number', connection.ANSWER_HEADERS)
    question_id = ((data_manager.get_question_id_from_answer_id(answer_id))[0])['question_id']
    data_manager.update_answer_vote_down(answer_id)

    return redirect(f'/question/{question_id}')

@app.route('/add-question', methods=['GET', 'POST'])
def new_question():
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        image = request.form['image']
        new_row = data_manager.transform_question_into_dictionary(title, message, image)
        data_manager.add_new_row_to_question_list(new_row)
        # data_list = data_manager.add_new_row_to_question_list(new_row)
        # connection.export_all_data(connection.QUESTION_PATH, data_list, connection.QUESTION_HEADERS)
        return redirect('/')

    return render_template('add-question.html')

@app.route('/question/<question_id>/add_comment_to_question', methods=['GET', 'POST'])
def question_add_comment(question_id: int):
    if request.method == 'POST':
        message = request.form['message']
        new_row = data_manager.transform_comment_into_dictionary(question_id, message )
        data_manager.add_comment_to_database(new_row)
        return redirect(f'/question/{question_id}')
    return render_template('new_comment_to_question.html', question_id=question_id)

@app.route('/question/<question_id>/new_answer', methods=['GET', 'POST'])
def new_answer(question_id):
    if request.method == 'POST':
        message = request.form['message']
        image = request.form['image']
        new_row = data_manager.transform_answer_into_dictionary(question_id, message, image)
        data_manager.add_new_row_to_answer_list(new_row)
        return redirect(f'/question/{question_id}')
    return render_template('new_answer.html', question_id = question_id)

@app.route('/question/view_up/<question_id>')
def question_view_up(question_id: int):
    data_manager.update_view_number_up(question_id)
    return redirect(f'/question/{question_id}')


@app.route('/answer/add_comment/<answer_id>', methods=['GET', 'POST'])
def comment_for_answer(answer_id):
    if request.method == 'POST':
        message = request.form['comment']
        data_manager.add_comment_to_database(data_manager.transform_answer_comment_into_dictionary(answer_id,message))
        return redirect('/')
    return render_template('comment_for_answer.html', answer_id = answer_id)




if __name__ == '__main__':
    app.run(
        debug = True,
        port = 5000
    )