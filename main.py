from flask import Flask, render_template, send_file, send_from_directory, safe_join, abort, redirect, url_for
from flask_restful import Api, Resource, request
import os, pathlib, datetime, time
from backend import process

uploads_path = "uploads"
downloads_path = "downloads\\"
images_path = "images\\"
allowed_extensions = [".pdf"]


app = Flask(__name__)
app.config["uploads_path"] = uploads_path
api = Api(app)
THIS_FOLDER = app.root_path

def correct_name(name):
    return (name[-4:] in allowed_extensions)


def temp_func():
    time.sleep(5)

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("/index.html")

@app.route("/process", methods=["GET"])
def post_upload():
    return render_template("/upload.html")

@app.route("/downloadfile/<filename>/<threshold>/<performance>", methods=["GET"])
def download_file(filename, threshold):
    if (process(filename, uploads_path+"\\", downloads_path, images_path, float(threshold)/100) == -1, performance):
        return render_template('falseoutput.html')
    return render_template('upload.html',value="fixed_"+filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = downloads_path +filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

@app.route("/api/v1.0/tasks/render/", methods=["POST"])
def upload():
    file = request.files["file"]
    threshold = request.form["threshold"]
    performance = request.form["performance"]
    if (correct_name(file.filename)):
        #file.save(os.path.join(app.config["uploads_path"], file.filename[:-4] + "-input.pdf"))
        currentDate = str(datetime.datetime.now()).replace(":","-").replace(" ", "")
        file.save(os.path.join(THIS_FOLDER, uploads_path, file.filename[:-4] + "-" + currentDate+ "-input.pdf"))
        return redirect("/downloadfile/" + file.filename[:-4] + "-" + currentDate + "-input.pdf/" + threshold + "/" + performance )
    

if __name__ == "__main__":
    app.run(debug=True)
