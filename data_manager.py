import connection
import util
from operator import itemgetter
import connection_with_database

@connection_with_database.connection_handler
def get_question_id_from_answer_id(cursor, answer_id):

    cursor.execute("""
                            SELECT question_id FROM answer
                            WHERE question_id  BY question.id DESC 
        """)

    data_list = cursor.fetchall()

    # data_list = connection.get_all_data(connection.QUESTION_PATH)
    # data_list = sorted(data_list, key=lambda x: int(itemgetter('id')(x)), reverse=True)

    return data_list


@connection_with_database.connection_handler
def get_question_list(cursor):

    cursor.execute("""
                        SELECT * FROM question
                        ORDER BY question.id DESC 
    """)

    data_list = cursor.fetchall()

    #data_list = connection.get_all_data(connection.QUESTION_PATH)
    #data_list = sorted(data_list, key=lambda x: int(itemgetter('id')(x)), reverse=True)

    return data_list

@connection_with_database.connection_handler
def get_answer_list(cursor):

    cursor.execute("""
                        SELECT * FROM answer
                        ORDER BY answer.id
    """)
    # data_list = connection.get_all_data(connection.ANSWER_PATH)
    # data_list = sorted(data_list, key=lambda x: int(itemgetter('id')(x)), reverse=True)
    data_list = cursor.fetchall()

    return data_list

@connection_with_database.connection_handler
def get_single_question(cursor, question_id):

    cursor.execute("""
                        SELECT * FROM question    
                        WHERE %(question_id)s = id
    """, {'question_id': question_id})

    question = cursor.fetchall()

    # for question in question_list:
        # if question['id'] == question_id:
    return question


@connection_with_database.connection_handler
def get_all_answers_for_single_question (cursor, question_id):

    cursor.execute("""
                        SELECT * FROM answer
                        WHERE question_id = %(question_id)s
    """, {'question_id': question_id})

    # all_answers_for_single_question=[]

    # for answer in answer_list:
        # if answer['question_id'] == question_id:
            # all_answers_for_single_question.append(answer)
    # if len(all_answers_for_single_question) == 0:
        # return False
    all_answers_for_single_question = cursor.fetchall()
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
    #question = [util.calculate_timestamp(), 0,0, title, message, image]
    question['id'] = len(get_question_list())
    question['submission_time'] = util.calculate_timestamp()
    question['view_number'] = 0
    question['vote_number'] = 0
    question['title'] = title
    question['message'] = message
    question['image'] = image
    return question


@connection_with_database.connection_handler
def add_new_row_to_question_list(cursor, new_row):
    #print(new_row)
    cursor.execute("""
                        INSERT INTO question ( 
                        submission_time,
                        view_number, 
                        vote_number, 
                        title, 
                        message, 
                        image)
                        VALUES (
                        %(submission_time)s,
                        %(view_number)s,
                        %(vote_number)s,
                        %(title)s,
                        %(message)s,
                        %(image)s);
    """, {'submission_time' : new_row['submission_time'],
          'view_number' : new_row['view_number'],
          'vote_number' : new_row['vote_number'],
          'title' : new_row['title'],
          'message' : new_row['message'],
          'image' : new_row['image']})


@connection_with_database.connection_handler
def add_new_row_to_answer_list(cursor, new_row):
    cursor.execute("""
                        INSERT INTO answer( 
                        submission_time, 
                        vote_number, 
                        question_id, 
                        message, 
                        image)
                        VALUES (
                        %(submission_time)s,
                        %(vote_number)s,
                        %(question_id)s,
                        %(message)s,
                        %(image)s);
    """, {'submission_time': new_row['submission_time'],
          'vote_number': new_row['vote_number'],
          'question_id': new_row['question_id'],
          'message': new_row['message'],
          'image': new_row['image']})# data_list.append(new_row)


