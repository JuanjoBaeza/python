from googletrans import Translator, constants
from pprint import pprint
from playsound import playsound
from gtts import gTTS

# googletrans=4.0.0rc1, playsound1.2.2, print
# https://stackoverflow.com/questions/52455774/googletrans-stopped-working-with-error-nonetype-object-has-no-attribute-group

def trnslate():

    tr = Translator()
    
    pprint(f'The available languages and their codes are: {constants.LANGUAGES}')

    lan = input('Please enter your desired language:\n')
    phrase = input('Say something nice:\n')

    #Traduccion texto
    translated = tr.translate(phrase, dest = lan)
    print(translated.text)
    
    #Volcado en mp3
    aud = gTTS(translated.text, lang = lan)
    aud.save('trantest.mp3')
    
    #Ejecucion del mp3
    playsound('trantest.mp3')
#   os.remove('trantest.mp3')
    
trnslate()