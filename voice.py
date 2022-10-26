import speech_recognition as sr
import openai
import subprocess
import pyautogui
import streamlit as st

def voice_to_instructions():
    """Convert voice to instructions"""
    r = sr.Recognizer()
    instructions = []
    receive_command = False
    recording = True

    while recording == True:
        try:
            with sr.Microphone() as mic:
                r.adjust_for_ambient_noise(mic, duration=.2)
                audio = r.listen(mic)

                text = r.recognize_google(audio)
                text = text.lower()

                print(f"Recognized {text}")

                if "yo jake" in text and receive_command == False:
                    instructions.append(text.replace("yo jake", ''))      
                    receive_command = True
                    print(instructions)
                    st.write(instructions)
                elif "do it jake" in text and receive_command == True:
                    instructions.append(text.replace("do it jake", ''))
                    print(instructions)
                    st.write(instructions)
                    recording = False
                elif receive_command == True:
                    instructions.append(text)
                    print(instructions)
                    st.write(instructions)

        except:
            r = sr.Recognizer()
            continue


    instructions = list(filter(None, instructions))
    print(f"You said: {instructions}")
    st.write(f"You said: {instructions}")
    instructions = instructions + ["stop"]
    return instructions
    



#####################################################################################################################
# Main Code

def main():
    r = sr.Recognizer()
    steps = []
    receive_command = False
    recording = True

    while recording == True:
        try:
            with sr.Microphone() as mic:
                r.adjust_for_ambient_noise(mic, duration=.2)
                audio = r.listen(mic)

                text = r.recognize_google(audio)
                text = text.lower()

                print(f"Recognized {text}")

                if "yo jake" in text and receive_command == False:
                    steps.append(text.replace("yo jake", ''))      
                    receive_command = True
                    print(steps)
                elif "do it jake" in text and receive_command == True:
                    steps.append(text.replace("do it jake", ''))
                    print(steps)
                    recording = False
                elif receive_command == True:
                    steps.append(text)
                    print(steps)

        except:
            r = sr.Recognizer()
            continue


    steps = list(filter(None, steps))
    print(f"You said: {steps}")
    steps = steps + ["stop"]


    openai.api_key = st.secrets["OPENAI_API_KEY"]

    robotc_path = r'C:\Program Files (x86)\Robomatter Inc\ROBOTC Development Environment 4.X\ROBOTC.exe' 
    script_path = r'C:\Users\stemg\Documents\GitHub\Robo-autoscript\script.c'

    content = "#pragma config(Motor,  port2,           rightMotor,    tmotorNormal, openLoop, reversed)\n#pragma config(Motor,  port3,           leftMotor,     tmotorNormal, openLoop)\n\n/*\nProgram Description: This program is a RobotC program\n\nRobot Description: The robot has 2 motors with 4 wheels.\n*/\n\ntask main()\n{\n"

    instructions_incode = ""
    instructions_prompt = "Edit and complete the code below to execute the instructions:\n"
    for index, instruction in enumerate(steps):
        instructions_prompt += f"    {index + 1}. {instruction}\n"
        instructions_incode += f"   // {index + 1}. {instruction}\n\n\n"


    # Generate code
    response = openai.Edit.create(
        model="code-davinci-edit-001",
        input = f"{content}{instructions_incode}\n",
        instruction=instructions_prompt,
        temperature=0,
        top_p=1
    )

    if 'choices' in response:
        response_choices = response['choices']
        if len(response_choices) > 0:

            # save the script to a file
            with open('script.c', 'w') as f:
                f.write(response_choices[0]['text'])

            # Open RoboC and Compile the script
            subprocess.Popen(robotc_path)
            pyautogui.sleep(4)
            pyautogui.hotkey('ctrl', 'o') # Open file
            pyautogui.sleep(1)
            pyautogui.typewrite(script_path) # Type the path to the script
            pyautogui.sleep(2)
            pyautogui.press('enter') # Press enter
            pyautogui.sleep(3)
            pyautogui.press('f5') # Compile
            pyautogui.sleep(3)
            pyautogui.moveTo(400, 75)
            pyautogui.sleep(8)
            pyautogui.click()
            pyautogui.sleep(2)
            pyautogui.hotkey('alt', 'f4') # Close RobotC

        else:
            print('No choices')

if __name__ == "__main__":
    main()