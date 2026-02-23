import streamlit as st
from streamlit_ace import st_ace
import time
import os
import subprocess
import speech_recognition as sr
import random

# Import our new Agentic RAG engine
from rag_engine import build_rag_pipeline

# ---------------------------------------------------------
# 1. SETUP & CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
     page_title="Robo Auto-Script",
     page_icon="🤖",
     initial_sidebar_state="expanded"
)

from dotenv import load_dotenv
load_dotenv()

# Environment variables for Legacy Mode
robotc_path = r'C:\Program Files (x86)\Robomatter Inc\ROBOTC Development Environment 4.X\ROBOTC.exe' 
script_path = r'C:\coding\GitHub\Robo-autoscript\Dashboard\script.c'

if "rag_engine" not in st.session_state:
    with st.spinner("🧠 Initializing Agentic Knowledge Base..."):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        manual_path = os.path.join(base_dir, "ROBOT_Manual.md")
        st.session_state.rag_engine = build_rag_pipeline(manual_path)

# ---------------------------------------------------------
# 2. EXECUTION MODES (Virtual vs Legacy)
# ---------------------------------------------------------
def simulate_execution():
    st.markdown("### 🖥️ Virtual Execution Console")
    with st.status("Executing Pipeline...", expanded=True) as status:
        st.write("⚙️ Parsing natural language to C-Code via Agentic RAG...")
        time.sleep(1)
        st.write("🔨 Compiling ROBOTC script...")
        time.sleep(1)
        st.write("📡 Searching for Virtual VEX Controller on COM3...")
        time.sleep(1)
        st.write("🚀 Uploading instructions to hardware...")
        time.sleep(1.5)
        status.update(label="✅ Execution Complete!", state="complete", expanded=False)
    st.success("🤖 Robot successfully performed the actions in the simulation!")

def legacy_pyautogui_execution(script_path, robotc_path):
    st.warning("⚠️ Running Legacy PyAutoGUI Mode. Do not touch your mouse!")
    try:
        import pyautogui
        subprocess.Popen(robotc_path)
        pyautogui.sleep(1)
        pyautogui.hotkey('ctrl', 'o')
        pyautogui.sleep(1)
        pyautogui.typewrite(script_path)
        pyautogui.sleep(2)
        pyautogui.press('enter')
        pyautogui.sleep(3)
        pyautogui.press('f5')
        st.success('✅ Legacy Compilation Complete!')
    except Exception as e:
        st.error(f"Legacy execution failed. Error: {e}")

def process_and_generate(user_prompt, boilerplate_code, exec_mode):
    with st.spinner('Thinking...'):
        generated_code = st.session_state.rag_engine(
            question=user_prompt, 
            boilerplate=boilerplate_code
        )
        st.code(generated_code, language="c")
        
        with open('script.c', 'w') as f:
            f.write(generated_code)
        st.download_button('⬇️ Download script.c', generated_code.encode('utf-8'), file_name='script.c', mime='text/plain')
        
        if "Virtual Simulator" in exec_mode:
            simulate_execution()
        else:
            legacy_pyautogui_execution(script_path, robotc_path)

# ---------------------------------------------------------
# 3. UI LAYOUT & SIDEBAR
# ---------------------------------------------------------
st.title("🤖 Robo-Autoscript Pipeline")

with st.sidebar:
    st.header("⚙️ Settings")
    execution_mode = st.radio("Execution Mode", ["Virtual Simulator (Safe Demo)", "Legacy RPA (PyAutoGUI Windows)"])
    st.divider()
    boilerplate_choice = st.selectbox("Hardware Config", ["2_wheel_drive", "4_wheel_drive"])
    
    st.divider()
    st.header("🚨 Hardware Interrupts")
    st.write("Simulate an incoming serial signal from the Raspberry Pi CV Module.")
    if st.button("📷 Trigger Camera Obstacle", type="primary"):
        scenarios = [
            "EMERGENCY SENSOR READING: Obstacle directly ahead. The left path is completely clear. The right path is blocked by a wall. Decide how to safely evade.",
            "EMERGENCY SENSOR READING: Obstacle directly ahead. The right path is completely clear. The left path is blocked by a wall. Decide how to safely evade.",
            "EMERGENCY SENSOR READING: Trapped! Obstacles detected ahead, to the left, and to the right. Only the rear is clear. Decide how to safely evade."
        ]
        st.session_state['hardware_interrupt'] = random.choice(scenarios)

try:
    with open(f'boilerplates/{boilerplate_choice}.txt', 'r') as f:
        boilerplate = f.read()
except FileNotFoundError:
    boilerplate = "// Boilerplate missing"

with st.expander("View/Edit Current Boilerplate"):
    boilerplate = st_ace(value=boilerplate, language="c_cpp", height=200)

# Check for hardware interrupts before rendering the rest of the UI
if 'hardware_interrupt' in st.session_state and st.session_state['hardware_interrupt']:
    st.error("🚨 HARDWARE INTERRUPT RECEIVED FROM RASPBERRY PI 🚨")
    st.warning(st.session_state['hardware_interrupt'])
    
    process_and_generate(st.session_state['hardware_interrupt'], boilerplate, execution_mode)
    
    st.session_state['hardware_interrupt'] = None
    st.stop() 

# ---------------------------------------------------------
# 4. MAIN TABS
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Sequence of Instructions (SI)", "Problem Solving (SayCan)", "Voice Control"])

with tab1:
    st.header("Type Sequence of Instructions (SI)")
    if 'instructions' not in st.session_state:
        st.session_state['instructions'] = ['Stop']

    new_instruction = st.text_input("Add an action")
    col1, col2 = st.columns(2)
    if col1.button("➕ Add action") and new_instruction:
        st.session_state['instructions'].insert(-1, new_instruction)
        st.rerun()
    if col2.button("🗑️ Clear All"):
        st.session_state['instructions'] = ['Stop']
        st.rerun()

    instructions_prompt = "Execute the following sequence of instructions in order:\n"
    for index, instruction in enumerate(st.session_state['instructions']):
        st.caption(f"{index + 1}. {instruction}")
        instructions_prompt += f"{index + 1}. {instruction}\n"

    if st.button("🤖 Generate & Execute Script", key="btn_si"):
        process_and_generate(instructions_prompt, boilerplate, execution_mode)

with tab2:
    st.header("Agentic Problem Solving (SayCan)")
    st.write("The AI will decompose the problem and ground it against the physical capabilities of the robot.")
    problem_prompt = st.text_area("Problem Description")
    if st.button("🤖 Generate & Execute Script", key='btn_ps'):
        process_and_generate(problem_prompt, boilerplate, execution_mode)

with tab3:
    st.header("🎤 Voice Control Integration")
    st.write("Click the button and speak your command into the microphone.")
    
    if st.button("🎙️ Start Recording Command"):
        r = sr.Recognizer()
        with st.spinner("Listening... Speak now! (Timeout in 5s)"):
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)
                
                st.info("Transcribing via Google Speech Recognition...")
                voice_text = r.recognize_google(audio)
                st.success(f"**You said:** '{voice_text}'")
                
                process_and_generate(voice_text, boilerplate, execution_mode)
                
            except sr.WaitTimeoutError:
                st.error("No speech detected. Please try again.")
            except sr.UnknownValueError:
                st.error("Could not understand the audio. Please speak clearly.")
            except Exception as e:
                st.error(f"Microphone error: {e}. Check your system permissions.")