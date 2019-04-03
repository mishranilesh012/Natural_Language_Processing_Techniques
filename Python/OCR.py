import cv2
import pytesseract
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import base64
import json
app = Flask(__name__)
api = Api(app)

def convertBaseToImage(imgstring):
    imgdata = base64.b64decode(imgstring)
    filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)

class CheckOCR():
    def post(self):
        req_data = json.get_json()
        image = req_data['imageData']
        convertBaseToImage(image)

        imPath = 'some_image.JPG'
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        config = ('-l eng --oem 1 --psm 3')
        # Read image from disk
        im = cv2.imread(imPath, cv2.IMREAD_COLOR)

        # Run tesseract OCR on image
        text = pytesseract.image_to_string(im, config=config)

        # Print recognized text
        return jsonify(
            Text = text
        )

# if __name__ == '__main__':
#
api.add_resource(CheckOCR,"/checkOcr")
app.run(port = 5000, debug = True)