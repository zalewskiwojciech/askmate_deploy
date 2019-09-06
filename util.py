
from datetime import datetime, time
import data_manager
import bcrypt

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
    answer_list = data_manager.get_question_id_from_answer_id(answer_id)
    question_id = None
    for answer in answer_list:
        if answer == answer_id:
            question_id = answer['question_id']
            break
    return question_id

def hash_password(plain_text_password):

    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_text_password.encode("utf-8"), hashed_bytes_password)