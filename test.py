#!/usr/bin/env python3
"""
Test file for the Python to C++ converter
"""

import sys
import os
from src.core.main import analyze_python_code

def mock_convert_to_cpp(python_code, context=""):
    """Mock version of convert_to_cpp that simulates API response without calling Claude"""
    print("🔧 Using MOCK API (no real API call)")
    
    # Simple mock translation logic
    if "def add_numbers" in python_code:
        return """#include <iostream>

int add_numbers(int a, int b) {
    return a + b;
}

void hello() {
    std::cout << "Hello World" << std::endl;
}

int main() {
    hello();
    int result = add_numbers(5, 3);
    std::cout << "Result: " << result << std::endl;
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
        print("✅ analyze_python_code test PASSED")
    else:
        print("❌ analyze_python_code test FAILED")
        print(f"Expected: {expected}")
        print(f"Got: {result}")
    
    return result == expected

def test_convert_to_cpp():
    """Test the convert_to_cpp function (using mock)"""
    print("\nTesting convert_to_cpp function (MOCK VERSION)...")
    
    # Simple Python code for testing
    test_code = """
def add_numbers(a, b):
    return a + b

def hello():
    print("Hello World")
"""
    
    context = "Simple calculator functions"
    
    print("Calling MOCK API to convert Python to C++...")
    result = mock_convert_to_cpp(test_code, context)
    
    if result is None:
        print("❌ convert_to_cpp test FAILED - Mock API call failed")
        return False
    
    print("✅ Mock API call successful!")
    print(f"C++ code length: {len(result)} characters")
    print("\nGenerated C++ code:")
    print("=" * 50)
    print(result)
    print("=" * 50)
    
    # Basic validation - check if it looks like C++ code
    cpp_indicators = ['#include', 'int main', 'std::', 'cout', 'return', ';']
    has_cpp_elements = any(indicator in result for indicator in cpp_indicators)
    
    if has_cpp_elements:
        print("✅ convert_to_cpp test PASSED - Looks like valid C++ code")
        return True
    else:
        print("❌ convert_to_cpp test FAILED - Doesn't look like C++ code")
        return False

def test_function_structure():
    """Test that the function structure is correct without API"""
    print("\nTesting function structure...")
    
    try:
        # Test if we can import the function
        from src.core.main import convert_to_cpp
        print("✅ Function import successful")
        
        # Test function signature
        import inspect
        sig = inspect.signature(convert_to_cpp)
        params = list(sig.parameters.keys())
        
        if 'python_code' in params and 'context' in params:
            print("✅ Function signature correct")
            return True
        else:
            print("❌ Function signature incorrect")
            return False
            
    except Exception as e:
        print(f"❌ Function structure test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting tests for Python to C++ converter...")
    print("=" * 60)
    
    # Test 1: Analyze function
    test1_passed = test_analyze_python_code()
    
    # Test 2: Function structure
    test2_passed = test_function_structure()
    
    # Test 3: Convert function (mock)
    test3_passed = test_convert_to_cpp()
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"analyze_python_code: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"function_structure: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"convert_to_cpp (mock): {'✅ PASSED' if test3_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 All tests passed!")
        print("💡 Note: Used mock API - no real API calls made")
        return 0
    else:
        print("\n💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())


