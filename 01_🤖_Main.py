import streamlit as st
import openai
from streamlit_ace import st_ace
import subprocess
import pyautogui
import voice

def generate_script(content, instructions_incode, instructions_prompt, robotc_path, script_path):
    """Generates the script for the robot to execute by calling the OpenAI API
    It also compiles the script and runs it on the robot

    Args:
        content (string): The code that is already written with robot description and overall structure. Boilerplate code.
        instructions_incode (string): string of instructions for robot in code. This will get appended to the content.
        instructions_prompt (string): string of codex edit instructions
    """
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
            
            # Compile the script
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
            pyautogui.moveTo(650, 150)
            pyautogui.sleep(8)
            pyautogui.click()
            pyautogui.sleep(5)
            pyautogui.hotkey('alt', 'f4') # Close RobotC

        else:
            st.write("No choices found")

# Environment variables
robotc_path = r'C:\Program Files (x86)\Robomatter Inc\ROBOTC Development Environment 4.X\ROBOTC.exe' 
script_path = r'C:\Users\stemg\Documents\GitHub\Robo-autoscript\script.c'

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
# Tabs for mode selection
tab1, tab2 = st.tabs(["Type", "Voice"])

# Type mode
with tab1:
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

    # Prepare instructions for codex
    instructions_incode = ""
    instructions_prompt = "Edit and complete the code below to execute the instructions:\n"
    for index, instruction in enumerate(st.session_state['instructions']):
        st.caption(f"{index + 1}. {instruction}")
        instructions_prompt += f"    {index + 1}. {instruction}\n"
        instructions_incode += f"   // {index + 1}. {instruction}\n\n\n"

    # Generate code
    if st.button("🤖 Generate Script"):
        generate_script(content, instructions_incode, instructions_prompt, robotc_path, script_path)

# Voice mode          
with tab2:
    recording = st.button("🎤 Start Recording")
    if recording:
        instructions = voice.voice_to_instructions()

        # Prepare instructions for codex
        instructions_incode = ""
        instructions_prompt = "Edit and complete the code below to execute the instructions:\n"
        for index, instruction in enumerate(instructions):
            st.caption(f"{index + 1}. {instruction}")
            instructions_prompt += f"    {index + 1}. {instruction}\n"
            instructions_incode += f"   // {index + 1}. {instruction}\n\n\n"

        # Generate code
        generate_script(content, instructions_incode, instructions_prompt, robotc_path, script_path)