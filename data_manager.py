import connection
import util
from operator import itemgetter
import connection_with_database


@connection_with_database.connection_handler
def get_question_id_from_answer_id(cursor, answer_id):
    cursor.execute("""
                        SELECT question_id FROM answer
                        WHERE id = %(answer_id)s;
                        """,
                       {'answer_id': answer_id})


    question_id_from_answer_id = cursor.fetchall()

    # data_list = connection.get_all_data(connection.QUESTION_PATH)
    # data_list = sorted(data_list, key=lambda x: int(itemgetter('id')(x)), reverse=True)

    return question_id_from_answer_id

    # data_list = connection.get_all_data(connection.QUESTION_PATH)
    # data_list = sorted(data_list, key=lambda x: int(itemgetter('id')(x)), reverse=True)


@connection_with_database.connection_handler
def update_question_vote_up(cursor, question_id):


    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number + 1
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})



@connection_with_database.connection_handler
def update_question_vote_down(cursor, question_id):


    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number - 1
                    WHERE id = %(question_id)s AND vote_number > 0
                    """,
                   {'question_id': question_id})



@connection_with_database.connection_handler
def update_answer_vote_up(cursor, answer_id):


    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number + 1
                    WHERE id = %(answer_id)s;
                    """,
                    {'answer_id': answer_id})




@connection_with_database.connection_handler
def update_answer_vote_down(cursor, answer_id):

    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number - 1
                    WHERE id = %(answer_id)s AND vote_number > 0;
                    """,
                    {'answer_id': answer_id})

# @connection_with_database.connection_handler
# def search_question_id_from_answers(cursor, search_phrase):
#
#     cursor.execute("""
#                         SELECT question_id FROM answer
#                         WHERE message LIKE %(search_phrase)s
#                         ;
#        """, {'search_phrase': search_phrase})
#
#     complete_questions_search_id_from_answers=cursor.fetchall()
#     return complete_questions_search_id_from_answers
#
# @connection_with_database.connection_handler
# def search_question_id_from_questions(cursor, search_phrase):
#
#
#     cursor.execute("""
#                         SELECT id FROM question
#                         WHERE message LIKE %(search_phrase)s OR title LIKE %(search_phrase)s
#                         ;
#     """, {'search_phrase' : search_phrase})
#
#     complete_questions_search_id_from_questions = cursor.fetchall()
#     return complete_questions_search_id_from_questions
#

@connection_with_database.connection_handler
def search_question_list(cursor, search_phrase):
    cursor.execute("""
                        SELECT * FROM question WHERE id IN 
                                                            (SELECT question_id FROM answer
                                                            WHERE message LIKE %(search_phrase)s) OR 
                                                            message LIKE %(search_phrase)s OR
                                                            title LIKE %(search_phrase)s
                        ORDER BY question.id DESC;
                                                            

    """, {'search_phrase' : search_phrase})

    complete_questions_search_list = cursor.fetchall()
    return complete_questions_search_list



    # cursor.execute("""
    #                     SELECT * FROM question
    #                     WHERE id IN (%(question_id))
    #                     ;
    # """, {'question_id' : question_id})
    #
    # complete_questions_search_list = cursor.fetchall()
    # return complete_questions_search_list
    #

@connection_with_database.connection_handler
def get_question_list(cursor):

    cursor.execute("""
                        SELECT * FROM question
                        ORDER BY question.id DESC; 
    """)

    data_list = cursor.fetchall()

    #data_list = connection.get_all_data(connection.QUESTION_PATH)
    #data_list = sorted(data_list, key=lambda x: int(itemgetter('id')(x)), reverse=True)

    return data_list

@connection_with_database.connection_handler
def get_answer_list(cursor):

    cursor.execute("""
                        SELECT * FROM answer
                        ORDER BY answer.id;
    """)
    # data_list = connection.get_all_data(connection.ANSWER_PATH)
    # data_list = sorted(data_list, key=lambda x: int(itemgetter('id')(x)), reverse=True)
    data_list = cursor.fetchall()

    return data_list

@connection_with_database.connection_handler
def get_single_question(cursor, question_id):

    cursor.execute("""
                        SELECT * FROM question    
                        WHERE  id = %(question_id)s;
    """, {'question_id': question_id})

    single_question = cursor.fetchall()

    # for question in question_list:
        # if question['id'] == question_id:
    return single_question


@connection_with_database.connection_handler
def get_all_answers_for_single_question (cursor, question_id):

    cursor.execute("""
                        SELECT * FROM answer
                        WHERE question_id = %(question_id)s
                        ORDER BY answer.id;
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


@connection_with_database.connection_handler
def get_all_comments_for_single_question (cursor, question_id):

    cursor.execute("""
                        SELECT * FROM comment
                        WHERE question_id = %(question_id)s
                        ORDER BY id;
    """, {'question_id': question_id})

    all_comments_for_single_question = cursor.fetchall()
    if len(all_comments_for_single_question) == 0:
        return False
    return all_comments_for_single_question



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
    question['username'] = None
    question['submission_time'] = util.calculate_timestamp()
    question['view_number'] = 0
    question['vote_number'] = 0
    question['title'] = title
    question['message'] = message
    question['image'] = image
    return question


def transform_answer_comment_into_dictionary(answer_id,message):
    comment = {}
    comment['question_id'] = None
    comment['answer_id'] = answer_id
    comment['message'] = message
    comment['submission_time'] = util.calculate_timestamp()
    return comment

# komentarz

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



def transform_comment_into_dictionary(question_id, message ):
    comment = {}
    #question = [util.calculate_timestamp(), 0,0, title, message, image]
    comment['submission_time'] = util.calculate_timestamp()
    comment['question_id'] = question_id
    comment['answer_id'] = None
    comment['message'] = message
    return comment



@connection_with_database.connection_handler
def add_new_row_to_question_list(cursor, new_row):
    #print(new_row)
    cursor.execute("""
                        INSERT INTO question ( 
                        username,
                        submission_time,
                        view_number, 
                        vote_number, 
                        title, 
                        message, 
                        image)
                        VALUES (
                        %(username)s
                        %(submission_time)s,
                        %(view_number)s,
                        %(vote_number)s,
                        %(title)s,
                        %(message)s,
                        %(image)s);
    """, {'username': new_row['username'],
          'submission_time': new_row['submission_time'],
          'view_number': new_row['view_number'],
          'vote_number': new_row['vote_number'],
          'title': new_row['title'],
          'message': new_row['message'],
          'image': new_row['image']})


@connection_with_database.connection_handler
def update_view_number_up(cursor, question_id):

    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE %(question_id)s = question.id;
    
    
                    """,
                   {'question_id': question_id})



@connection_with_database.connection_handler
def add_comment_to_database(cursor, new_row):

    cursor.execute("""
                    INSERT INTO dekghdttahrq2c."public".comment(
                    question_id,
                    answer_id, 
                    message, 
                    submission_time)
                    VALUES( 
                        %(question_id)s,
                        %(answer_id)s,
                        %(message)s,
                        %(submission_time)s);
                    """,
                    {'question_id': new_row['question_id'],
                    'answer_id': new_row['answer_id'],
                    'message': new_row['message'],
                    'submission_time': new_row['submission_time']}
                    )

@connection_with_database.connection_handler
def get_all_comments(cursor):

    cursor.execute("""
                        SELECT * FROM comment
                        ORDER BY id;
    """)

    all_comments = cursor.fetchall()
    if len(all_comments) == 0:
        return False
    return all_comments





@connection_with_database.connection_handler
def check_username(cursor, username):

    cursor.execute("""
                    SELECT username 
                    FROM users
                    WHERE %(username)s = username;     
                    """,
                   {'username': username})
    duplication = cursor.fetchall()
    return duplication

@connection_with_database.connection_handler
def update_users_registration(cursor, username, password, registration_time):

    cursor.execute("""
                    INSERT INTO users (username, registration_time, password)
                    VALUES (%(username)s, %(registration_time)s, %(password)s)
                    """,
                   {'username': username,
                    'password': password,
                    'registration_time': registration_time
                    })


@connection_with_database.connection_handler
def get_session_user_id(cursor, username):

    cursor.execute("""
                    SELECT id 
                    FROM users
                    WHERE %(username)s = username;     
                    """,
                   {'username': username})
    session_user_id = cursor.fetchall()
    return session_user_id

@connection_with_database.connection_handler
def is_user_valid(cursor, username, password):


    cursor.execute("""
                        SELECT  password 
                        FROM users
                        WHERE 
                        %(username)s = username;     
                        """,
                   {'username': username,
                    })
    user_pw_select = cursor.fetchall()


    is_password_valid = util.verify_password(password, user_pw_select[0].get('password', ' '))
    if is_password_valid:

        return True
    else:
        return False
