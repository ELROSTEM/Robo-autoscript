import streamlit as st
from streamlit_ace import st_ace
import time
import os
import subprocess

# Import our new modern RAG engine
from rag_engine import build_rag_pipeline

# ---------------------------------------------------------
# 1. SETUP & CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
     page_title="Robo Auto-Script",
     page_icon="🤖",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "Scripting RobotC code with RAG for Robotics Control"
     }
)

from dotenv import load_dotenv
load_dotenv()

# Environment variables for Legacy Mode
robotc_path = r'C:\Program Files (x86)\Robomatter Inc\ROBOTC Development Environment 4.X\ROBOTC.exe' 
script_path = r'C:\coding\GitHub\Robo-autoscript\Dashboard\script.c'

if "rag_engine" not in st.session_state:
    with st.spinner("🧠 Initializing Robot Knowledge Base..."):
        st.session_state.rag_engine = build_rag_pipeline("ROBOT_Manual.md")

# ---------------------------------------------------------
# 2. EXECUTION MODES (Virtual vs Legacy)
# ---------------------------------------------------------
def simulate_execution():
    """Simulates compiling and sending code to a robot for portfolio demos."""
    st.markdown("### 🖥️ Virtual Execution Console")
    with st.status("Executing Pipeline...", expanded=True) as status:
        st.write("⚙️ Parsing natural language to C-Code via RAG...")
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
    """The original RPA fallback for physical Windows execution."""
    st.warning("⚠️ Running Legacy PyAutoGUI Mode. Do not touch your mouse!")
    try:
        import pyautogui
        # Open RoboC and Compile the script
        subprocess.Popen(robotc_path)
        pyautogui.sleep(1)
        pyautogui.hotkey('ctrl', 'o') # Open file
        pyautogui.sleep(1)
        pyautogui.typewrite(script_path) # Type the path to the script
        pyautogui.sleep(2)
        pyautogui.press('enter') # Press enter
        pyautogui.sleep(3)
        pyautogui.press('f5') # Compile
        st.success('✅ Legacy Compilation Complete!')
    except ImportError:
        st.error("PyAutoGUI is not installed in this environment.")
    except Exception as e:
        st.error(f"Legacy execution failed (likely not on Windows). Error: {e}")

def process_and_generate(user_prompt, boilerplate_code, exec_mode):
    """Handles the RAG generation and UI updates."""
    with st.spinner('Thinking...'):
        generated_code = st.session_state.rag_engine(
            question=user_prompt, 
            boilerplate=boilerplate_code
        )
        
        st.code(generated_code, language="c")
        
        with open('script.c', 'w') as f:
            f.write(generated_code)
            
        st.download_button(
            '⬇️ Download script.c', 
            generated_code.encode('utf-8'), 
            file_name='script.c', 
            mime='text/plain'
        )
        
        # Route the execution based on the UI toggle
        if exec_mode == "Virtual Simulator (Safe Demo)":
            simulate_execution()
        else:
            legacy_pyautogui_execution(script_path, robotc_path)

# ---------------------------------------------------------
# 3. UI LAYOUT
# ---------------------------------------------------------
st.title("🤖 Robo-Autoscript Pipeline")

# SIDEBAR: Settings & Execution Mode
with st.sidebar:
    st.header("⚙️ Settings")
    execution_mode = st.radio(
        "Execution Mode", 
        ["Virtual Simulator (Safe Demo)", "Legacy RPA (PyAutoGUI Windows)"],
        help="Virtual mode simulates the hardware connection. Legacy mode physically takes over the mouse to open ROBOTC.exe."
    )
    st.divider()
    boilerplate_choice = st.selectbox("Hardware Config", ["2_wheel_drive", "4_wheel_drive"])

try:
    with open(f'boilerplates/{boilerplate_choice}.txt', 'r') as f:
        boilerplate = f.read()
except FileNotFoundError:
    st.error(f"Could not find boilerplates/{boilerplate_choice}.txt")
    boilerplate = "// Boilerplate missing"

with st.expander("View/Edit Current Boilerplate"):
    boilerplate = st_ace(value=boilerplate, language="c_cpp", height=200)

tab1, tab2, tab3 = st.tabs(["Sequence of Instructions (SI)", "Problem Solving (PS)", "Voice Control"])

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

    st.markdown("**Current Sequence:**")
    instructions_prompt = "Execute the following sequence of instructions in order:\n"
    for index, instruction in enumerate(st.session_state['instructions']):
        st.caption(f"{index + 1}. {instruction}")
        instructions_prompt += f"{index + 1}. {instruction}\n"

    if st.button("🤖 Generate & Execute Script", key="btn_si"):
        process_and_generate(instructions_prompt, boilerplate, execution_mode)

with tab2:
    st.header("Type Problem Solving (PS)")
    problem_prompt = st.text_area("Problem Description")
    if st.button("🤖 Generate & Execute Script", key='btn_ps'):
        process_and_generate(problem_prompt, boilerplate, execution_mode)

with tab3:
    st.header("🎤 Voice Control Integration")
    st.info("Voice integration coming in Phase 3!")