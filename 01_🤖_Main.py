import streamlit as st
import openai
from streamlit_ace import st_ace
import subprocess
import pyautogui

st.set_page_config(
     page_title="Robo Auto Script",
     page_icon="🤖",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "Scripting RoboC code with OpenAi's Codex"
     }
)

openai.api_key = st.secrets["OPENAI_API_KEY"]



# Spawn a new Ace editor
content = st_ace(value="#pragma config(Motor,  port2,           rightMotor,    tmotorNormal, openLoop, reversed)\n#pragma config(Motor,  port3,           leftMotor,     tmotorNormal, openLoop)\n\n/*\nProgram Description: This program is a RobotC program\n\nRobot Description: The robot has 2 motors with 4 wheels.\n*/\n\ntask main()\n{\n", language="c")


# Instruction input
if 'instructions' not in st.session_state:
    st.session_state['instructions'] = ['Stop']

new_instruction = st.text_input("Add Instruction")
col1, col2 = st.columns(2)
if col1.button("Add instruction"):
    st.session_state['instructions'].insert(-1, new_instruction)
elif col2.button("Clear Instructions"):
    st.session_state['instructions'] = ['Stop']
    st.experimental_rerun()

instructions_incode = ""
instructions_prompt = "Edit and complete the code below to execute the instructions:\n"
for index, instruction in enumerate(st.session_state['instructions']):
    st.caption(f"{index + 1}. {instruction}")
    instructions_prompt += f"    {index + 1}. {instruction}\n"
    instructions_incode += f"   // {index + 1}. {instruction}\n\n\n"


# Generate code
if st.button("🤖 Generate Script"):
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
            # Display the first choice
            st.code(response_choices[0]['text'], language="c")

            # save the script to a file
            with open('script.c', 'w') as f:
                f.write(response_choices[0]['text'])

            # Download the first choice
            st.download_button('Download Script', response_choices[0]['text'].encode('utf-8'), file_name='script.c', mime='text/plain')
            

            # Open RoboC and Compile the script
            subprocess.Popen(r'C:\Program Files (x86)\Robomatter Inc\ROBOTC Development Environment 4.X\ROBOTC.exe')
            pyautogui.sleep(4)
            pyautogui.hotkey('ctrl', 'o') # Open file
            pyautogui.sleep(1)
            pyautogui.typewrite('C:\Coding\GitHub\Robo-autoscript\script.c') # Type the path to the script
            pyautogui.sleep(1)
            pyautogui.press('enter') # Press enter
            pyautogui.sleep(3)
            pyautogui.press('f5') # Compile
            pyautogui.sleep(10)
            pyautogui.hotkey('alt', 'f4') # Close RobotC




        else:
            st.write("No choices found")








# command = st.text_area("Enter you command here:", "Move the robot forward for 1 second then stop")


# response = openai.Completion.create(
#   model="code-davinci-002",
#   prompt= prompt,
#   temperature=0,
#   max_tokens=256,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0
# )

# st.write(response)
