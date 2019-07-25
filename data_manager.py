import connection
import util


question_list = connection.get_all_data(connection.QUESTION_PATH)
answer_list = connection.get_all_data(connection.ANSWER_PATH)
def get_question_list():
    return connection.get_all_data(connection.QUESTION_PATH)

def get_answer_list():
    return connection.get_all_data(connection.ANSWER_PATH)


def get_single_question(question_id, question_list):

    for question in question_list:
        if question['id'] == question_id:
            return question

def get_all_answers_for_single_question (question_id, answer_list):

    all_answers_for_single_question=[]

    for answer in answer_list:
        if answer['question_id'] == question_id:
            all_answers_for_single_question.append(answer)
    if len(all_answers_for_single_question) == 0:
        return False
    return all_answers_for_single_question


def transform_answer_into_dictionary(question_id, message, image):
    answer = {}
    answer['id'] = util.find_biggest_answer_id(get_answer_list()) + 1
    answer['submission_time'] = util.calculate_timestamp()
    answer['vote_number'] = 0
    answer['question_id'] = question_id
    answer['message'] = message
    answer['image'] = image
    return answer

def transform_question_into_dictionary(title, message, image):
    question = {}
    question['id'] = len(get_question_list())
    question['submission_time'] = util.calculate_timestamp()
    question['view_number'] = 0
    question['vote_number'] = 0
    question['title'] = title
    question['message'] = message
    question['image'] = image
    return question



def add_new_row_to_data_list(new_row, data_list):

    data_list.append(new_row)
    return data_list

