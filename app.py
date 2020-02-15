#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
import json
from logging import Formatter, FileHandler
# from forms import *
import os
# import speech_recognition as
import azure_services as azs

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if(not os.path.exists(UPLOAD_FOLDER)):
    os.mkdir(UPLOAD_FOLDER)
# db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/index')
def index():
    return render_template('pages/placeholder.home.html')


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/hindi')
def hindi():
    return render_template('pages/placeholder.hindi.html')


@app.route('/marathi')
def marathi():
    return render_template('pages/placeholder.marathi.html')


# def transcribe(audio, r):
#     try:
#         # for testing purposes, we're just using the default API key
#         # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
#         # instead of `r.recognize_google(audio)`
#         res = r.recognize_google(audio)
#     except sr.UnknownValueError:
#         res = "Google Speech Recognition could not understand audio"
#     except sr.RequestError as e:
#         res = "Could not request results from Google Speech Recognition service; {}".format(
#             e)
#     return res


# @app.route('/listen')
# def listen():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source)
#         print("Listening..")
#         audio = r.listen(source)
#         print("Listening Finished..")
#         res = transcribe(audio, r)
#         print(res)
#     return res, '200'

@app.route('/listen')
def listen():
    lang = request.args.get('lang')
    res = azs.listen(lang)
    return res, '200'


ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'raw', 'jpeg', 'gif'}


def allowed_file(filename):
    # return '.' in filename and \
    #        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return True


# @app.route('/transcribe', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
#             r = sr.Recognizer()
#             with sr.AudioFile(filepath) as source:
#                 audio = r.record(source)
#                 res = transcribe(audio, r)
#                 return render_template('pages/placeholder.home.html', value=res)
#     return 'NOT OK', 200

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'testing.wav'))
            return './static/uploads/'+filename, 200


@app.route('/transcribe', methods=['GET'])
def transcribe():
    filepath = './static/uploads/testing.wav'
    lang = request.args.get('lang')
    res = azs.transcribe(filepath, lang)
    print(res)
    return res


@app.route('/sentiment', methods=['POST'])
def sentiment():
    data = request.form
    input_text = data.get('inputText')
    input_lang = data.get('inputLanguage')
    print("@app.route('/sentiment',", input_text)
    res = azs.get_sentiment(input_text, input_lang)
    return res, '200'
# @app.route('/about')
# def about():
#     return render_template('pages/placeholder.about.html')


# @app.route('/login')
# def login():
#     form = LoginForm(request.form)
#     return render_template('forms/login.html', form=form)


# @app.route('/register')
# def register():
#     form = RegisterForm(request.form)
#     return render_template('forms/register.html', form=form)


# @app.route('/forgot')
# def forgot():
#     form = ForgotForm(request.form)
#     return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
'''
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=5000)
