import speech_recognition as sr
from textblob import TextBlob

r = sr.Recognizer()

with sr.Microphone() as source:
    print('Say Something')
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print('You said: {}'.format(text))
    except:
        print('Sorry could not hear your voice')


#statement = "Today was a great day"
sentiment = TextBlob(text)
print("Sentiment Score: ", sentiment.sentiment.polarity)  # Result = 1.0

# statement2 = "Today I went to Barbeque Nation and the Food was very good"
# sentiment2 = TextBlob(statement2)
# print("Sentiment Score: ", sentiment2.sentiment.polarity)
# Result = 0.909999

#
# value = sr.AudioFile('mc1.wav')
# with value as source:
#     audio = r.record(source)
#     try:
#         text = r.recognize_google(audio)
#         print('You said: {}'.format(text))
#     except:
#         print('Sorry could not hear your voice')