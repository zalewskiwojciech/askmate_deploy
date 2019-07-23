from flask import Flask, render_template, request, redirect, url_for

import data_manager, connection

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def show_list():
    return render_template('list.html',
                           question_list = data_manager.question_list,
                           QUESTION_HEADERS = connection.QUESTION_HEADERS)



if __name__ == '__main__':
    app.run(
        debug = True,
        port = 5000
    )