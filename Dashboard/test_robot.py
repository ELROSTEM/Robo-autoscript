import pytest
import os
from rag_engine import build_rag_pipeline

def test_syntax_generation():
    # 1. Dynamically find the path to the manual
    # This finds the directory this test file is in (Dashboard)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    manual_path = os.path.join(base_dir, "ROBOT_Manual.md")
    
    # Initialize the pipeline with the absolute path
    generate_code = build_rag_pipeline(manual_path)
    
    test_boilerplate = "// Test Config\n#pragma config(Motor, port2, leftMotor, tmotorNormal, openLoop)"
    result = generate_code("Move forward for 1 second", test_boilerplate)
    
    assert "task main()" in result
    assert "motor[" in result
    assert "leftMotor" in result
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