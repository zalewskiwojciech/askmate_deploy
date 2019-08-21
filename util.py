
from datetime import datetime
import data_manager

def find_biggest_answer_id(answer_list):

    biggest_id = -1
    for single_answer in answer_list:
        single_aswer_id = int(single_answer['id'])
        if  single_aswer_id > biggest_id:
            biggest_id = single_aswer_id
    return biggest_id


def calculate_timestamp():

    dt_object = datetime.now()
    return dt_object


def find_question_id_from_answer_id(answer_id):
    answer_list = data_manager.get_answer_list()
    question_id = None
    for answer in answer_list:
        if answer['id'] == answer_id:
            question_id = answer['question_id']
            break
    return question_id

