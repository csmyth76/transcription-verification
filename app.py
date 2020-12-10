#from flask_ngrok import run_with_ngrok

from shutil import copy
from flask import Flask, render_template, session, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
import os
import sys
import json

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav','json'}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#run_with_ngrok(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
'''
@app.route('/', methods=['GET', 'POST'])
def index():

        if request.method == 'GET':
          session["internal_path"] = "/data"
          return render_template('index.html')
'''
@app.route('/', methods=['GET', 'POST'])
def upload(): 
    # sets session list of wav and json files
    print ("UPLOAD")
    path_text = "/data"
    path_files = []
    wj_path_names = []
    
    # get all files in directory
    for fl in os.listdir(path_text):
        path_files.append(fl)
    
    # identify and collect wav/json pairs
    for fl in path_files:
      name, extension = os.path.splitext(fl)
      if extension == ".wav":
        json_file_name = name + ".json"
        if json_file_name in path_files:
          path_name = os.path.join(path_text,name)
          wj_path_names.append(path_name)
        else:
          print (f"{fl} has no matching JSON; ignoring")
    
    # create transcription file
    out_path = os.path.join(path_text,"transcriptions_vryfd.txt")
    with open(out_path, "w") as f:
      pass
    session["out_file"] = out_path

    # prep for next run
    session["wj_path_names"] = wj_path_names
    next_page = upload_to_static(wj_path_names)

    return render_template( 'play_file.html', wav=next_page['wav'], transcript=next_page['transcript'])


def upload_to_static(wj_path_names):
    next_page={}

    # setup static path
    base = os.path.basename(wj_path_names[0])
    static_path = os.path.join(os.getcwd(), 'static')

    #copy over json
    dst_path_json = os.path.join (static_path, base + ".json")
    copy(wj_path_names[0] + ".json", dst_path_json)
    
    # get transcription
    with open(dst_path_json) as f:
      data = json.load(f)
    next_page['transcript'] = data["text"]

    # copy over wav file and set up to play
    dst_path_wav = os.path.join (static_path, base + ".wav")
    copy(wj_path_names[0] + ".wav", dst_path_wav)

    # store wav destination to play for next page
    next_page['wav'] = os.path.join('static', base + ".wav") 
    
    return next_page

@app.route("/next_file", methods=["POST"])
def next_file():
    print ("NEXT FILE")
    wj_path_names = session["wj_path_names"]
    
    # store transcirption
    with open(session["out_file"], "a") as f:
      filename = os.path.basename(session["wj_path_names"][0]) + ".wav"
      transx_line = filename + " " + request.form['transcription'] + "\n"
      f.write(transx_line)

    # collect file name here and remove file from static dir
    del_file = wj_path_names.pop(0)
    for ext in [".wav", ".json"]:
        del_file_ext = os.path.join(del_file, ext)
        if os.path.exists(del_file_ext):
            os.remove(del_file_ext)
        else:
            print ("File does not exist: :" + str(del_file_ext))

    if len(wj_path_names) >= 1:
      # prep for next run
      session["wj_path_names"] = wj_path_names
      next_page = upload_to_static(session["wj_path_names"] )
    else:
      # create an end page
      return ""

    return render_template( 'play_file.html', wav=next_page['wav'], transcript=next_page['transcript'])


if __name__ == '__main__':
    #app.debug = True
    app.run(host ='0.0.0.0', port = 5001, debug = True) 
    #app.run()  # If address is in use, may need to terminate other sessions:
               # Runtime > Manage Sessions > Terminate Other Sessions
    
# /content/en-us_kaldi-zamia/test/perfect
