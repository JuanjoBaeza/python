from googletrans import Translator, constants
from pprint import pprint
from playsound import playsound
import pyttsx3

# googletrans=4.0.0rc1, playsound1.2.2, print
# https://stackoverflow.com/questions/52455774/googletrans-stopped-working-with-error-nonetype-object-has-no-attribute-group

engine = pyttsx3.init()

rate = engine.getProperty('rate')
print(rate)
engine.setProperty('rate', 150)

volume = engine.getProperty('volume')
print(volume)
engine.setProperty('volume', 0.8)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def trnslate():

    tr = Translator()

    for voice in voices:
        print("Voice:")
        print(" - ID: %s" % voice.id)
        print(" - Name: %s" % voice.name)
        print(" - Languages: %s" % voice.languages)
        print(" - Gender: %s" % voice.gender)
        print(" - Age: %s" % voice.age)

    pprint(f'The available languages and their codes are: {constants.LANGUAGES}')
    lan = input('Please enter your desired language:\n')
    phrase = input('Say something nice:\n')
    translated = tr.translate(phrase, dest = lan)
    print(translated.text)

    engine.say(phrase)
    engine.save_to_file(phrase, 'test.mp3')
    engine.runAndWait()
    
trnslate()