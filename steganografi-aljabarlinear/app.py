from flask import Flask
from flask import request
from flask import jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from steganografi import *

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/upload", methods=['POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['image']
        path = "original_image/"
        file_name = secure_filename(file.filename)
        file.save(path +file_name)

        encrypt_message = encrypt(request.form['message'])

        result = embed_message(str(request.form['id']), path, file_name, encrypt_message)
    
    return jsonify({
        'original_image' : path+file_name,
        'embedded_image' : result,
        'filename' : request.form['filename'],
        'status' : 200
    })
    
@app.route("/extract_image", methods=['POST'])
def extract():
    if request.method == 'POST':
        file = request.files['image']
        path = "temp/"
        file_name = secure_filename("temp_" + file.filename)
        file.save(path +file_name)
        
        extract_image = extract_message(path+file_name)

        result = decrypt(extract_image)
    
    return jsonify({
        "extract_result" : result,
        "status" : 200,
    })

@app.route("/embedded_image/<url>")
def open_embedded_image(url):
    return send_file("embedded_image/"+url)


@app.route("/original_image/<url>")
def open_original_image(url):
    return send_file("original_image/"+url)