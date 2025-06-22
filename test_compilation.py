#!/usr/bin/env python3
"""
Test file for C++ compilation validation
"""

import sys
import os
from src.core.main import compile_cpp_code

def test_valid_cpp_compilation():
    """Test compilation with valid C++ code"""
    print("Testing valid C++ compilation...")
    
    valid_cpp_code = """#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}"""
    
    success, errors = compile_cpp_code(valid_cpp_code, "test_output")
    
    if success:
        print("✅ Valid C++ compilation test PASSED")
        return True
    else:
        print("❌ Valid C++ compilation test FAILED")
        print(f"Errors: {errors}")
        return False

def test_invalid_cpp_compilation():
    """Test compilation with invalid C++ code"""
    print("\nTesting invalid C++ compilation...")
    
    invalid_cpp_code = """#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl
    return 0;  // Missing semicolon
}"""
    
    success, errors = compile_cpp_code(invalid_cpp_code, "test_output")
    
    if not success and errors:
        print("✅ Invalid C++ compilation test PASSED (correctly caught errors)")
        print(f"Expected compilation errors: {errors}")
        return True
    else:
        print("❌ Invalid C++ compilation test FAILED (should have caught errors)")
        return False

def test_missing_gcc():
    """Test behavior when g++ is not available"""
    print("\nTesting missing g++ compiler...")
    
    # This test is informational - we can't easily simulate missing g++ in a test
    # but we can document the expected behavior
    print("ℹ️  This test checks if g++ is available on the system")
    
    try:
        import subprocess
        result = subprocess.run(['g++', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ g++ is available on this system")
            return True
        else:
            print("❌ g++ is not available on this system")
            return False
    except FileNotFoundError:
        print("❌ g++ is not available on this system")
        return False

def main():
    """Run all compilation tests"""
    print("Starting C++ compilation validation tests...")
    print("=" * 60)
    
    # Test 1: Valid C++ compilation
    test1_passed = test_valid_cpp_compilation()
    
    # Test 2: Invalid C++ compilation
    test2_passed = test_invalid_cpp_compilation()
    
    # Test 3: Check g++ availability
    test3_passed = test_missing_gcc()
    
    print("\n" + "=" * 60)
    print("Compilation Test Summary:")
    print(f"Valid C++ compilation: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Invalid C++ compilation: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"g++ availability: {'✅ AVAILABLE' if test3_passed else '❌ NOT AVAILABLE'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 Compilation validation tests passed!")
        return 0
    else:
        print("\n💥 Some compilation tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 