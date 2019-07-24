import time


def find_biggest_answer_id_for_this_question(question_id):

    biggest_id = -1
    for single_answer in answer_list:
        if single_answer['question_id'] == question_id and single_answer['id'] > biggest_id:
            biggest_id = single_answer['id']
    return biggest_id


def calculate_timestamp():

    dt_object = int(time.time())
    return dt_object
