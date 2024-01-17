from gtts import gTTS

list = ["Customary", "Conceited", "Delightful", "Indispensable", "Preoccupy"]
pro = []

def text_to_speech(word):
        speech = gTTS(text = word)
        path = f".//Sound Track//{word}.mp3"
        speech.save(path)
        return path

for word in list:
    sound = text_to_speech(word)