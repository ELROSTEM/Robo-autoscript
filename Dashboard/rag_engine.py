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
    """Builds the vector database and the LangChain QA pipeline from a Markdown file."""
    print("🧠 Loading ROBOT_Manual.md...")
    
    # 1. Load the Markdown file
    loader = TextLoader(markdown_path, encoding="utf-8")
    docs = loader.load()
    
    # 2. Split the text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    
    # 3. Create the FAISS Vector Database using the cheapest embedding model
    vectorstore = FAISS.from_documents(
        splits, 
        OpenAIEmbeddings(model="text-embedding-3-small")
    )
    
    # We retrieve the top 3 most relevant chunks based on the user's prompt
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # 4. Create the Prompt with the boilerplate injected dynamically
    template = """You are an expert robotics software engineer programming in ROBOTC.
    Use the following pieces of retrieved documentation to write the exact C code that accomplishes the user's request.
    
    Boilerplate Configuration Provided by User:
    {boilerplate}
    
    Context from Reference Manual:
    {context}
    
    User Request: {question}
    
    Provide ONLY the final, complete ROBOTC script including the boilerplate at the top. 
    Make sure you declare the task main() block and put your generated code inside it.
    Do not include markdown formatting like ```c, and do not provide explanations.
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    # 5. Initialize the LLM (using the cheapest, smartest model)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # 6. Chain it all together using LangChain Expression Language (LCEL)
    full_chain = prompt | llm | StrOutputParser()
    
    # 7. Define the generation function
    def generate_code(question: str, boilerplate: str):
        # Retrieve context based ONLY on the question
        docs = retriever.invoke(question)
        context_str = format_docs(docs)
        
        # Pass everything into the prompt and generate
        return full_chain.invoke({
            "context": context_str,
            "question": question,
            "boilerplate": boilerplate
        })
        
    return generate_code

if __name__ == "__main__":
    # --- TEST PHASE ---
    # Make sure 'ROBOT_Manual.md' is in the same directory, 
    # and your .env file contains OPENAI_API_KEY="sk-..."
    
    four_wheel_boilerplate = """
    #pragma config(Motor,  port3,           rightMotor,    tmotorNormal, openLoop, reversed)
    #pragma config(Motor,  port2,           leftMotor,     tmotorNormal, openLoop)
    #pragma config(Motor,  port5,           rightrearMotor,     tmotorNormal, openLoop, reversed)
    #pragma config(Motor,  port4,           leftrearMotor,      tmotorNormal, openLoop)
    /*
    Program Description: This program is a RobotC program
    Robot Description: The robot has 4 motors with 4 wheels
    */
    """
    
    generate_code = build_rag_pipeline("ROBOT_Manual.md")
    
    user_command = "Move forward for a bit, then do a pivot turn to the left, and then stop."
    print(f"\n🤖 Generating code for 4-WHEEL DRIVE: '{user_command}'...\n")
    
    generated_code = generate_code(question=user_command, boilerplate=four_wheel_boilerplate)
    print(generated_code)