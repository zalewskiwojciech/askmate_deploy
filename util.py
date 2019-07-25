import time


def find_biggest_answer_id(answer_list):

    biggest_id = -1
    for single_answer in answer_list:
        single_aswer_id = int(single_answer['id'])
        if  single_aswer_id > biggest_id:
            biggest_id = single_aswer_id
    return biggest_id


def calculate_timestamp():

    dt_object = int(time.time())
    return dt_object

