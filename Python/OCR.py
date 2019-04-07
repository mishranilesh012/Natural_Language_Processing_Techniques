import cv2
import pytesseract
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import base64
import json

def convertBaseToImage(imgstring):
    imgdata = base64.b64decode(imgstring)
    filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)

app = Flask(__name__)
api = Api(app)

class CheckOCR(Resource):
    def post(self):
        req_data = request.get_json()
        image = req_data['imageData']
        textarea = req_data['text']
        textarea = textarea.lower()
        convertBaseToImage(image)

        imPath = 'some_image.JPG'
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        config = ('-l eng --oem 1 --psm 6')
        # Read image from disk
        im = cv2.imread(imPath, cv2.COLOR_BGR2GRAY)

        methods = [["m"],["g"]]
        listArea = []
        listText = []
        for method in methods:

            blur = ''
            if(method[0] == 'g'):
                blur = cv2.GaussianBlur(im,(15,15),0)
            else:
                blur = cv2.medianBlur(im, 3)

            text = pytesseract.image_to_string(blur, config=config)
            text = text.lower()
            print(text)
            
        
            method.append(text)

            listArea = list(textarea)
            listText = list(text)

            matchCount = 0
            totalCount = len(listArea)
            for i in range(len(listArea)):

                if( i < len(listText) and listArea[i] == listText[i]):
                    matchCount+=1

            accuracy = (matchCount/totalCount)*100
            method.append(accuracy)

        accuracy = 0
        status = ""
        currentText = ""
        if(methods[0][2] > methods[1][2] ):
            accuracy = methods[0][2]
            currentText = methods[0][1]
        else:
            accuracy = methods[1][2]
            currentText = methods[1][1]

        if(len(listArea)==len(listText) and int(accuracy) == 100):
            status = "matched !!"
        else:
            status = "not matched"

        return ({
            "currentText" : currentText,
            "orignalTxt" : textarea,
            "status" : status,
            "accuracy" : accuracy
        }
        )

# if __name__ == '__main__':
#
api.add_resource(CheckOCR,"/checkOcr")
app.run(port = 5000, debug = True)