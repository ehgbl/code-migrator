#!/usr/bin/env python3
"""
Test file for the Python to C++ converter
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path
from src.core.main import analyze_python_code, convert_to_cpp, write_cpp_file, read_python_file

def create_test_files():
    """Create test input and output files"""
    # Create test input file
    test_input_code = """def greet(name):
    print(f"Hello, {name}!")

def calculate_sum(a, b):
    return a + b

if __name__ == "__main__":
    greet("World")
    result = calculate_sum(5, 3)
    print(f"Sum: {result}")
"""
    
    with open("input.py", "w", encoding="utf-8") as f:
        f.write(test_input_code)
    
    print(" Created test input.py file")

def cleanup_test_files():
    """Clean up test files"""
    files_to_remove = ["input.py", "output.cpp"]
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f" Removed {file}")

def mock_convert_to_cpp(python_code, context=""):
    """Mock version of convert_to_cpp that simulates API response without calling Claude"""
    print("🔧 Using MOCK API (no real API call)")
    
    # Simple mock translation logic
    if "def calculate_sum" in python_code:
        return """#include <iostream>
#include <string>

void greet(const std::string& name) {
    std::cout << "Hello, " << name << "!" << std::endl;
}

int calculate_sum(int a, int b) {
    return a + b;
}

int main() {
    greet("World");
    int result = calculate_sum(5, 3);
    std::cout << "Sum: " << result << std::endl;
    return 0;
}"""
    else:
        return """#include <iostream>

void hello() {
    std::cout << "Hello World" << std::endl;
}

int main() {
    hello();
    return 0;
}"""

def test_analyze_python_code():
    """Test the analyze_python_code function"""
    print("Testing analyze_python_code function...")
    
    # Simple Python code for testing
    test_code = """
import math

def hello():
    print("Hello World")

def add_numbers(a, b):
    return a + b

class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x):
        self.result += x
        return self.result
"""
    
    result = analyze_python_code(test_code)
    print(f"Analysis result: {result}")
    
    # Check if the analysis is correct
    expected = {
        'functions': 4,  # hello, add_numbers, __init__, add
        'classes': 1,    # Calculator
        'imports': 1,    # import math
        'total_lines': 17
    }
    
    if result == expected:
        print(" analyze_python_code test PASSED")
    else:
        print("analyze_python_code test FAILED")
        print(f"Expected: {expected}")
        print(f"Got: {result}")
    
    return result == expected

def test_read_python_file():
    """Test the read_python_file function"""
    print("\nTesting read_python_file function...")
    
    # Test reading the input file
    result = read_python_file("input.py")
    
    if result is None:
        print("read_python_file test FAILED - Could not read input.py")
        return False
    
    if "def greet" in result and "def calculate_sum" in result:
        print("read_python_file test PASSED")
        return True
    else:
        print("read_python_file test FAILED - File content not as expected")
        return False

def test_write_cpp_file():
    """Test the write_cpp_file function"""
    print("\nTesting write_cpp_file function...")
    
    test_cpp_code = """#include <iostream>

int main() {
    std::cout << "Hello World" << std::endl;
    return 0;
}"""
    
    result = write_cpp_file(test_cpp_code, "output.cpp")
    
    if not result:
        print("write_cpp_file test FAILED - Could not write file")
        return False
    
    # Check if file was created and has content
    if os.path.exists("output.cpp"):
        with open("output.cpp", "r", encoding="utf-8") as f:
            content = f.read()
        if "#include" in content and "main()" in content:
            print(" write_cpp_file test PASSED")
            return True
        else:
            print("write_cpp_file test FAILED - File content not as expected")
            return False
    else:
        print("write_cpp_file test FAILED - File was not created")
        return False

def test_convert_to_cpp():
    """Test the convert_to_cpp function (using mock)"""
    print("\nTesting convert_to_cpp function (MOCK VERSION)...")
    
    # Read the test input file
    python_code = read_python_file("input.py")
    if python_code is None:
        print(" convert_to_cpp test FAILED - Could not read input file")
        return False
    
    context = "Simple greeting and calculation functions"
    
    print("Calling MOCK API to convert Python to C++...")
    result = mock_convert_to_cpp(python_code, context)
    
    if result is None:
        print(" convert_to_cpp test FAILED - Mock API call failed")
        return False
    
    print(" Mock API call successful!")
    print(f"C++ code length: {len(result)} characters")
    
    # Basic validation - check if it looks like C++ code
    cpp_indicators = ['#include', 'int main', 'std::', 'cout', 'return', ';']
    has_cpp_elements = any(indicator in result for indicator in cpp_indicators)
    
    if has_cpp_elements:
        print(" convert_to_cpp test PASSED - Looks like valid C++ code")
        return True
    else:
        print(" convert_to_cpp test FAILED - Doesn't look like C++ code")
        return False

def test_complete_workflow():
    """Test the complete workflow"""
    print("\nTesting complete workflow...")
    
    # Step 1: Read Python file
    python_code = read_python_file("input.py")
    if python_code is None:
        print(" Workflow test FAILED - Could not read input file")
        return False
    
    # Step 2: Analyze code
    analysis = analyze_python_code(python_code)
    print(f"Analysis: {analysis['functions']} functions, {analysis['classes']} classes, {analysis['imports']} imports")
    
    # Step 3: Convert to C++
    cpp_code = mock_convert_to_cpp(python_code, "Test workflow")
    if cpp_code is None:
        print(" Workflow test FAILED - Could not convert to C++")
        return False
    
    # Step 4: Write output file
    if write_cpp_file(cpp_code, "output.cpp"):
        print(" Complete workflow test PASSED")
        print("Generated C++ code:")
        print("=" * 50)
        print(cpp_code)
        print("=" * 50)
        return True
    else:
        print(" Workflow test FAILED - Could not write output file")
        return False

def test_function_structure():
    """Test that the function structure is correct without API"""
    print("\nTesting function structure...")
    
    try:
        # Test if we can import the function
        from src.core.main import convert_to_cpp
        print(" Function import successful")
        
        # Test function signature
        import inspect
        sig = inspect.signature(convert_to_cpp)
        params = list(sig.parameters.keys())
        
        if 'python_code' in params and 'context' in params:
            print(" Function signature correct")
            return True
        else:
            print(" Function signature incorrect")
            return False
            
    except Exception as e:
        print(f" Function structure test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting tests for Python to C++ converter...")
    print("=" * 60)
    
    # Create test files
    create_test_files()
    
    # Test 1: Analyze function
    test1_passed = test_analyze_python_code()
    
    # Test 2: Function structure
    test2_passed = test_function_structure()
    
    # Test 3: Read file function
    test3_passed = test_read_python_file()
    
    # Test 4: Write file function
    test4_passed = test_write_cpp_file()
    
    # Test 5: Convert function (mock)
    test5_passed = test_convert_to_cpp()
    
    # Test 6: Complete workflow
    test6_passed = test_complete_workflow()
    
    # Cleanup
    cleanup_test_files()
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"analyze_python_code: {' PASSED' if test1_passed else ' FAILED'}")
    print(f"function_structure: {' PASSED' if test2_passed else ' FAILED'}")
    print(f"read_python_file: {' PASSED' if test3_passed else ' FAILED'}")
    print(f"write_cpp_file: {' PASSED' if test4_passed else ' FAILED'}")
    print(f"convert_to_cpp (mock): {' PASSED' if test5_passed else ' FAILED'}")
    print(f"complete_workflow: {' PASSED' if test6_passed else ' FAILED'}")
    
    all_tests_passed = all([test1_passed, test2_passed, test3_passed, test4_passed, test5_passed, test6_passed])
    
    if all_tests_passed:
        print("\n🎉 All tests passed!")
        print("💡 Note: Used mock API - no real API calls made")
        return 0
    else:
        print("\n💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())


