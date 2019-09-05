from flask import Flask, render_template, request, redirect

import data_manager, connection, util

app = Flask(__name__)

app.secret_key = b'\x1bb\x10\xac\x01\x850\xc3[\xa7\n\x8f'

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
    return render_template('question.html',
                           question_id=question_id,
                           single_question=single_question,
                           QUESTION_HEADERS=connection.QUESTION_HEADERS,
                           all_answers=answers_list_for_single_question,
                           ANSWER_HEADERS=connection.ANSWER_HEADERS
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



@app.route('/question/<question_id>/new_answer', methods=['GET', 'POST'])
def new_answer(question_id):

    if request.method == 'POST':
        message = request.form['message']
        image = request.form['image']
        # answer_in_dictionary_format = data_manager.transform_answer_into_dictionary(question_id, message, image)
        # data_to_export = data_manager.add_new_row_to_answer_list(answer_in_dictionary_format)
        # connection.export_all_data(connection.ANSWER_PATH, data_to_export, connection.ANSWER_HEADERS)
        new_row = data_manager.transform_answer_into_dictionary(question_id, message, image)
        data_manager.add_new_row_to_answer_list(new_row)
        return redirect(f'/question/{question_id}')
    return render_template('new_answer.html', question_id = question_id)


@app.route('/question/view_up/<question_id>')
def question_view_up(question_id: int):

    data_manager.update_view_number_up(question_id)
    return redirect(f'/question/{question_id}')


@app.route('/registration', methods=['GET', 'POST'])
def registration():

    if request.method == 'POST':
        username = request.form['username']
        password = util.hash_password(request.form['password'])
        registration_time = util.calculate_timestamp()
        duplication = data_manager.check_username(username)
        if len(duplication) != 0:
            message = 'username alredy exists '
            return render_template('registration.html', message=message )
        elif len(username) < 5:
            message = 'usernames must have at least 5 characters'
            return render_template('registration.html', message = message)
        elif len(request.form['password']) < 5:
            message = 'password must have at least 5 characters'
            return render_template('registration.html', message = message)
        else:
            message = 'you are succesfully registred'
            data_manager.update_users_registration(username, password, registration_time)
            return render_template('registration.html', message = message)
    return render_template('registration.html')


if __name__ == '__main__':
    app.run(
        debug = True,
        port = 5000
    )