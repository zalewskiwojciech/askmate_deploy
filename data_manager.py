import connection

question_list = connection.get_all_data(connection.QUESTION_PATH)

def get_single_question(question_id, question_list):

    for question in question_list:
        if question['id'] == question_id:
            return question
