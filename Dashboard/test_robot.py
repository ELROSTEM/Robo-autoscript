import pytest
import os
from rag_engine import build_rag_pipeline

def test_syntax_generation():
    """
    Verifies that the RAG engine produces valid ROBOTC 
    boilerplate and structure when given a prompt.
    """
    # 1. Setup the pipeline using the manual in the same folder
    generate_code = build_rag_pipeline("ROBOT_Manual.md")
    
    # 2. Create a dummy boilerplate with a unique motor name
    test_boilerplate = "// Test Config\n#pragma config(Motor, port2, leftMotor, tmotorNormal, openLoop)"
    
    # 3. Ask for a simple action
    result = generate_code("Move forward for 1 second", test_boilerplate)
    
    # 4. Assertions (The "Checks")
    # Does it have the main task block?
    assert "task main()" in result
    
    # Does it actually contain motor commands?
    assert "motor[" in result
    
    # Does it include the specific motor name from our boilerplate?
    assert "leftMotor" in result
    
    # Does it close the brackets?
    assert "}" in result

if __name__ == "__main__":
    # This allows you to run 'python test_robot.py' manually to check it
    print("🧪 Running local test...")
    try:
        test_syntax_generation()
        print("✅ Test Passed!")
    except AssertionError as e:
        print("❌ Test Failed!")
        raise e