#https://pypi.org/project/SpeechRecognition/

import speech_recognition as sr

r = sr.Recognizer()
steps = []
boolean = False
bool2 = True

while bool2 == True:
    try:
        with sr.Microphone() as mic:
            r.adjust_for_ambient_noise(mic, duration=.2)
            audio = r.listen(mic)

            text = r.recognize_google(audio)
            text = text.lower()

            print(f"Recognized {text}")

            if "hello computer" in text and boolean == False:
                steps.append(text.replace("hello computer", ''))      
                boolean = True
                print(steps)
            elif "goodbye computer" in text and boolean == True:
                steps.append(text.replace("goodbye computer", ''))
                print(steps)
                bool2 = False
            elif boolean == True:
                steps.append(text)
                print(steps)

    except:

        r = sr.Recognizer()
        continue
steps = list(filter(None, steps))
print(f"You said: {steps}")


