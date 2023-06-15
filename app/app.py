from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import time 
import label
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        file = request.files["camera"]
        if file.filename is not None:
            filename = secure_filename(str(time.time()) + file.filename)
            file.save(os.path.join("static/img/output/", filename))
            label.label("static/img/output/" + filename, filename)
            return render_template("res.html", img=os.path.join("img/output/", filename))
        else:
            return "", 400
    else:
        return "", 405
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)