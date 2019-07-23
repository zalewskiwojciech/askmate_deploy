import csv
import os

QUESTION_PATH = os.getenv('QUESTION_PATH') if 'QUESTION_PATH' in os.environ else 'sample_data/question.csv'
ANSWER_PATH = os.getenv('ANSWER_PATH') if 'ANSWER_PATH' in os.environ else 'answer.csv'
QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']

#ENRTEERRRRY !!!!!!!!!!!!!!!!!!!!!!!!!!!!

def get_all_data(my_path):
    with open(my_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter = ',')
        data_list = []
        for row in reader:
            data_list.insert(0, dict(row))
    return data_list


def add_user_story(story):
    with open(DATA_FILE_PATH, 'a') as file:
        file.write('\n')
        for item in story:
            file.write(item)
            file.write(';')