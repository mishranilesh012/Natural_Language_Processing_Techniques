import cv2
import pytesseract
import audioAnalysis as adA
# adA.speakerDiarizationWrapper("dataFiles/mc1.wav",0,False)
import speech_recognition as sr
from textblob import TextBlob
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import base64
import json


r = sr.Recognizer()

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
		inputText = textarea
		convertBaseToImage(image)

		imPath = 'some_image.JPG'
		pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
		config = ('-l eng --oem 1 --psm 6')
		# Read image from disk
		gray = cv2.imread(imPath, cv2.COLOR_BGR2GRAY)

		# text = pytesseract.image_to_string(blur, config=config)
		# text = text.lower()
		# print(text)

		methods = [["m"], ["g"]]
		listInput = []
		listTxt = []

		for method in methods:

			blur = ''
			if (method[0] == 'g'):
				blur = cv2.GaussianBlur(gray, (15, 15), 0)
			else:
				blur = cv2.medianBlur(gray, 3)

			cv2.imwrite("testImg/imageToSave.jpg", blur)

			text = pytesseract.image_to_string(blur, config=config)
			text = text.lower()
			print(text)
			txt = text.lower()

			method.append(txt)

			listInput = list(inputText)
			listTxt = list(txt)

			matchCount = 0
			listTemp1 = []
			listTemp2 = []
			if (len(listInput) >= len(listTxt)):
				totalCount = len(listInput)
				listTemp1 = listInput
				listTemp2 = listTxt
			else:
				totalCount = len(listTxt)
				listTemp1 = listTxt
				listTemp2 = listInput

			for i in range(len(listTemp1)):

				if (i < len(listTemp2) and listTemp1[i] == listTemp2[i]):
					matchCount += 1

			accuracy = (matchCount / totalCount) * 100
			method.append(accuracy)

			print(matchCount)
			print(totalCount)

		accuracy = 0
		status = ""
		currentTxt = ""
		if (methods[0][2] > methods[1][2]):
			accuracy = methods[0][2]
			currentTxt = methods[0][1]
		else:
			accuracy = methods[1][2]
			currentTxt = methods[1][1]

		if (int(accuracy) == 100):
			status = "Match"
		else:
			status = "Failed"

		outJson = {

			"current": currentTxt,
			"original": inputText,
			"status": status,
			"accuracy": accuracy

		}

		return (outJson)

class Diarization(Resource):
	def post(self):
		req_data = request.get_json()
		fileStr = req_data["imageData"]
		fileStr = (str.encode(fileStr))
		print(fileStr)

		with open("output/inputAudio.wav", "wb") as fh:
			fh.write(base64.decodebytes(fileStr))

		filePath = "output/inputAudio.wav"
		adA.speakerDiarizationWrapper(filePath,0,False)

		with open("output/outImg.jpg", "rb") as image_file:
			img_data = base64.b64encode(image_file.read())

		harvard = sr.AudioFile(filePath)
		outJson = {}
		with harvard as source:
			audio = r.record(source)

			txt = r.recognize_google(audio)

			if(len(list(txt)) > 0):
				print(txt)
				sentiment = TextBlob(txt)
				img_data = img_data.decode("utf-8")
				outJson = {
					"orignalText" : txt,
					"Score": sentiment.sentiment.polarity,
					"imgData": img_data
				}

			else:
				outJson = {
					"Score: ": "Empty text"
				}


		return (outJson)

	def get(self):
		return ({"data":"information"})


api.add_resource(CheckOCR,"/checkOcr")
api.add_resource(Diarization,"/getData")

app.run(port = 5000, debug = True)