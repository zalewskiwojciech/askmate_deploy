import connection

question_list = connection.get_all_data(connection.QUESTION_PATH)
answer_list = connection.get_all_data(connection.ANSWER_PATH)

def get_single_question(question_id, question_list):

    for question in question_list:
        if question['id'] == question_id:
            return question

def get_all_answers_for_single_question (question_id, answer_list):

    all_answers_for_single_question=[]

    for answer in answer_list:
        if answer['question_id'] == question_id:
            all_answers_for_single_question.append(answer)

    return all_answers_for_single_question