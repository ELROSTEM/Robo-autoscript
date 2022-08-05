import streamlit as st
import openai

st.set_page_config(
     page_title="Robo Auto Script",
     page_icon="🤖",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "Scripting RoboC code with OpenAi's Codex"
     }
)

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Instruction input
if 'instructions' not in st.session_state:
    st.session_state['instructions'] = ['Stop']

new_instruction = st.text_input("Add Instruction")
if st.button("Add instruction"):
    st.session_state['instructions'].insert(-1, new_instruction)

instructions_incode = ""
instructions_prompt = "Complete the code below to execute the instructions:\n"
for index, instruction in enumerate(st.session_state['instructions']):
    st.caption(f"{index + 1}. {instruction}")
    instructions_prompt += f"    {index + 1}. {instruction}\n"
    instructions_incode += f"   // {index + 1}. {instruction}\n\n\n"


# Generate code
if st.button("🤖 Generate Script"):
    response = openai.Edit.create(
        model="code-davinci-edit-001",
        input = f"/*\nProgram Description: This program is a RobotC program\n\nRobot Description: The robot has 4 motors with 4 wheels.\n*/\n\nint main()\n{{\n{instructions_incode}\n    ",
        instruction=instructions_prompt,
        temperature=0,
        top_p=1
    )

    if 'choices' in response:
        x = response['choices']
        if len(x) > 0:
            st.code(x[0]['text'], language="c")
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
