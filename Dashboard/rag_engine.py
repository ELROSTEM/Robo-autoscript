import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load the environment variables from your .env file secretly
load_dotenv()

def format_docs(docs):
    """Combines retrieved Markdown chunks into a single string of context."""
    return "\n\n".join(doc.page_content for doc in docs)

def build_rag_pipeline(markdown_path: str):
    """Builds the SayCan-style Agentic RAG pipeline."""
    print("🧠 Loading ROBOT_Manual.md...")
    
    # 1. Load and Split the Manual
    loader = TextLoader(markdown_path, encoding="utf-8")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    
    # 2. Create the Vector Store
    vectorstore = FAISS.from_documents(
        splits, 
        OpenAIEmbeddings(model="text-embedding-3-small")
    )
    # We only need the top 2 chunks per step since we are doing micro-queries
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    # Initialize the LLM Engine
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # ---------------------------------------------------------
    # AGENT 1: THE PLANNER (Task Decomposition)
    # ---------------------------------------------------------
    planner_template = """You are a robotic task planner. 
    Break the following complex user request into a simple, numbered list of atomic robotic actions.
    Keep them high-level (e.g., "1. Move forward", "2. Turn left").
    
    CRITICAL RULE: If the user asks the robot to do something physically impossible for a standard wheeled robot 
    (like fly, shoot lasers, jump, or teleport), EXCLUDE that action entirely or replace it with "stop".
    
    User Request: {question}
    
    Output ONLY the numbered list of achievable actions. Do not write code.
    """
    planner_prompt = ChatPromptTemplate.from_template(planner_template)
    planner_chain = planner_prompt | llm | StrOutputParser()

    # ---------------------------------------------------------
    # AGENT 2: THE CODER (Syntax Generation)
    # ---------------------------------------------------------
    coder_template = """You are an expert robotics software engineer programming in ROBOTC.
    You have been given a Grounded Task Plan (a sequence of verified actions) and the relevant Context from the Reference Manual for those actions.
    
    CRITICAL HARDWARE RULE: Look closely at the Boilerplate Configuration provided below. 
    If the boilerplate initializes 4 drive motors (e.g., it includes leftrearMotor and rightrearMotor), 
    you MUST ensure that all your generated locomotion commands apply power to all 4 motors, 
    even if the Context examples only show 2 motors.
    
    Boilerplate Configuration Provided by User:
    {boilerplate}
    
    Grounded Task Plan:
    {task_plan}

    Context from Reference Manual:
    {context}
    
    Write the final, complete ROBOTC script executing the task plan in order. 
    Make sure you declare the task main() block and put your generated code inside it.
    Add comments explaining each step from the task plan.
    Provide ONLY the code. Do not include markdown formatting like ```c, and do not provide explanations.
    """
    coder_prompt = ChatPromptTemplate.from_template(coder_template)
    coder_chain = coder_prompt | llm | StrOutputParser()
    
    # ---------------------------------------------------------
    # THE PIPELINE ORCHESTRATOR
    # ---------------------------------------------------------
    def generate_code(question: str, boilerplate: str):
        # STEP 1: Decompose the problem (The "Say")
        print("\n🧠 [Planner] Decomposing complex task...")
        task_plan = planner_chain.invoke({"question": question})
        print(f"📋 Grounded Task Plan Generated:\n{task_plan}\n")
        
        # STEP 2: Grounding Loop (The "Can")
        print("🔍 [Retriever] Fetching manual chunks for each individual step...")
        steps = task_plan.split('\n')
        all_docs = []
        
        for step in steps:
            if step.strip(): # Ignore empty lines
                # Retrieve context just for this specific micro-action
                docs = retriever.invoke(step)
                all_docs.extend(docs)
        
        # Deduplicate chunks so we don't overflow the context window
        unique_docs = {doc.page_content: doc for doc in all_docs}.values()
        context_str = format_docs(unique_docs)
        
        # STEP 3: Generate the Code
        print("💻 [Coder] Writing final ROBOTC script...")
        return coder_chain.invoke({
            "context": context_str,
            "task_plan": task_plan,
            "boilerplate": boilerplate
        })
        
    return generate_code

# --- Quick Terminal Test ---
if __name__ == "__main__":
    generate_code = build_rag_pipeline("ROBOT_Manual.md")
    
    four_wheel_boilerplate = """
    #pragma config(Motor,  port3,           rightMotor,    tmotorNormal, openLoop, reversed)
    #pragma config(Motor,  port2,           leftMotor,     tmotorNormal, openLoop)
    #pragma config(Motor,  port5,           rightrearMotor,     tmotorNormal, openLoop, reversed)
    #pragma config(Motor,  port4,           leftrearMotor,      tmotorNormal, openLoop)
    """
    
    # We are giving it a complex task WITH an impossible action (flying)
    user_command = "Drive forward to the wall, do a pivot turn left, fly over the wall, and then reverse."
    
    final_code = generate_code(question=user_command, boilerplate=four_wheel_boilerplate)
    print("\n--- FINAL C CODE ---\n")
    print(final_code)