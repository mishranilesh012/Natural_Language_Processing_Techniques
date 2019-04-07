from PIL import Image
import pyocr.builders
from flask import Flask, request
from flask_restful import Resource, Api
import base64
import cv2
# with open("testImg/test_1.jpg", "rb") as image_file:
#     img_data = base64.b64encode(image_file.read())
# print(img_data)

app = Flask(__name__)
api = Api(app)

tools = pyocr.get_available_tools()
print(tools)
tool = tools[0]
langs = tool.get_available_languages()
lang = langs[0]


class ExtractImg(Resource):

    def post(self):
        req_data = request.get_json()

        img_data = req_data["img"]
        inputText = req_data["inputText"]
        inputText = inputText.lower()
        # print(img_data)
        # print(req_data)
        # print(inputText)

        img_data = (str.encode(img_data))

        with open("testImg/imageToSave.jpg", "wb") as fh:
            fh.write(base64.decodebytes(img_data))

        image = cv2.imread("testImg/imageToSave.jpg")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        methods = [["m"],["g"]]
        listInput = []
        listTxt = []

        for method in methods:

            blur = ''
            if(method[0] == 'g'):
                blur = cv2.GaussianBlur(gray,(15,15),0)
            else:
                blur = cv2.medianBlur(gray, 3)


            cv2.imwrite("testImg/imageToSave.jpg",blur)

            txt = tool.image_to_string(
                    Image.open("testImg/imageToSave.jpg"),
                    lang=lang,
                builder=pyocr.builders.TextBuilder()
            )
            print("----")
            print(txt)
            txt = txt.lower()

            method.append(txt)

            listInput = list(inputText)
            listTxt = list(txt)

            matchCount = 0
            listTemp1 = []
            listTemp2 = []
            if(len(listInput) >= len(listTxt)):
                totalCount = len(listInput)
                listTemp1 = listInput
                listTemp2 = listTxt
            else:
                totalCount = len(listTxt)
                listTemp1 = listTxt
                listTemp2 = listInput


            for i in range(len(listTemp1)):

                if( i < len(listTemp2)   and listTemp1[i] == listTemp2[i]):
                    matchCount+=1


            accuracy = (matchCount/totalCount)*100
            method.append(accuracy)

            print(matchCount)
            print(totalCount)

        accuracy = 0
        status = ""
        currentTxt = ""
        if(methods[0][2] > methods[1][2] ):
            accuracy = methods[0][2]
            currentTxt = methods[0][1]
        else:
            accuracy = methods[1][2]
            currentTxt = methods[1][1]

        if(int(accuracy) == 100):
            status = "matched !!"
        else:
            status = "not matched"


        outJson = {

            "currentTxt" : currentTxt,
            "orignalTxt" : inputText,
            "status" : status,
            "accuracy" : accuracy

        }

        return (outJson)


api.add_resource(ExtractImg,"/getText")

app.run(host='127.0.0.1', port = '2935', debug = True)


