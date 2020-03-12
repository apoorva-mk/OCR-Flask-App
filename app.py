from flask import Flask
from flask import request
import ocr
import os
port = int(os.environ.get("PORT", 5000))
app = Flask(__name__)


@app.route('/', methods=["GET","POST"])
def hello_world():
    if request.method == 'POST':
        req_data = request.get_json()
        encoded_string = req_data["base64encodedimage"]
        text = ocr.obtain_text_from_image(encoded_string.encode())
        return text
    else:
        return "This is an simple OCR API, made by Alphageek"

if __name__ == '__main__':
    app.run(port=port)