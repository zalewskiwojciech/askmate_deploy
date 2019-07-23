from flask import Flask, render_template, request, redirect, url_for

import connection

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def show_list():
    return render_template('list.html') #>>>lista pytan



if __name__ == '__main__':
    app.run(
        debug = True,
        port = 5000
    )